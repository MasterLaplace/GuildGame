"""
ECS Systems — All simulation logic.
Systems iterate over entities with specific components and update them.
"""
import math
import random
import statistics
from ecs_core import System
from components import Position, Velocity, Biological, Genetics, Renderable, Affiliation
from settings import *

# ─── Helper ──────────────────────────────────────────────────────────

def dist2(ax, ay, bx, by):
    dx, dy = ax - bx, ay - by
    return dx*dx + dy*dy

def dist(ax, ay, bx, by):
    return math.sqrt(dist2(ax, ay, bx, by))

# Global lineage counter
_lineage_counter = 1000

def next_lineage_id():
    global _lineage_counter
    _lineage_counter += 1
    return _lineage_counter

# Global pack counter
_pack_counter = 0

def next_pack_id():
    global _pack_counter
    _pack_counter += 1
    return _pack_counter

# ─── Movement System ─────────────────────────────────────────────────

class MovementSystem(System):
    def __init__(self, registry, scent_map):
        super().__init__(registry)
        self.scent_map = scent_map

    def update(self, dt):
        for entity in self.registry.view(Position, Velocity, Biological, Genetics):
            pos = self.registry.get_component(entity, Position)
            vel = self.registry.get_component(entity, Velocity)
            bio = self.registry.get_component(entity, Biological)
            gen = self.registry.get_component(entity, Genetics)

            tx, ty = 0.0, 0.0

            if bio.state == "WANDER":
                tx = vel.vx + random.uniform(-1.5, 1.5)
                ty = vel.vy + random.uniform(-1.5, 1.5)

            elif bio.state == "SEEK":
                if bio.diet_type == "HERBIVORE":
                    gx, gy = self.scent_map.get_gradient(0, pos.x, pos.y)  # follow plant scent
                elif bio.diet_type == "CARNIVORE":
                    gx, gy = self.scent_map.get_gradient(1, pos.x, pos.y)  # follow herbivore scent
                else:
                    gx, gy = 0, 0
                tx = gx * gen.max_speed
                ty = gy * gen.max_speed
                # Add small wander noise to avoid getting stuck
                tx += random.uniform(-0.3, 0.3)
                ty += random.uniform(-0.3, 0.3)

            elif bio.state == "FLEE":
                # Herbivores flee carnivore scent (channel 2)
                gx, gy = self.scent_map.get_gradient(2, pos.x, pos.y)
                tx = -gx * gen.max_speed * 1.3  # flee is faster than normal
                ty = -gy * gen.max_speed * 1.3
                # Also flee boss terror (channel 3)
                bx, by = self.scent_map.get_gradient(3, pos.x, pos.y)
                tx -= bx * gen.max_speed
                ty -= by * gen.max_speed
                # Add noise
                tx += random.uniform(-1, 1)
                ty += random.uniform(-1, 1)

            elif bio.state == "STARVING":
                # Desperate: wander more aggressively, ignore human zone fear
                tx = vel.vx + random.uniform(-2, 2)
                ty = vel.vy + random.uniform(-2, 2)
                # Starving carnivores head toward herbivore scent
                if bio.diet_type == "CARNIVORE":
                    gx, gy = self.scent_map.get_gradient(1, pos.x, pos.y)
                    tx += gx * gen.max_speed * 0.5
                    ty += gy * gen.max_speed * 0.5
                # If truly desperate, head toward human zone
                if bio.energy < bio.max_energy * 0.1:
                    dx = HUMAN_ZONE_CENTER[0] - pos.x
                    dy = HUMAN_ZONE_CENTER[1] - pos.y
                    d = math.sqrt(dx*dx + dy*dy) + 0.001
                    tx += (dx/d) * 2.0
                    ty += (dy/d) * 2.0

            elif bio.state == "REPRODUCE":
                tx, ty = 0, 0  # Stay still during reproduction

            # Avoid human zone if not starving
            if bio.state not in ("STARVING",):
                dx = pos.x - HUMAN_ZONE_CENTER[0]
                dy = pos.y - HUMAN_ZONE_CENTER[1]
                d = math.sqrt(dx*dx + dy*dy) + 0.001
                if d < HUMAN_ZONE_RADIUS * 1.8:
                    tx += (dx / d) * HUMAN_ZONE_REPULSION
                    ty += (dy / d) * HUMAN_ZONE_REPULSION

            # Normalize to max speed
            length = math.sqrt(tx*tx + ty*ty)
            if length > 0.001:
                vel.vx = (tx / length) * gen.max_speed
                vel.vy = (ty / length) * gen.max_speed

            pos.x += vel.vx * dt
            pos.y += vel.vy * dt

            # Bounce at boundaries
            if pos.x < 5:    pos.x = 5;    vel.vx = abs(vel.vx)
            if pos.x > SCREEN_WIDTH-5:  pos.x = SCREEN_WIDTH-5;  vel.vx = -abs(vel.vx)
            if pos.y < 5:    pos.y = 5;    vel.vy = abs(vel.vy)
            if pos.y > SCREEN_HEIGHT-5: pos.y = SCREEN_HEIGHT-5; vel.vy = -abs(vel.vy)


