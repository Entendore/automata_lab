import numpy as np
from .base import ISimulation, register_plugin

@register_plugin("Brian's Brain")
class BriansBrain(ISimulation):
    """3-state cyclic automaton: Off -> On -> Dying -> Off"""
    def __init__(self, width, height):
        super().__init__(width, height)

    def parse_custom_rule(self, rule_str: str) -> bool:
        return False # Fixed rules

    def reset(self, density=0.1):
        # States: 0=Off, 1=On, 2=Dying
        self.grid = np.random.choice([0, 1, 2], size=(self.height, self.width), p=[1-density, density, 0])
        self.generation = 0

    def update(self):
        p = np.pad(self.grid, 1, mode='wrap')
        
        # Count only ON neighbors (state 1)
        neighbors_on = (
            (p[0:-2, 0:-2] == 1) + (p[0:-2, 1:-1] == 1) + (p[0:-2, 2:] == 1) +
            (p[1:-1, 0:-2] == 1) +                            (p[1:-1, 2:] == 1) +
            (p[2:,   0:-2] == 1) + (p[2:,   1:-1] == 1) + (p[2:,   2:] == 1)
        )
        
        new_grid = np.zeros_like(self.grid)
        
        # Off (0) -> On (1) if exactly 2 neighbors are On
        new_grid[(self.grid == 0) & (neighbors_on == 2)] = 1
        
        # On (1) -> Dying (2)
        new_grid[self.grid == 1] = 2
        
        # Dying (2) -> Off (0) (handled by initialization)
        
        self.grid = new_grid
        self.generation += 1
        self.population = np.sum(self.grid == 1)
