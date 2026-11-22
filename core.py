import pygame
import sys
from config import WIDTH, HEIGHT, UI_HEIGHT, TARGET_FPS
from backend import plugins_registry, ISimulation
from renderer import Renderer
from input_handler import InputHandler

class Application:
    def __init__(self):
        pygame.init()
        pygame.key.set_repeat(500, 30)
        
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT + UI_HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption("Automata Lab Pro")
        self.clock = pygame.time.Clock()
        
        # Fonts
        self.font = pygame.font.SysFont("Consolas", 16)
        self.font_large = pygame.font.SysFont("Segoe UI", 20, bold=True)
        
        # Simulation Setup
        self.grid_w = 400
        self.grid_h = 400
        self.simulation: ISimulation = None
        self.plugin_names = list(plugins_registry.keys())
        self.plugin_idx = 0
        
        # Components
        self.renderer = Renderer(self.screen, self.grid_w, self.grid_h)
        self.input_handler = InputHandler(self)
        
        # State
        self.running = True
        self.paused = True
        self.sim_speed = 1
        self.input_active = False
        self.input_text = ""
        self.message = ""
        self.message_timer = 0
        
        self.load_plugin(0)

    def load_plugin(self, index):
        self.plugin_idx = index % len(self.plugin_names)
        name = self.plugin_names[self.plugin_idx]
        cls = plugins_registry[name]
        self.simulation = cls(self.grid_w, self.grid_h)
        self.simulation.reset()
        self.paused = True
        self.show_message(f"Loaded: {name}")

    def next_plugin(self):
        self.load_plugin(self.plugin_idx + 1)

    def clear_sim(self):
        self.simulation.clear()
        self.paused = True

    def show_message(self, msg, duration=2.0):
        self.message = msg
        self.message_timer = duration

    def update(self):
        if not self.paused:
            for _ in range(self.sim_speed):
                self.simulation.update()
        
        if self.message_timer > 0:
            self.message_timer -= 1 / TARGET_FPS

    def render(self):
        self.screen.fill(self.renderer.colors["bg"])
        
        # Detect if simulation is multi-state for coloring
        is_multi = self.plugin_names[self.plugin_idx] != "Conway's Life"
        self.renderer.render_grid(self.simulation.grid, is_multi)
        
        # UI Data
        ui_data = {
            'name': self.plugin_names[self.plugin_idx],
            'paused': self.paused,
            'speed': self.sim_speed,
            'gen': self.simulation.generation,
            'pop': self.simulation.population,
            'font': self.font,
            'font_large': self.font_large
        }
        
        self.renderer.render_ui(ui_data)
        self.renderer.render_message(self.message if self.message_timer > 0 else "", 
                                     self.font, self.input_active, self.input_text)
        
        pygame.display.flip()

    def run(self):
        while self.running:
            self.input_handler.process_events()
            self.update()
            self.render()
            self.clock.tick(TARGET_FPS)
        
        pygame.quit()
        sys.exit()
