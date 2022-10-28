import pygame
import sys
from scene import Scene
from shaders import Shaders
from model import Model
from camera import Camera
from event import EventHandler, handle_events, add_tick_listener
from OpenGL.GL import glClearColor, glCullFace, GL_BACK, glClear, GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT

TARGET_FRAMERATE = 120

class Application:
    def __init__(self, width, height):
        self.window_size = (width, height)
        self.shouldClose = False 
    
    @EventHandler(pygame.QUIT)
    def close(self, event, dt=0):
        self.shouldClose = True
        pygame.quit()
        sys.exit(0)
    
    def run(self):     
        glCullFace(GL_BACK)

        clock = pygame.time.Clock()
        
        scene = Scene(Shaders())
        scene.add_model("assets/models/bunny_world.obj")
        scene.create_camera(self.window_size[0], self.window_size[1])
        
        while not self.shouldClose:
            glClearColor(0.7, 0.1, 0.3, 1.0)
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
            handle_events(clock.tick(TARGET_FRAMERATE))
            
            scene.render()
            
            pygame.display.flip()
            