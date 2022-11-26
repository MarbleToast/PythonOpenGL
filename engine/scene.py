import glm
import glfw
import math
import random
from OpenGL.GL import *
from engine.object.camera import Camera
from engine.object.model import Model
from engine.config import config
from engine.postprocessing.shadows import ShadowsEffect

class Scene:
    def __init__(self, path, perspective):
        self.path = path
        self.camera = Camera(position=glm.vec3(0, 10, 0))
        self.perspective = perspective
        self.objects = []
        self.light_direction = glm.vec3(0, 1, 0)
        self.ticks = 0
        
        self.point_light_positions = [
            glm.vec3(-20, 2, -10),
        ]
        
        self.shadows = ShadowsEffect(self.point_light_positions[0], config['near_plane'], config['far_plane'])
        
        self.setup()
        
    def setup(self):
       cube = Model('resources/models/cube.json')
       ball = Model('resources/models/ball.json')
       
       positions = []
       for i in range(-10, 10):
           for j in range(-10, 10):
               positions.append(glm.vec3(i*3, random.gauss(-2, 1), j*3))
               
       cube.set_transforms([{"position": pos, "rotation": glm.vec3(), "scale": glm.vec3(3, 5, 3)} for pos in positions])
       ball.set_transforms([{"position": pos, "rotation": glm.vec3(), "scale": glm.vec3(1)} for pos in self.point_light_positions])
       self.add_object(cube)
       self.add_object(ball)
       
       self.shadows.create(1024, 1024)
        
    def add_object(self, object):
        self.objects.append(object)
        
    def update(self, window, dt):
        self.ticks += 0.1
        self.point_light_positions = [glm.vec3(10 * math.sin(self.ticks)*dt, 2, 10), glm.vec3(10, 2, 10 * math.sin(self.ticks)*dt)]
        self.point_light_positions[0].z = math.sin(glfw.get_time()*0.1) * 2
        self.objects[1].set_transforms([{"position": pos, "rotation": glm.vec3(), "scale": glm.vec3(1)} for pos in self.point_light_positions])
        
        self.shadows.update_light_space_matrix(self.point_light_positions[0], config['near_plane'], config['far_plane'])
        self.camera.update(window, dt)
        
    def draw(self, main_program, depth_program):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glClearColor(0.4, 0.2, 0.4, 1)
        
        self.shadows.start(depth_program)
        for obj in self.objects:
            obj.draw(depth_program)
        self.shadows.end(main_program)
        
        glViewport(0, 0, config['window_width'], config['window_height'])
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        # Assign uniforms of main shader program
        main_program.use()
        main_program.setMat4('viewProject', self.perspective * self.camera.get_view())
        main_program.setVec3('viewPos', self.camera.position)
        
        main_program.setVec3('directionalLight.direction', self.light_direction)
        main_program.setVec3("directionalLight.ambient", glm.vec3(0.1, 0.345, 0.133))
        main_program.setVec3("directionalLight.diffuse", glm.vec3(0.35))
        main_program.setVec3("directionalLight.specular", glm.vec3(0.5))
        
        main_program.setVec3("pointLights[0].position", self.point_light_positions[0])
        main_program.setVec3("pointLights[0].ambient", glm.vec3(0.886, 0.345, 0.133))
        main_program.setVec3("pointLights[0].diffuse", glm.vec3(0.886, 0.345, 0.133))
        main_program.setVec3("pointLights[0].specular", glm.vec3(1))
        main_program.setFloat("pointLights[0].constant", 1)
        main_program.setFloat("pointLights[0].linear", 0.09)
        main_program.setFloat("pointLights[0].quadratic", 0.032)
        
        main_program.setVec3("pointLights[1].position", self.point_light_positions[1])
        main_program.setVec3("pointLights[1].ambient", glm.vec3(0.886, 0.345, 0.133))
        main_program.setVec3("pointLights[1].diffuse", glm.vec3(0.886, 0.345, 0.133))
        main_program.setVec3("pointLights[1].specular", glm.vec3(1))
        main_program.setFloat("pointLights[1].constant", 1)
        main_program.setFloat("pointLights[1].linear", 0.09)
        main_program.setFloat("pointLights[1].quadratic", 0.032)

        for obj in self.objects:
            obj.draw(main_program)
        

