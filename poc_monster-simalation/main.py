"""
Main entry point — Pygame loop, entity spawning, rendering, and reporting.
"""
import pygame
import random
import sys
import json
import time
import math

from ecs_core import Registry
from components import Position, Velocity, Renderable, Biological, Genetics, Affiliation
from spatial import SpatialHashGrid, ScentMap
from systems import (MovementSystem, BiologicalSystem, InteractionSystem,
                     PackSystem, next_lineage_id)
from settings import *

# ─── Entity Factories ────────────────────────────────────────────────

def spawn_plant(registry):
    e = registry.create_entity()
    registry.add_component(e, Position(random.uniform(20, SCREEN_WIDTH-20),
                                       random.uniform(20, SCREEN_HEIGHT-20)))
    registry.add_component(e, Renderable(COLORS["PLANT"], 3, "rect"))
    registry.add_component(e, Biological("PLANT", PLANT_ENERGY, PLANT_ENERGY, 0))
    registry.add_component(e, Genetics(0, 0, 0, 1.0, 1.0, 0))
    registry.add_component(e, Affiliation(0))

def spawn_herbivore(registry):
    e = registry.create_entity()
    lid = next_lineage_id()
    registry.add_component(e, Position(random.uniform(20, SCREEN_WIDTH-20),
                                       random.uniform(20, SCREEN_HEIGHT-20)))
    registry.add_component(e, Velocity(random.uniform(-1, 1), random.uniform(-1, 1)))
    registry.add_component(e, Renderable(COLORS["HERBIVORE"], 4, "circle"))
    registry.add_component(e, Biological("HERBIVORE", HERBIVORE_MAX_ENERGY * 0.7,
                                          HERBIVORE_MAX_ENERGY, HERBIVORE_REPRODUCE_COST))
    registry.add_component(e, Genetics(
        max_speed=HERBIVORE_BASE_SPEED * random.uniform(0.9, 1.1),
        vision_radius=HERBIVORE_VISION * random.uniform(0.9, 1.1),
        strength=HERBIVORE_STRENGTH * random.uniform(0.8, 1.2),
        absorption_rate=HERBIVORE_ABSORPTION,
        size_factor=1.0,
        mutation_chance=MUTATION_CHANCE
    ))
    registry.add_component(e, Affiliation(species_id=1, lineage_id=lid))

def spawn_carnivore(registry):
    e = registry.create_entity()
    lid = next_lineage_id()
    registry.add_component(e, Position(random.uniform(20, SCREEN_WIDTH-20),
                                       random.uniform(20, SCREEN_HEIGHT-20)))
    registry.add_component(e, Velocity(random.uniform(-1, 1), random.uniform(-1, 1)))
    registry.add_component(e, Renderable(COLORS["CARNIVORE"], 6, "triangle"))
    registry.add_component(e, Biological("CARNIVORE", CARNIVORE_MAX_ENERGY * 0.6,
                                          CARNIVORE_MAX_ENERGY, CARNIVORE_REPRODUCE_COST))
    registry.add_component(e, Genetics(
        max_speed=CARNIVORE_BASE_SPEED * random.uniform(0.9, 1.1),
        vision_radius=CARNIVORE_VISION * random.uniform(0.9, 1.1),
        strength=CARNIVORE_STRENGTH * random.uniform(0.8, 1.2),
        absorption_rate=CARNIVORE_ABSORPTION,
        size_factor=1.0,
        mutation_chance=MUTATION_CHANCE
    ))
    registry.add_component(e, Affiliation(species_id=2, lineage_id=lid))

# ─── Rendering ───────────────────────────────────────────────────────

