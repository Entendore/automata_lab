import pygame
import numpy as np
from config import UI_HEIGHT, THEMES

class Renderer:
    def __init__(self, screen, grid_w: int, grid_h: int):
        self.screen = screen
        self.grid_w = grid_w
        self.grid_h = grid_h
        
        self.zoom = 1.0
        self.camera_x = 0
        self.camera_y = 0
        
        self.grid_surface = pygame.Surface((grid_w, grid_h))
        self.theme_name = "Default"
        self.colors = THEMES[self.theme_name]

    def set_theme(self, name: str):
        if name in THEMES:
            self.theme_name = name
            self.colors = THEMES[name]

    def render_grid(self, grid: np.ndarray, multi_state: bool = False):
        self.grid_surface.fill(self.colors["dead"])
        ys, xs = np.where(grid > 0)
        vals = grid[ys, xs]
        
        pixel_arr = pygame.surfarray.pixels3d(self.grid_surface)
        
        if not multi_state:
            pixel_arr[xs, ys] = self.colors["alive"]
        else:
            for y, x, v in zip(ys, xs, vals):
                c = self.colors["alive"] if v == 1 else (80, 80, 80) if v == 2 else self.colors["accent"]
                pixel_arr[x, y] = c
                
        del pixel_arr

        scaled_w = int(self.grid_w * self.zoom)
        scaled_h = int(self.grid_h * self.zoom)
        scaled_surface = pygame.transform.scale(self.grid_surface, (scaled_w, scaled_h))
        self.screen.blit(scaled_surface, (-self.camera_x, -self.camera_y))

    def render_ui(self, data: dict):
        h = self.screen.get_height()
        pygame.draw.rect(self.screen, self.colors["ui_bg"], (0, h - UI_HEIGHT, self.screen.get_width(), UI_HEIGHT))
        pygame.draw.line(self.screen, self.colors["ui_border"], (0, h - UI_HEIGHT), (self.screen.get_width(), h - UI_HEIGHT), 2)

        title = data['font_large'].render(f"{data['name']}", True, self.colors["accent"])
        self.screen.blit(title, (20, h - UI_HEIGHT + 15))
        
        mode = "PAUSED" if data['paused'] else f"RUNNING x{data['speed']}"
        state_col = (255, 100, 100) if data['paused'] else (100, 255, 100)
        stats = f"Gen: {data['gen']} | Pop: {data['pop']}"
        state_text = data['font'].render(f"{mode} | {stats} | Zoom: {self.zoom:.1f}x", True, state_col)
        self.screen.blit(state_text, (20, h - UI_HEIGHT + 38))

        help_text = data['font'].render("[N]ext  [R]andom  [C]lear  [Enter] Rule  [T]heme", True, (150, 150, 150))
        self.screen.blit(help_text, (self.screen.get_width() - 450, h - UI_HEIGHT + 20))

    def render_message(self, msg: str, font, input_active: bool = False, input_text: str = ""):
        if input_active:
            box = pygame.Rect(self.screen.get_width()//2 - 150, self.screen.get_height()//2 - 15, 300, 30)
            pygame.draw.rect(self.screen, (0,0,0), box)
            pygame.draw.rect(self.screen, self.colors["accent"], box, 2)
            txt_surf = font.render(input_text + "_", True, self.colors["text"])
            self.screen.blit(txt_surf, (box.x + 5, box.y + 5))
        elif msg:
            txt_surf = font.render(msg, True, self.colors["accent"])
            rect = txt_surf.get_rect(center=(self.screen.get_width()//2, self.screen.get_height()//2))
            pygame.draw.rect(self.screen, (0,0,0), rect.inflate(20, 10))
            self.screen.blit(txt_surf, rect)