# ─── Biological System (Energy, Aging, State Transitions) ────────────

class BiologicalSystem(System):
    def update(self, dt):
        dead = []
        for entity in self.registry.view(Biological, Genetics):
            bio = self.registry.get_component(entity, Biological)
            gen = self.registry.get_component(entity, Genetics)

            if bio.diet_type == "PLANT":
                continue  # Plants don't drain energy

            bio.age += dt

            # Energy drain: base rate + speed cost
            if bio.diet_type == "HERBIVORE":
                drain = HERBIVORE_ENERGY_DRAIN + (gen.max_speed * 0.01)
            else:
                drain = CARNIVORE_ENERGY_DRAIN + (gen.max_speed * 0.008)
            bio.energy -= drain * dt

            # Death by starvation
            if bio.energy <= 0:
                dead.append(entity)
                continue

            # FSM state transitions based on energy
            if bio.energy < bio.max_energy * 0.25:
                if bio.state != "FLEE":  # Don't override FLEE
                    bio.state = "STARVING"
            elif bio.energy >= bio.reproduce_cost:
                bio.state = "REPRODUCE"
            else:
                if bio.state not in ("SEEK", "FLEE"):  # Don't override active states
                    bio.state = "WANDER"

        for e in dead:
            self.registry.destroy_entity(e)


# ─── Interaction System (Feeding, Combat, Scent, Fleeing, Reproduction) ──

