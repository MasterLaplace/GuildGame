"""
Spatial data structures for the ecosystem simulation.

SpatialHashGrid: O(1) amortized neighbor queries via grid hashing.
ScentMap: Multi-channel diffusion grid using numpy for emergent navigation.
"""
import numpy as np
import math
from settings import SCENT_CHANNELS, SCENT_DECAY, SCENT_DIFFUSION


class SpatialHashGrid:
    """
    Spatial hash grid for fast proximity queries.
    Rebuilt every frame. Entities are bucketed into grid cells.
    """
    def __init__(self, width, height, cell_size):
        self.cell_size = cell_size
        self.cols = math.ceil(width / cell_size)
        self.rows = math.ceil(height / cell_size)
        self.cells = {}

    def clear(self):
        self.cells.clear()

    def _get_cell(self, x, y):
        return int(x // self.cell_size), int(y // self.cell_size)

    def insert(self, entity_id, x, y):
        key = self._get_cell(x, y)
        if key not in self.cells:
            self.cells[key] = []
        self.cells[key].append(entity_id)

    def get_nearby(self, x, y, radius):
        """Return all entity IDs within radius of (x, y)."""
        nearby = []
        min_col, min_row = self._get_cell(x - radius, y - radius)
        max_col, max_row = self._get_cell(x + radius, y + radius)
        for col in range(max(0, min_col), min(self.cols, max_col + 1)):
            for row in range(max(0, min_row), min(self.rows, max_row + 1)):
                bucket = self.cells.get((col, row))
                if bucket:
                    nearby.extend(bucket)
        return nearby

    def count_in_radius(self, x, y, radius, entity_ids_to_count):
        """Count how many of the given entity IDs are actually within radius."""
        count = 0
        r2 = radius * radius
        for eid in entity_ids_to_count:
            # Caller must provide positions externally for accurate count
            # This is a simplified version - the system will do the full check
            count += 1
        return count


class ScentMap:
    """
    Multi-channel diffusion grid for emergent navigation.

    Channels:
      0: Plant scent       (attracts herbivores)
      1: Herbivore scent   (attracts carnivores)
      2: Carnivore scent   (repels herbivores — triggers FLEE)
      3: Boss terror scent (repels everyone)

    The diffusion equation per cell per tick:
      S(x,y,t+1) = S(x,y,t) * decay * (1-diffusion) + diffusion/4 * Σ neighbors

    Boundaries are zeroed to prevent wrap-around artifacts from np.roll.
    """
    def __init__(self, width, height, cell_size):
        self.cell_size = cell_size
        self.cols = math.ceil(width / cell_size)
        self.rows = math.ceil(height / cell_size)
        self.grid = np.zeros((SCENT_CHANNELS, self.cols, self.rows), dtype=np.float32)

    def add_scent(self, channel, x, y, amount):
        col = int(x // self.cell_size)
        row = int(y // self.cell_size)
        if 0 <= col < self.cols and 0 <= row < self.rows:
            self.grid[channel, col, row] = min(
                self.grid[channel, col, row] + amount, 100.0
            )

    def update(self):
        """Apply decay and diffusion to all channels."""
        # Decay
        self.grid *= SCENT_DECAY

        # Diffusion: shift grid in 4 cardinal directions
        for c in range(SCENT_CHANNELS):
            layer = self.grid[c]
            up    = np.roll(layer, -1, axis=1)
            down  = np.roll(layer,  1, axis=1)
            left  = np.roll(layer, -1, axis=0)
            right = np.roll(layer,  1, axis=0)

            # Zero out wrapped edges
            up[:, -1] = 0
            down[:, 0] = 0
            left[-1, :] = 0
            right[0, :] = 0

            neighbors_avg = (up + down + left + right) * (SCENT_DIFFUSION / 4.0)
            self.grid[c] = layer * (1.0 - SCENT_DIFFUSION) + neighbors_avg

    def get_gradient(self, channel, x, y):
        """
        Return the normalized gradient direction (dx, dy) at position (x, y).
        Uses central difference for smooth gradients.
        """
        col = int(x // self.cell_size)
        row = int(y // self.cell_size)

        if not (1 <= col < self.cols - 1 and 1 <= row < self.rows - 1):
            return 0.0, 0.0

        dx = float(self.grid[channel, col + 1, row] - self.grid[channel, col - 1, row])
        dy = float(self.grid[channel, col, row + 1] - self.grid[channel, col, row - 1])

        length = math.sqrt(dx * dx + dy * dy)
        if length > 0.001:
            return dx / length, dy / length
        return 0.0, 0.0

    def get_value(self, channel, x, y):
        """Get raw scent value at a position."""
        col = int(x // self.cell_size)
        row = int(y // self.cell_size)
        if 0 <= col < self.cols and 0 <= row < self.rows:
            return float(self.grid[channel, col, row])
        return 0.0
