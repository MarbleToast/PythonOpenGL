import glm
import math
import random
from OpenGL.GL import *
from engine.object.camera import Camera
from engine.object.model import Model


class Scene:
    def __init__(self, path, perspective):
        self.path = path
        self.camera = Camera(position=glm.vec3(0, 10, 0))
        self.perspective = perspective
        self.objects = []
        self.light_direction = glm.vec3(0)
        
        self.setup()
        
    def setup(self):
        mountain = Model('resources/models/cube.json')
        cube = Model('resources/models/ball.json', texture_set="mountain")
                
        mountain.set_transforms([{
            "position": glm.vec3(5, random.gauss(-2, 0.2), 5),
            "rotation": glm.vec3(2),
            "scale": glm.vec3(2)
        }])
        
        cube.set_transforms([{
            "position": glm.vec3(0),
            "rotation": glm.vec3(),
            "scale": glm.vec3(0.5)
        },
        {
            "position": glm.vec3(10, 0, 10),
            "rotation": glm.vec3(),
            "scale": glm.vec3(0.5)
        }])
        
        self.add_object(cube)
        self.add_object(mountain)
        
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
        
        program.setVec3('directionalLight.direction', self.light_direction)
        program.setVec3("directionalLight.ambient", glm.vec3(0.05))
        program.setVec3("directionalLight.diffuse", glm.vec3(0.85));
        program.setVec3("directionalLight.specular", glm.vec3(1));
        
        program.setVec3("pointLights[0].position", glm.vec3(0));
        program.setVec3("pointLights[0].ambient", glm.vec3(0.4));
        program.setVec3("pointLights[0].diffuse", glm.vec3(0.85));
        program.setVec3("pointLights[0].specular", glm.vec3(1));
        program.setFloat("pointLights[0].constant", 2);
        program.setFloat("pointLights[0].linear", 0.2);
        program.setFloat("pointLights[0].quadratic", 0.064);
        
        program.setVec3("pointLights[1].position", glm.vec3(10, 0, 10));
        program.setVec3("pointLights[1].ambient", glm.vec3(0.05));
        program.setVec3("pointLights[1].diffuse", glm.vec3(0.85));
        program.setVec3("pointLights[1].specular", glm.vec3(1));
        program.setFloat("pointLights[1].constant", 1);
        program.setFloat("pointLights[1].linear", 0.09);
        program.setFloat("pointLights[1].quadratic", 0.032);

        for obj in self.objects:
            obj.draw(program)
        