def render(screen, registry, font, debug_scent, scent_map):
    screen.fill(COLORS["BACKGROUND"])

    # Human zone
    surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    pygame.draw.circle(surf, COLORS["HUMAN_ZONE"], HUMAN_ZONE_CENTER, HUMAN_ZONE_RADIUS)
    screen.blit(surf, (0, 0))
    txt = font.render("Human City", True, COLORS["TEXT"])
    screen.blit(txt, (HUMAN_ZONE_CENTER[0] - txt.get_width()//2,
                       HUMAN_ZONE_CENTER[1] - txt.get_height()//2))

    # Debug scent heatmap
    if debug_scent and scent_map:
        scent_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        for c in range(scent_map.cols):
            for r in range(scent_map.rows):
                # Show herbivore scent (green) and carnivore scent (red)
                hv = min(200, int(scent_map.grid[1, c, r] * 3))
                cv = min(200, int(scent_map.grid[2, c, r] * 3))
                if hv > 2 or cv > 2:
                    pygame.draw.rect(scent_surf, (cv, hv, 0, max(hv, cv)),
                                     (c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        screen.blit(scent_surf, (0, 0))

    # Entities
    counts = {"PLANT": 0, "HERBIVORE": 0, "CARNIVORE": 0, "ANOMALY": 0,
              "FLEEING": 0, "STARVING": 0, "PACKS": set()}

    for entity in registry.view(Position, Renderable):
        pos = registry.get_component(entity, Position)
        ren = registry.get_component(entity, Renderable)
        bio = registry.get_component(entity, Biological)
        aff = registry.get_component(entity, Affiliation)

        if bio:
            counts[bio.diet_type] = counts.get(bio.diet_type, 0) + 1
            if bio.state == "FLEE":
                counts["FLEEING"] += 1
            if bio.state == "STARVING":
                counts["STARVING"] += 1
        if aff and aff.pack_id != -1:
            counts["PACKS"].add(aff.pack_id)

        if ren.is_anomaly:
            counts["ANOMALY"] += 1
            # Pulsing aura
            pulse = int(abs(math.sin(time.time() * 3)) * 60) + 40
            pygame.draw.circle(screen, (pulse, 0, pulse),
                               (int(pos.x), int(pos.y)), int(ren.size) + 6, 2)
            pygame.draw.circle(screen, COLORS["ANOMALY_OUTLINE"],
                               (int(pos.x), int(pos.y)), int(ren.size) + 3, 1)

        ix, iy = int(pos.x), int(pos.y)
        if ren.shape == "circle":
            pygame.draw.circle(screen, ren.color, (ix, iy), max(2, int(ren.size)))
        elif ren.shape == "rect":
            s = max(2, int(ren.size))
            pygame.draw.rect(screen, ren.color, (ix - s, iy - s, s*2, s*2))
        elif ren.shape == "triangle":
            s = max(3, int(ren.size))
            pts = [(ix, iy - s), (ix - s, iy + s), (ix + s, iy + s)]
            pygame.draw.polygon(screen, ren.color, pts)

    # HUD
    y = 8
    lines = [
        f"Plants: {counts['PLANT']}  |  Herbivores: {counts['HERBIVORE']}  |  "
        f"Carnivores: {counts['CARNIVORE']}",
        f"Anomalies: {counts['ANOMALY']}  |  Packs: {len(counts['PACKS'])}  |  "
        f"Fleeing: {counts['FLEEING']}  |  Starving: {counts['STARVING']}",
        "[D] Scent Debug  |  [+/-] Speed"
    ]
    for line in lines:
        txt = font.render(line, True, COLORS["TEXT"])
        screen.blit(txt, (8, y))
        y += 20

    return (counts["PLANT"], counts["HERBIVORE"], counts["CARNIVORE"],
            counts["ANOMALY"], len(counts["PACKS"]))

# ─── Main Loop ───────────────────────────────────────────────────────

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Guild Game Monster Simulator — Ecosystem Prototype")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("consolas", 16)

    registry = Registry()
    spatial_grid = SpatialHashGrid(SCREEN_WIDTH, SCREEN_HEIGHT, CELL_SIZE)
    scent_map = ScentMap(SCREEN_WIDTH, SCREEN_HEIGHT, CELL_SIZE)

    systems = [
        InteractionSystem(registry, spatial_grid, scent_map),
        BiologicalSystem(registry),
        PackSystem(registry, spatial_grid),
        MovementSystem(registry, scent_map),
    ]

    # Seed population
    for _ in range(MAX_PLANTS):
        spawn_plant(registry)
    for _ in range(STARTING_HERBIVORES):
        spawn_herbivore(registry)
    for _ in range(STARTING_CARNIVORES):
        spawn_carnivore(registry)

    running = True
    debug_scent = False
    sim_speed = 1

    report = {"start_time": time.time(), "snapshots": [], "events": []}
    frame = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    debug_scent = not debug_scent
                if event.key == pygame.K_PLUS or event.key == pygame.K_KP_PLUS:
                    sim_speed = min(5, sim_speed + 1)
                if event.key == pygame.K_MINUS or event.key == pygame.K_KP_MINUS:
                    sim_speed = max(1, sim_speed - 1)

        dt = FIXED_TIMESTEP * sim_speed
        scent_map.update()
        for s in systems:
            s.update(dt)

        plants, herbs, carns, anoms, packs = render(
            screen, registry, font, debug_scent, scent_map)

        # Plant regrowth (logistic: slower as we approach cap)
        if plants < MAX_PLANTS:
            growth_chance = PLANT_REGROW_CHANCE * (1.0 - plants / MAX_PLANTS)
            if random.random() < growth_chance:
                spawn_plant(registry)

        # Snapshot every second
        frame += 1
        if frame % FPS == 0:
            snap = {
                "time": frame // FPS,
                "plants": plants,
                "herbivores": herbs,
                "carnivores": carns,
                "anomalies": anoms,
                "packs": packs
            }
            report["snapshots"].append(snap)

        pygame.display.flip()
        clock.tick(FPS)

    # Save report
    report["end_time"] = time.time()
    report["duration_seconds"] = report["end_time"] - report["start_time"]
    with open("simulation_report.json", "w") as f:
        json.dump(report, f, indent=2)
    print("Report saved to simulation_report.json")

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
