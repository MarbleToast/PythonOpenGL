# -*- coding: utf-8 -*-
"""
Created on Thu Oct 20 15:25:01 2022

@author: jrbra
"""

from math import sin, cos, radians

from types import SimpleNamespace
from pygame.math import Vector3, Vector2

GLOBAL_UP = Vector3(0., 1., 0.)
DEFAULT_POSITION = Vector3(0., 0., 0.)
DEFAULT_ROTATION = Vector2(-90., 0.)
DEFAULT_SCALE = Vector3(1., 1., 1.)

Transform = SimpleNamespace(
    position = DEFAULT_POSITION,
    rotation = DEFAULT_ROTATION,
    scale = DEFAULT_SCALE
)

class GameObject:
    def __init__(self, name: str, transform: Transform = Transform, model = None):
        self.name = name
        self.transform = transform
        self.model = model
        self.front = Vector3(0., 0., -1.)
        self.parent = None
        self.update_vectors()
        
    def update(self, event):
        self.update_vectors()
        
    def update_vectors(self):
        temp = Vector3(
            cos(radians(self.transform.rotation.x)) * cos(radians(self.transform.rotation.y)),
            sin(radians(self.transform.rotation.y)),
            sin(radians(self.transform.rotation.x)) * cos(radians(self.transform.rotation.y))
        )
        self.front = temp.normalize()
        self.right = GLOBAL_UP.cross(self.front).normalize()
        self.up = self.front.cross(self.right)