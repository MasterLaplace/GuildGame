"""
Global configuration for the ecosystem simulation.
All biological constants are tuned to produce stable Lotka-Volterra oscillations.

Key design principle: the 10% trophic efficiency rule.
A carnivore must consume ~4 herbivores to reproduce.
An herbivore must consume ~3 plants to reproduce.
This creates the natural population pyramid.
"""
import pygame

# ─── Screen Settings ─────────────────────────────────────────────────
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 900
FPS = 60
FIXED_TIMESTEP = 1.0 / FPS

# ─── Spatial Settings ────────────────────────────────────────────────
CELL_SIZE = 40  # Size of cells for spatial hashing and scent map

# ─── Colors ──────────────────────────────────────────────────────────
COLORS = {
    "BACKGROUND": (20, 22, 28),
    "PLANT": (50, 180, 50),
    "HERBIVORE": (80, 220, 120),
    "CARNIVORE": (220, 60, 60),
    "ANOMALY": (180, 0, 255),
    "ANOMALY_OUTLINE": (255, 200, 255),
    "HUMAN_ZONE": (80, 120, 220, 60),
    "DEBUG_GRID": (40, 40, 50),
    "TEXT": (220, 220, 220),
    "TEXT_WARN": (255, 200, 80),
    "PACK_LINE": (255, 255, 100, 40),
}

# ─── Initial Population ─────────────────────────────────────────────
MAX_PLANTS = 350
STARTING_HERBIVORES = 80
STARTING_CARNIVORES = 12

# ─── Plant Settings ─────────────────────────────────────────────────
PLANT_ENERGY = 25.0
PLANT_REGROW_CHANCE = 0.05  # Chance per frame to spawn a new plant (if below cap)
PLANT_SCENT_AMOUNT = 5.0     # Scent emitted by plants (attracts herbivores)

# ─── Herbivore Settings (r-strategist) ───────────────────────────────
# Fast reproduction, low cost, short life.
HERBIVORE_MAX_ENERGY = 80.0
HERBIVORE_REPRODUCE_COST = 50.0   # Must eat ~2 plants (2*25=50) to reproduce
HERBIVORE_BASE_SPEED = 45.0
HERBIVORE_VISION = 60.0
HERBIVORE_STRENGTH = 5.0
HERBIVORE_ABSORPTION = 1.0
HERBIVORE_ENERGY_DRAIN = 3.0      # Energy lost per second

# ─── Carnivore Settings (K-strategist) ───────────────────────────────
# Slow reproduction, high cost, long life.
CARNIVORE_MAX_ENERGY = 250.0
CARNIVORE_REPRODUCE_COST = 200.0  # Must eat ~4 herbivores (4*50=200) to reproduce
CARNIVORE_BASE_SPEED = 65.0
CARNIVORE_VISION = 120.0
CARNIVORE_STRENGTH = 25.0
CARNIVORE_ABSORPTION = 0.8
CARNIVORE_EAT_ENERGY = 50.0      # Energy gained per herbivore kill
CARNIVORE_ENERGY_DRAIN = 2.0      # Energy lost per second (slower metabolism)

# ─── Carrying Capacity ──────────────────────────────────────────────
# Maximum number of entities of the same species within a local radius.
# Reproduction is blocked if local density exceeds this.
CARRYING_CAPACITY_RADIUS = 150.0
CARRYING_CAPACITY_HERBIVORE = 15   # Max herbivores within radius
CARRYING_CAPACITY_CARNIVORE = 5    # Max carnivores within radius

# ─── Genetics & Evolution ────────────────────────────────────────────
MUTATION_CHANCE = 0.08              # Base chance per gene to mutate
MUTATION_AMPLITUDE = 0.12           # Normal mutation: +/- 12%
MELTDOWN_POP_THRESHOLD = 4          # If local population < this, meltdown activates
MELTDOWN_MUTATION_AMPLITUDE = 0.5   # Meltdown mutation: +/- 50% (chaotic)
MELTDOWN_MUTATION_CHANCE = 0.4      # Meltdown: 40% chance per gene

# ─── Anomaly / Boss Detection ────────────────────────────────────────
# An entity becomes an Anomaly if any of its genes exceed
# the population mean + ANOMALY_SIGMA_THRESHOLD * standard_deviation.
ANOMALY_SIGMA_THRESHOLD = 2.5
ANOMALY_SIZE_MULTIPLIER = 2.5
ANOMALY_TERROR_SCENT = 80.0

# ─── Scent Map Channels ─────────────────────────────────────────────
# 0: Plant scent       (attracts herbivores)
# 1: Herbivore scent   (attracts carnivores)
# 2: Carnivore scent   (repels herbivores)
# 3: Boss terror scent (repels everyone)
SCENT_CHANNELS = 4
SCENT_DECAY = 0.92
SCENT_DIFFUSION = 0.08

# ─── Pack Dynamics ───────────────────────────────────────────────────
PACK_FORMATION_RADIUS = 80.0    # Carnivores within this range can form packs
PACK_MAX_SIZE = 8               # Above this, pack splits (budding)
PACK_DISSOLUTION_CHANCE = 0.6   # Chance of dissolution when alpha dies

# ─── Combat ──────────────────────────────────────────────────────────
EAT_RANGE = 12.0                # Distance to consume food
COMBAT_RANGE = 15.0             # Distance for melee combat

# ─── Human Zone ──────────────────────────────────────────────────────
HUMAN_ZONE_CENTER = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
HUMAN_ZONE_RADIUS = 110
HUMAN_ZONE_REPULSION = 6.0
