import pygame
import logging
import display
from app import Application

def pre_init():
    if not pygame.init():
        logging.error("Pygame could not initialise.")
        
def main():
    pre_init()
    display.init_display(640, 480)
    app = Application(640, 480)
    app.run()
        
if __name__ == "__main__":
    main()