class InteractionSystem(System):
    def __init__(self, registry, spatial_grid, scent_map):
        super().__init__(registry)
        self.spatial_grid = spatial_grid
        self.scent_map = scent_map
        # Population stats for anomaly detection (updated each frame)
        self._pop_stats = {}

    def _compute_population_stats(self, entities):
        """Compute mean and std of strength for each species for anomaly detection."""
        by_species = {}
        for eid in entities:
            aff = self.registry.get_component(eid, Affiliation)
            gen = self.registry.get_component(eid, Genetics)
            if aff and gen:
                if aff.species_id not in by_species:
                    by_species[aff.species_id] = []
                by_species[aff.species_id].append(gen.strength)
        stats = {}
        for sid, strengths in by_species.items():
            if len(strengths) >= 3:
                m = statistics.mean(strengths)
                s = statistics.stdev(strengths) if len(strengths) > 1 else 1.0
                stats[sid] = (m, max(s, 0.1))
        self._pop_stats = stats

    def _count_local_same_species(self, pos, species_id, radius):
        """Count how many entities of the same species are within radius."""
        nearby = self.spatial_grid.get_nearby(pos.x, pos.y, radius)
        count = 0
        for eid in nearby:
            aff = self.registry.get_component(eid, Affiliation)
            if aff and aff.species_id == species_id:
                epos = self.registry.get_component(eid, Position)
                if epos and dist(pos.x, pos.y, epos.x, epos.y) <= radius:
                    count += 1
        return count

    def _find_mate(self, entity, pos, gen, aff, radius):
        """Find a nearby entity of same species with energy > reproduce_cost."""
        nearby = self.spatial_grid.get_nearby(pos.x, pos.y, radius)
        best = None
        best_fitness = -1
        for eid in nearby:
            if eid == entity:
                continue
            other_aff = self.registry.get_component(eid, Affiliation)
            other_bio = self.registry.get_component(eid, Biological)
            if (other_aff and other_bio
                    and other_aff.species_id == aff.species_id
                    and other_bio.energy >= other_bio.reproduce_cost * 0.5
                    and other_bio.state != "FLEE"):
                other_pos = self.registry.get_component(eid, Position)
                if other_pos and dist(pos.x, pos.y, other_pos.x, other_pos.y) < radius:
                    other_gen = self.registry.get_component(eid, Genetics)
                    if other_bio.fitness > best_fitness:
                        best = eid
                        best_fitness = other_bio.fitness
        return best

    def _spawn_offspring(self, parent_a, parent_b, mutation_amplitude):
        """Create a child entity from two parents with crossover + mutation."""
        pos_a = self.registry.get_component(parent_a, Position)
        bio_a = self.registry.get_component(parent_a, Biological)
        gen_a = self.registry.get_component(parent_a, Genetics)
        ren_a = self.registry.get_component(parent_a, Renderable)
        aff_a = self.registry.get_component(parent_a, Affiliation)
        gen_b = self.registry.get_component(parent_b, Genetics)

        # Crossover then mutate
        child_gen = Genetics.crossover(gen_a, gen_b)
        child_gen = child_gen.mutate(amplitude=mutation_amplitude)

        # Inherit parent properties
        child_bio = Biological(
            bio_a.diet_type,
            energy=bio_a.max_energy * 0.4,
            max_energy=bio_a.max_energy,
            reproduce_cost=bio_a.reproduce_cost
        )
        child_pos = Position(
            pos_a.x + random.uniform(-15, 15),
            pos_a.y + random.uniform(-15, 15)
        )
        child_vel = Velocity(random.uniform(-0.5, 0.5), random.uniform(-0.5, 0.5))

        base_size = ren_a.size * (child_gen.size_factor / gen_a.size_factor)
        base_size = max(2.0, min(base_size, 20.0))

        child_ren = Renderable(ren_a.color, base_size, ren_a.shape, False)
        child_aff = Affiliation(
            species_id=aff_a.species_id,
            lineage_id=aff_a.lineage_id,
            pack_id=-1
        )

        child = self.registry.create_entity()
        self.registry.add_component(child, child_pos)
        self.registry.add_component(child, child_vel)
        self.registry.add_component(child, child_bio)
        self.registry.add_component(child, child_gen)
        self.registry.add_component(child, child_ren)
        self.registry.add_component(child, child_aff)

        # Check for anomaly by standard deviation
        species_stats = self._pop_stats.get(aff_a.species_id)
        if species_stats and not ren_a.is_anomaly:
            mean_str, std_str = species_stats
            if child_gen.strength > mean_str + ANOMALY_SIGMA_THRESHOLD * std_str:
                child_ren.is_anomaly = True
                child_ren.color = COLORS["ANOMALY"]
                child_ren.size *= ANOMALY_SIZE_MULTIPLIER
                child_gen.size_factor *= ANOMALY_SIZE_MULTIPLIER

        return child

    def update(self, dt):
        # Rebuild spatial grid
        self.spatial_grid.clear()
        all_entities = self.registry.view(Position)
        for eid in all_entities:
            p = self.registry.get_component(eid, Position)
            self.spatial_grid.insert(eid, p.x, p.y)

        # Compute population statistics for anomaly detection
        living = self.registry.view(Position, Biological, Genetics, Affiliation)
        self._compute_population_stats(living)

        dead = set()

        for entity in living:
            if entity in dead:
                continue
            pos = self.registry.get_component(entity, Position)
            bio = self.registry.get_component(entity, Biological)
            gen = self.registry.get_component(entity, Genetics)
            ren = self.registry.get_component(entity, Renderable)
            aff = self.registry.get_component(entity, Affiliation)

            if bio.diet_type == "PLANT":
                # Plants just emit scent
                self.scent_map.add_scent(0, pos.x, pos.y, PLANT_SCENT_AMOUNT)
                continue

            # ── Emit scents ──
            if bio.diet_type == "HERBIVORE":
                self.scent_map.add_scent(1, pos.x, pos.y, 8.0)
            elif bio.diet_type == "CARNIVORE":
                self.scent_map.add_scent(2, pos.x, pos.y, 12.0)
            if ren.is_anomaly:
                self.scent_map.add_scent(3, pos.x, pos.y, ANOMALY_TERROR_SCENT)

            # ── Reproduction with crossover ──
            if bio.state == "REPRODUCE":
                # Check carrying capacity
                if bio.diet_type == "HERBIVORE":
                    k = CARRYING_CAPACITY_HERBIVORE
                else:
                    k = CARRYING_CAPACITY_CARNIVORE
                local_pop = self._count_local_same_species(pos, aff.species_id, CARRYING_CAPACITY_RADIUS)
                if local_pop < k:
                    mate = self._find_mate(entity, pos, gen, aff, gen.vision_radius)
                    if mate and mate not in dead:
                        # Determine mutation amplitude (meltdown check)
                        if local_pop <= MELTDOWN_POP_THRESHOLD:
                            amp = MELTDOWN_MUTATION_AMPLITUDE
                        else:
                            amp = MUTATION_AMPLITUDE
                        self._spawn_offspring(entity, mate, amp)
                        bio.energy -= bio.reproduce_cost  # Full cost
                        mate_bio = self.registry.get_component(mate, Biological)
                        if mate_bio:
                            mate_bio.energy -= mate_bio.reproduce_cost * 0.3
                bio.state = "WANDER"

            # ── Interaction with nearby entities ──
            nearby = self.spatial_grid.get_nearby(pos.x, pos.y, gen.vision_radius)
            can_see_food = False
            should_flee = False

            for other in nearby:
                if other == entity or other in dead:
                    continue
                other_pos = self.registry.get_component(other, Position)
                if not other_pos:
                    continue
                d = dist(pos.x, pos.y, other_pos.x, other_pos.y)
                if d > gen.vision_radius:
                    continue

                other_bio = self.registry.get_component(other, Biological)
                if not other_bio:
                    continue
                other_ren = self.registry.get_component(other, Renderable)

                # ── Herbivore eats plant ──
                if bio.diet_type == "HERBIVORE" and other_bio.diet_type == "PLANT":
                    can_see_food = True
                    if d < EAT_RANGE:
                        gained = other_bio.energy * gen.absorption_rate
                        bio.energy = min(bio.max_energy, bio.energy + gained)
                        bio.energy_absorbed += gained
                        dead.add(other)

                # ── Carnivore eats herbivore ──
                elif bio.diet_type == "CARNIVORE" and other_bio.diet_type == "HERBIVORE":
                    can_see_food = True
                    if d < COMBAT_RANGE:
                        # Combat: strength vs strength
                        if gen.strength >= other_bio.fitness * 0.1 + random.uniform(0, 5):
                            gained = CARNIVORE_EAT_ENERGY * gen.absorption_rate
                            bio.energy = min(bio.max_energy, bio.energy + gained)
                            bio.kills += 1
                            bio.energy_absorbed += gained
                            dead.add(other)

                # ── Carnivore territorial combat ──
                elif (bio.diet_type == "CARNIVORE" and other_bio.diet_type == "CARNIVORE"):
                    other_aff = self.registry.get_component(other, Affiliation)
                    # Fight if different lineage and close
                    if (other_aff and aff.lineage_id != other_aff.lineage_id
                            and d < COMBAT_RANGE):
                        if gen.strength > self.registry.get_component(other, Genetics).strength:
                            bio.kills += 1
                            gained = CARNIVORE_EAT_ENERGY * 0.3
                            bio.energy = min(bio.max_energy, bio.energy + gained)
                            dead.add(other)
                        else:
                            bio.damage_taken += 10

                # ── Herbivore detects carnivore → FLEE ──
                if (bio.diet_type == "HERBIVORE"
                        and other_bio.diet_type == "CARNIVORE"
                        and d < gen.vision_radius * 0.8):
                    should_flee = True

                # ── Everyone flees anomalies (except other anomalies) ──
                if (other_ren and other_ren.is_anomaly
                        and not ren.is_anomaly
                        and d < gen.vision_radius):
                    should_flee = True

            # ── Update FSM based on perception ──
            if should_flee and bio.state not in ("STARVING",):
                bio.state = "FLEE"
            elif can_see_food and bio.state not in ("FLEE", "STARVING", "REPRODUCE"):
                bio.state = "SEEK"

        for e in dead:
            self.registry.destroy_entity(e)


