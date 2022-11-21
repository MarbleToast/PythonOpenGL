import glm
import math
from OpenGL.GL import *
from engine.object.camera import Camera
from engine.object.model import Model


class Scene:
    def __init__(self, path, perspective):
        self.path = path
        self.camera = Camera(position=glm.vec3(0, 10, 0))
        self.perspective = perspective
        self.objects = []
        
        self.setup()
        
    def setup(self):
        cube = Model('resources/models/cube.json')
        
        positions = []
        for i in range(-3, 3):
            for j in range(-3, 3):
                positions.append(glm.vec3(i*3, 0, j*3))
                
        cube.set_transforms([{"position": pos, "rotation": glm.vec3(), "scale": glm.vec3(3, 0.5, 3)} for pos in positions])
        self.add_object(cube)
        
    def add_object(self, object):
        self.objects.append(object)
        
    def update(self, window, dt):
        self.camera.update(window, dt)
        
    def draw(self, program):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glClearColor(0.4, 0.2, 0.4, 1)
        
        program.use()
        program.setMat4('viewProject', self.perspective * self.camera.get_view())
        program.setVec3('viewPos', self.camera.position)
        program.setVec3('light.direction', glm.vec3(-0.2, -1.0, -0.3))

        for obj in self.objects:
            obj.draw(program)
        

