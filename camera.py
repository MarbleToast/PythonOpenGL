import numpy as np
import pygame
from math import tan, radians
from gameobject import GameObject, DEFAULT_POSITION

Z_NEAR = 0.1
Z_FAR = 1000

class Camera(GameObject):
    def __init__(self, viewport_width, viewport_height, position = DEFAULT_POSITION, field_of_view = 90., sensitivity = 1):
        super().__init__("Camera")
        
        self.viewport_width = viewport_width
        self.viewport_height = viewport_height

        self.field_of_view = field_of_view
        self.sensitivity = sensitivity
        self.transform.position = position
        
        self.movement_speed = 500
        
        self.update_vectors()
        
    def generate_frustrum(self):
        f = tan(radians(self.field_of_view)/2)
        aspect = self.viewport_width / self.viewport_height
        
        pers_matrix = np.empty((4, 4))
        pers_matrix[0][0] = 1 / (aspect * f)
        pers_matrix[1][1] = 1 / aspect
        pers_matrix[2][2] = -(Z_NEAR + Z_FAR)/(Z_NEAR - Z_FAR)
        pers_matrix[2][3] = -1
        pers_matrix[3][2] = -(2 * Z_NEAR * Z_FAR)/(Z_NEAR - Z_FAR)
        self.frustrum = pers_matrix
        
    def update(self, event, dt):
        velocity = self.movement_speed * (dt / 100)
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.transform.position += self.right * velocity
        if keys[pygame.K_d]:
            self.transform.position -= self.right * velocity
        if keys[pygame.K_w]:
            self.transform.position += self.front * velocity
        if keys[pygame.K_s]:
            self.transform.position -= self.front * velocity
            
        super().update(event)
            
    def get_view(self):
        pass