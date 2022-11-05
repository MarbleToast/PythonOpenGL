import engine.constants as constants
import glm

from math import sin, cos, radians

class SceneObject:
    def __init__(self, name: str, scene, position = None, rotation = None, scale = None):
        self.name = name
        
        if position == None:
            self.position = glm.vec3(0., 0., 0.)
        else:
            self.position = position

        if rotation == None:
            self.rotation = glm.vec2(0., 0.)
        else:
            self.rotation = rotation
            
        if scale == None:
            self.scale = glm.vec3(1., 1., 1.)
        else:
            self.scale = scale
            
        self.scene = scene
        self.front = glm.vec3(0., 0., -1.)
        self.update_vectors()
        
    def update_vectors(self):
        x = cos(radians(self.rotation.x)) * cos(radians(self.rotation.y))
        y = sin(radians(self.rotation.y))
        z = sin(radians(self.rotation.x)) * cos(radians(self.rotation.y))
        self.front = glm.normalize(glm.vec3(x, y, z))
        self.right = glm.normalize(glm.cross(self.front, constants.WORLD_UP))
        self.up = glm.normalize(glm.cross(self.right, self.front))