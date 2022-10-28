from pygame.math import Vector3, Vector2

GLOBAL_UP = Vector3(0., 1., 0.)
DEFAULT_POSITION = Vector3(0., 0., 0.)
DEFAULT_ROTATION = Vector2(-90., 0.)
DEFAULT_SCALE = Vector3(1., 1., 1.)

class Transform:
    def __init__(self, position = DEFAULT_POSITION, rotation = DEFAULT_ROTATION, scale = DEFAULT_SCALE):
        self.position = position
        self.rotation = rotation
        self.scale = scale
        
    def __repr__(self):
        return f"[{self.position}, {self.rotation}, {self.scale}]"