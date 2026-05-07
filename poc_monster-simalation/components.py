"""
ECS Components — Pure data containers for the ecosystem simulation.
Each component is a dataclass holding only data, no logic.
"""
from dataclasses import dataclass, field
import random

# ─── Spatial Components ──────────────────────────────────────────────

@dataclass
class Position:
    x: float
    y: float

@dataclass
class Velocity:
    vx: float
    vy: float

# ─── Rendering Component ─────────────────────────────────────────────

@dataclass
class Renderable:
    color: tuple
    size: float
    shape: str  # "circle", "rect", "triangle", "polygon"
    is_anomaly: bool = False

# ─── Biological Component ────────────────────────────────────────────

@dataclass
class Biological:
    diet_type: str          # "PLANT", "HERBIVORE", "CARNIVORE"
    energy: float
    max_energy: float
    reproduce_cost: float
    age: float = 0.0
    state: str = "WANDER"   # FSM states: WANDER, SEEK, FLEE, STARVING, REPRODUCE

    # Fitness tracking (for natural selection)
    kills: int = 0
    energy_absorbed: float = 0.0
    damage_taken: float = 0.0

    @property
    def fitness(self):
        """Fitness score: survival time + kills bonus - damage penalty."""
        return self.age + (self.kills * 10.0) + (self.energy_absorbed * 0.1) - (self.damage_taken * 0.5)

# ─── Genetics Component ──────────────────────────────────────────────

@dataclass
class Genetics:
    max_speed: float
    vision_radius: float
    strength: float
    absorption_rate: float      # How efficiently energy is extracted from food (0.5 to 1.5)
    size_factor: float          # Relative body size (affects rendering and combat)
    mutation_chance: float      # Base mutation probability per gene

    def mutate(self, amplitude=0.1):
        """
        Mutate each gene independently with the given amplitude.
        amplitude can be increased by the mutational meltdown system.
        """
        def _m(val):
            if random.random() < self.mutation_chance:
                return max(0.1, val * (1.0 + random.uniform(-amplitude, amplitude)))
            return val

        return Genetics(
            max_speed=_m(self.max_speed),
            vision_radius=_m(self.vision_radius),
            strength=_m(self.strength),
            absorption_rate=_m(self.absorption_rate),
            size_factor=_m(self.size_factor),
            mutation_chance=self.mutation_chance  # mutation_chance itself doesn't mutate
        )

    @staticmethod
    def crossover(parent_a, parent_b):
        """
        Sexual reproduction: for each gene, randomly pick from parent A or B
        with interpolation noise. This is the core of the genetic algorithm.
        """
        def _cross(va, vb):
            # Blend crossover with slight randomness
            t = random.uniform(0.3, 0.7)
            return va * t + vb * (1.0 - t)

        child = Genetics(
            max_speed=_cross(parent_a.max_speed, parent_b.max_speed),
            vision_radius=_cross(parent_a.vision_radius, parent_b.vision_radius),
            strength=_cross(parent_a.strength, parent_b.strength),
            absorption_rate=_cross(parent_a.absorption_rate, parent_b.absorption_rate),
            size_factor=_cross(parent_a.size_factor, parent_b.size_factor),
            mutation_chance=parent_a.mutation_chance
        )
        return child

# ─── Social Component ────────────────────────────────────────────────

@dataclass
class Affiliation:
    species_id: int         # Which species (1=herbivore, 2=carnivore, etc.)
    lineage_id: int = -1    # Family lineage (inherited from parent)
    pack_id: int = -1       # Current pack membership (-1 = solitary)
    is_alpha: bool = False   # Is this entity the alpha of its pack?
