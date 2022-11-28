import glm
import glfw
import math
import random
from OpenGL.GL import *
from engine.object.camera import Camera
from engine.object.model import Model
from engine.config import CONFIG
from engine.postprocessing.shadows import ShadowsEffect
from engine.core.program import ShaderProgram
from engine.texture.skybox import Skybox
from engine.texture.material import Material

class Scene:
    def __init__(self, path):
        self.path = path
        self.mouse_touched = False
        self.last_mouse_x = 0
        self.last_mouse_y = 0
        
        self.initialise_skybox()
        self.initialise_lights()
        self.initialise_shadows()
        self.initialise_camera()
        self.initialise_objects()
        self.initialise_shaders()
        
    def initialise_skybox(self):
        self.skybox = Skybox("negx.jpg", "posx.jpg", "posy.jpg", "negy.jpg", "negz.jpg", "posz.jpg")
        
    def initialise_lights(self):
        self.global_light_position = glm.vec3(0, 50, 0)
        self.point_light_positions = [glm.vec3(0, 5, 0), glm.vec3(0, 5, 0)]
        
    def initialise_shadows(self):
        self.shadows = ShadowsEffect(self.global_light_position)
        self.shadows.create()
        
    def initialise_camera(self):  
        self.camera = Camera(position=glm.vec3(0, 0, 0))
        
    def initialise_objects(self):
        self.objects = []
        
        cube = Model('resources/models/cube.json')
        ball = Model('resources/models/ball.json')
        plant = Model("resources/models/plant.json", material=Material("plant", "plant.png", normal_path="plant_normal.png"))
       
        positions = []
        for i in range(-10, 10):
            for j in range(-10, 10):
                positions.append(glm.vec3(i*3, random.gauss(0, 0.2), j*3))
               
        cube.set_transforms([{"position": pos, "rotation": glm.vec3(), "scale": glm.vec3(3, 0.5, 3)} for pos in positions])
        plant.set_transforms([{"position": glm.vec3(5, 5, 0), "rotation": glm.vec3(), "scale": glm.vec3(1)}])
        
        self.objects.append(cube)
        self.objects.append(ball)
        self.objects.append(plant)
        
    def initialise_shaders(self):
        self.lighting_program = ShaderProgram('resources/shaders/vertex.vs', 'resources/shaders/fragment.fs')
        self.shadow_program = ShaderProgram('resources/shaders/depth_vertex.vs', 'resources/shaders/depth_fragment.fs')
        
        self.skybox_program = ShaderProgram('resources/shaders/skybox_vertex.vs', 'resources/shaders/skybox_fragment.fs')
        self.skybox_program.use()
        self.skybox_program.setInt("skybox", 0)
        
    def mouse_callback(self, x, y):
        if not self.mouse_touched:
            self.last_mouse_x = x
            self.last_mouse_y = y
            self.mouse_touched = True
            
        x_offset = x - self.last_mouse_x
        y_offset = self.last_mouse_y - y
        
        self.last_mouse_x = x
        self.last_mouse_y = y

        self.camera.rotate(x_offset, y_offset)
        
    def key_callback(self, key, action):
        pass
        
    def update(self, window, dt):
        time = glfw.get_time()
        self.global_light_position.z = math.sin(time)
        self.objects[1].set_transforms([{"position": glm.vec3(math.sin(time) * dt, 5, math.cos(time) * dt), "rotation": glm.vec3(), "scale": glm.vec3(1)}])
        
        self.shadows.update_light_space_matrix(self.global_light_position)
        self.camera.update(window, dt)
        
    def draw(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glClearColor(0.431, 0.161, 0.204, 1.0)
        
        self.shadows.start(self.shadow_program)
        for obj in self.objects:
            obj.draw(self.shadow_program)
        self.shadows.end(self.lighting_program)
        
        # Assign uniforms of main shader program
        self.lighting_program.setMat4('viewProject', self.camera.get_perspective(CONFIG['window_width'], CONFIG['window_height']) * self.camera.get_view())
        self.lighting_program.setVec3('viewPos', self.camera.position)
        
        self.lighting_program.setVec3('globalLight.position', self.global_light_position)
        self.lighting_program.setVec3("globalLight.ambient", glm.vec3(0.08, 0.05, 0.05))
        self.lighting_program.setVec3("globalLight.diffuse", glm.vec3(0.8))
        self.lighting_program.setVec3("globalLight.specular", glm.vec3(1))
        
        self.lighting_program.setVec3("pointLights[0].position", self.point_light_positions[0])
        self.lighting_program.setVec3("pointLights[0].ambient", glm.vec3(0.886, 0.345, 0.133))
        self.lighting_program.setVec3("pointLights[0].diffuse", glm.vec3(0.886, 0.345, 0.133))
        self.lighting_program.setVec3("pointLights[0].specular", glm.vec3(1))
        self.lighting_program.setFloat("pointLights[0].constant", 1)
        self.lighting_program.setFloat("pointLights[0].linear", 0.09)
        self.lighting_program.setFloat("pointLights[0].quadratic", 0.032)
        
        self.lighting_program.setVec3("pointLights[1].position", self.point_light_positions[1])
        self.lighting_program.setVec3("pointLights[1].ambient", glm.vec3(0.886, 0.345, 0.133))
        self.lighting_program.setVec3("pointLights[1].diffuse", glm.vec3(0.886, 0.345, 0.133))
        self.lighting_program.setVec3("pointLights[1].specular", glm.vec3(1))
        self.lighting_program.setFloat("pointLights[1].constant", 1)
        self.lighting_program.setFloat("pointLights[1].linear", 0.09)
        self.lighting_program.setFloat("pointLights[1].quadratic", 0.032)

        for obj in self.objects:
            obj.draw(self.lighting_program)
            
        self.skybox_program.use()
        self.skybox_program.setMat4("view", glm.mat4(glm.mat3(self.camera.get_view())))
        self.skybox_program.setMat4("projection", self.camera.get_perspective(CONFIG['window_width'], CONFIG['window_height']))

        
        
