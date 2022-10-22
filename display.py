import pygame
from event import EventHandler
from OpenGL.GL import glBlendFunc, GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA, glViewport, glEnable, GL_CULL_FACE, GL_BLEND, GL_DEPTH_TEST, glEnableClientState, GL_VERTEX_ARRAY


def init_display(width, height):
    flags = pygame.OPENGL | pygame.DOUBLEBUF
        
    pygame.display.set_mode(
        (width, height),
        flags
    )
    
    glEnable(GL_CULL_FACE)
    glEnable(GL_BLEND)
    glEnable(GL_DEPTH_TEST)
    glEnableClientState(GL_VERTEX_ARRAY)
    
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
    
    glViewport(0, 0, width, height)
    
@EventHandler(pygame.WINDOWRESIZED)
def resize_callback(event, dt):
    size = pygame.display.get_window_size()
    glViewport(0, 0, size[0], size[1])
    
