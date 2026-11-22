from .base import ISimulation, plugins_registry, register_plugin

# Import concrete implementations to trigger registration
from . import conway
from . import brians_brain

__all__ = ['ISimulation', 'plugins_registry', 'register_plugin']
