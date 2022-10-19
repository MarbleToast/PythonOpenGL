import pygame
from event import register_handler
        
def initialise_display(width: int, height: int):
    flags = pygame.OPENGL | pygame.DOUBLEBUF
        
    pygame.display.set_mode(
        (width, height),
        flags
    )

@register_handler(pygame.QUIT)
def on_close(event):
    pygame.quit()
    