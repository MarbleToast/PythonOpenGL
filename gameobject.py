# -*- coding: utf-8 -*-
"""
Created on Thu Oct 20 15:25:01 2022

@author: jrbra
"""
from model import Model
from math import sin, cos, radians
from transform import Transform, GLOBAL_UP
from pygame.math import Vector3

class GameObject:
    def __init__(self, name: str, scene, transform = Transform(), model_filename = None):
        self.name = name
        self.transform = transform
        self.scene = scene
        self.front = Vector3(0., 0., -1.)
        self.parent = None
        self.update_vectors()
        if model_filename is not None:
            self.model = Model(model_filename, self)
            
    def update(self, event, dt):
        print(self.transform, self.name)
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