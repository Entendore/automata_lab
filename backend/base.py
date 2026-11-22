from abc import ABC, abstractmethod
import numpy as np
from typing import Dict, Type

# ==========================================
# PLUGIN REGISTRY SYSTEM
# ==========================================

plugins_registry: Dict[str, Type['ISimulation']] = {}

def register_plugin(name: str):
    """
    Decorator to register a simulation class.
    Usage: @register_plugin("MySimName")
    """
    def decorator(cls: Type['ISimulation']):
        plugins_registry[name] = cls
        return cls
    return decorator

# ==========================================
# ABSTRACT BASE CLASS
# ==========================================

class ISimulation(ABC):
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.grid = np.zeros((height, width), dtype=np.uint8)
        self.generation = 0
        self.population = 0

    @abstractmethod
    def update(self):
        """Advance simulation by one step."""
        pass

    @abstractmethod
    def parse_custom_rule(self, rule_str: str) -> bool:
        """Try to parse a rule string (optional). Return True if successful."""
        pass

    def reset(self, density: float = 0.2):
        self.grid = (np.random.random((self.height, self.width)) < density).astype(np.uint8)
        self.generation = 0

    def clear(self):
        self.grid.fill(0)
        self.generation = 0

    def draw(self, x: int, y: int, size: int, value: int):
        """Draw a circle onto the grid."""
        if size <= 1:
            if 0 <= x < self.width and 0 <= y < self.height:
                self.grid[y, x] = value
        else:
            # Create a circular mask
            y_coords, x_coords = np.ogrid[-size:size+1, -size:size+1]
            mask = x_coords**2 + y_coords**2 <= size**2
            
            # Calculate bounds
            y_min, y_max = max(0, y - size), min(self.height, y + size + 1)
            x_min, x_max = max(0, x - size), min(self.width, x + size + 1)
            
            # Align mask to grid slice
            mask_y_min = size - (y - y_min)
            mask_y_max = size + (y_max - y)
            mask_x_min = size - (x - x_min)
            mask_x_max = size + (x_max - x)
            
            valid_mask = mask[mask_y_min:mask_y_max, mask_x_min:mask_x_max]
            self.grid[y_min:y_max, x_min:x_max][valid_mask] = value
