import pygame
import sys
from event import handle_events
from camera import Camera
from OpenGL.GL import glEnable, GL_DEPTH_TEST, glCullFace, glClearColor, glClear, GL_BACK, GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT

def run():
    glEnable(GL_DEPTH_TEST)
    glCullFace(GL_BACK)
    
    while pygame.get_init():
        glClearColor(0.01, 0.01, 0.01, 0.01);
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
        
        camera = Camera()
        
        pygame.display.flip()
        handle_events()
        
    sys.exit()
        