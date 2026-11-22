import numpy as np
import re
from .base import ISimulation, register_plugin

@register_plugin("Conway's Life")
class ConwayLife(ISimulation):
    def __init__(self, width, height):
        super().__init__(width, height)
        self.birth = {3}
        self.survive = {2, 3}

    def parse_custom_rule(self, rule_str: str) -> bool:
        try:
            match = re.match(r'B(\d*)/S(\d*)', rule_str.replace(" ", ""))
            if match:
                self.birth = set(int(c) for c in match.group(1))
                self.survive = set(int(c) for c in match.group(2))
                return True
        except:
            pass
        return False

    def update(self):
        p = np.pad(self.grid, 1, mode='wrap')
        
        neighbors = (
            p[0:-2, 0:-2] + p[0:-2, 1:-1] + p[0:-2, 2:] +
            p[1:-1, 0:-2] +                   p[1:-1, 2:] +
            p[2:,   0:-2] + p[2:,   1:-1] + p[2:,   2:]
        )
        
        b_mask = np.isin(neighbors, list(self.birth))
        s_mask = np.isin(neighbors, list(self.survive))
        
        dead = self.grid == 0
        alive = self.grid == 1
        
        new_grid = np.zeros_like(self.grid)
        new_grid[dead & b_mask] = 1
        new_grid[alive & s_mask] = 1
        
        self.grid = new_grid
        self.generation += 1
        self.population = np.sum(self.grid)