# ─── Pack System ─────────────────────────────────────────────────────

class PackSystem(System):
    """Manages pack formation, alpha election, dissolution, and budding."""
    def __init__(self, registry, spatial_grid):
        super().__init__(registry)
        self.spatial_grid = spatial_grid
        self._tick = 0

    def update(self, dt):
        self._tick += 1
        if self._tick % 30 != 0:  # Run every 0.5 seconds
            return

        carnivores = self.registry.view(Position, Biological, Affiliation, Genetics)
        carn_list = []
        for eid in carnivores:
            bio = self.registry.get_component(eid, Biological)
            if bio.diet_type == "CARNIVORE":
                carn_list.append(eid)

        # ── Pack formation: solitary carnivores of same lineage group up ──
        for eid in carn_list:
            aff = self.registry.get_component(eid, Affiliation)
            if aff.pack_id != -1:
                continue
            pos = self.registry.get_component(eid, Position)
            nearby = self.spatial_grid.get_nearby(pos.x, pos.y, PACK_FORMATION_RADIUS)
            for other in nearby:
                if other == eid:
                    continue
                other_aff = self.registry.get_component(other, Affiliation)
                other_bio = self.registry.get_component(other, Biological)
                if (other_aff and other_bio
                        and other_bio.diet_type == "CARNIVORE"
                        and other_aff.lineage_id == aff.lineage_id):
                    other_pos = self.registry.get_component(other, Position)
                    if other_pos and dist(pos.x, pos.y, other_pos.x, other_pos.y) < PACK_FORMATION_RADIUS:
                        if other_aff.pack_id != -1:
                            aff.pack_id = other_aff.pack_id
                        else:
                            pid = next_pack_id()
                            aff.pack_id = pid
                            other_aff.pack_id = pid
                        break

        # ── Alpha election & budding ──
        packs = {}
        for eid in carn_list:
            aff = self.registry.get_component(eid, Affiliation)
            if aff.pack_id != -1:
                packs.setdefault(aff.pack_id, []).append(eid)

        for pack_id, members in packs.items():
            # Elect alpha (highest fitness)
            best = None
            best_fit = -1
            for m in members:
                bio = self.registry.get_component(m, Biological)
                aff = self.registry.get_component(m, Affiliation)
                aff.is_alpha = False
                if bio.fitness > best_fit:
                    best = m
                    best_fit = bio.fitness
            if best:
                self.registry.get_component(best, Affiliation).is_alpha = True

            # Budding: if pack too large, split
            if len(members) > PACK_MAX_SIZE:
                new_pid = next_pack_id()
                for m in members[PACK_MAX_SIZE // 2:]:
                    self.registry.get_component(m, Affiliation).pack_id = new_pid

        # ── Dissolution: check if alpha still exists ──
        for pack_id, members in packs.items():
            has_alpha = any(
                self.registry.get_component(m, Affiliation).is_alpha for m in members
            )
            if not has_alpha and random.random() < PACK_DISSOLUTION_CHANCE:
                for m in members:
                    self.registry.get_component(m, Affiliation).pack_id = -1
