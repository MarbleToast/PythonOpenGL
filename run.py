import pygame
from display import initialise_display
from world import run

def pre_init() -> None:
    pygame.init()
    pygame.display.init()

def init() -> None:
    pre_init()
    initialise_display(640, 480)
    run()
    
if __name__ == "__main__":
    init()