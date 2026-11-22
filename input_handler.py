import pygame
import time
import os

class InputHandler:
    def __init__(self, app):
        self.app = app
        self.dragging = False
        self.last_mouse_pos = (0, 0)
        self.brush_size = 1
        self.draw_value = 1 # 1=Alive, 0=Dead

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.app.running = False
            
            if self.app.input_active:
                self._handle_text_input(event)
                continue
            
            if event.type == pygame.KEYDOWN:
                self._handle_keydown(event)
            elif event.type == pygame.MOUSEWHEEL:
                self._handle_scroll(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._handle_mouse_down(event)
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 2: self.dragging = False
            elif event.type == pygame.MOUSEMOTION:
                self._handle_motion(event)

    def _handle_text_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if hasattr(self.app.simulation, 'parse_custom_rule'):
                    success = self.app.simulation.parse_custom_rule(self.app.input_text)
                    msg = f"Rule Set: {self.app.input_text}" if success else "Invalid Rule Format"
                    self.app.show_message(msg)
                self.app.input_active = False
            elif event.key == pygame.K_ESCAPE:
                self.app.input_active = False
            else:
                self.app.input_text += event.unicode

    def _handle_keydown(self, event):
        if event.key == pygame.K_SPACE: self.app.paused = not self.app.paused
        elif event.key == pygame.K_n: self.app.next_plugin()
        elif event.key == pygame.K_c: self.app.clear_sim()
        elif event.key == pygame.K_r: self.app.simulation.reset()
        elif event.key == pygame.K_t: self.app.renderer.set_theme("Matrix" if self.app.renderer.theme_name == "Default" else "Default")
        elif event.key == pygame.K_UP: self.app.sim_speed = min(20, self.app.sim_speed + 1)
        elif event.key == pygame.K_DOWN: self.app.sim_speed = max(1, self.app.sim_speed - 1)
        elif event.key == pygame.K_LEFTBRACKET: self.brush_size = max(1, self.brush_size - 1)
        elif event.key == pygame.K_RIGHTBRACKET: self.brush_size = min(20, self.brush_size + 1)
        elif event.key == pygame.K_ENTER: 
            self.app.input_active = True
            self.app.input_text = ""
            self.app.show_message("Enter Rule (e.g. B3/S23):")
        elif event.key == pygame.K_F12: self._screenshot()

    def _handle_scroll(self, event):
        zoom_factor = 1.1 if event.y > 0 else 0.9
        self.app.renderer.zoom *= zoom_factor
        self.app.renderer.zoom = max(0.5, min(10.0, self.app.renderer.zoom))

    def _handle_mouse_down(self, event):
        if event.button == 2:
            self.dragging = True
            self.last_mouse_pos = event.pos
        elif event.button == 1: self.draw_value = 1
        elif event.button == 3: self.draw_value = 0

    def _handle_motion(self, event):
        if self.dragging:
            dx = self.last_mouse_pos[0] - event.pos[0]
            dy = self.last_mouse_pos[1] - event.pos[1]
            self.app.renderer.camera_x += dx
            self.app.renderer.camera_y += dy
            self.last_mouse_pos = event.pos
        
        if pygame.mouse.get_pressed()[0] or pygame.mouse.get_pressed()[2]:
            self._paint(event.pos)

    def _paint(self, pos):
        mx, my = pos
        wx = int((mx + self.app.renderer.camera_x) / self.app.renderer.zoom)
        wy = int((my + self.app.renderer.camera_y) / self.app.renderer.zoom)
        self.app.simulation.draw(wx, wy, self.brush_size, self.draw_value)

    def _screenshot(self):
        if not os.path.exists("screenshots"): os.makedirs("screenshots")
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        pygame.image.save(self.app.screen, f"screenshots/automata_{timestamp}.png")
        self.app.show_message("Screenshot Saved")
