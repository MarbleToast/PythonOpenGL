import numpy as np
import pygame
from math import tan, radians
from game_object import GameObject, DEFAULT_POSITION

Z_NEAR = 0.1
Z_FAR = 1000

class Camera(GameObject):
    def __init__(self, position = DEFAULT_POSITION, field_of_view = 90., sensitivity = 1):
        super().__init__("Camera")
        self.field_of_view = field_of_view
        self.sensitivity = sensitivity
        self.transform.position = position
        
        self.update_vectors()
        
    def generate_frustrum(self):
        f = tan(radians(self.field_of_view)/2)
        win_size = pygame.display.get_window_size()
        aspect = win_size[0] / win_size[1]
        
        pers_matrix = np.empty((4, 4))
        pers_matrix[0][0] = 1 / (aspect * f)
        pers_matrix[1][1] = 1 / aspect
        pers_matrix[2][2] = -(Z_NEAR + Z_FAR)/(Z_NEAR - Z_FAR)
        pers_matrix[2][3] = -1
        pers_matrix[3][2] = -(2 * Z_NEAR * Z_FAR)/(Z_NEAR - Z_FAR)
        self.frustrum = pers_matrix
        
    def get_view(self):
        pass