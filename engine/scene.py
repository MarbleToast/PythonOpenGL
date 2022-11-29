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

"""
Scene

Holds all information on objects, how they update, and how to render them
"""
class Scene:
    def __init__(self):
        """
        Initialises all scene elements and properties.

        Returns
        -------
        None.

        """
        
        # Mouse information, to calculate offset in movement
        self.mouse_touched = False
        self.last_mouse_x = 0
        self.last_mouse_y = 0
        
        # Time information to pause and resume scene time
        self.pause_colour = False
        self.sky_colour = glm.vec3()
        self.ticks = 0
        
        # Initialise everything else
        self.initialise_skybox()
        self.initialise_lights()
        self.initialise_shadows()
        self.initialise_camera()
        self.initialise_objects()
        self.initialise_shaders()
        
    def initialise_skybox(self):
        """
        Initialise scene skybox.

        Returns
        -------
        None.

        """
        
        self.skybox = Skybox("negx.jpg", "posx.jpg", "posy.jpg", "negy.jpg", "negz.jpg", "posz.jpg")
        
    def initialise_lights(self):
        """
        Initialise scene global light position and point light position array.

        Returns
        -------
        None.

        """
        
        # Global light is pseudo-directional
        # It is a spot light without attenuation, allowing for easier shadows
        self.global_light_position = glm.vec3(0, 50, 0)
        self.point_light_positions = [glm.vec3(10, 0.75, 0)]
        
    def initialise_shadows(self):
        """
        Initialise shadow effect buffer wrapper.

        Returns
        -------
        None.

        """
        
        # Create shadows effect with global light
        self.shadows = ShadowsEffect(self.global_light_position)
        self.shadows.create()
        
    def initialise_camera(self):  
        """
        Initialise camera.

        Returns
        -------
        None.

        """
        
        # Camera given initial position
        self.camera = Camera(position=glm.vec3(0, 5, 0))
        
    def initialise_objects(self):
        """
        Initialise all objects in the scene.

        Returns
        -------
        None.

        """
        
        # Initialise empty object array
        self.objects = []
        
        # Floor cube
        cube = Model('resources/models/cube.json')
        
        # Central campfire
        campfire = Model(
            'resources/models/campfire.json',
            materials=[
                Material(
                    "campfire_diffuse.jpg",
                    normal_path="campfire_normal.jpg",
                    specular_path="campfire_specular.jpg",
                    displacement_path="campfire_depth.jpg",
                    shininess=0
                )
            ]
        )
        
        # Bamboo type 1
        plant = Model(
            "resources/models/bamboo1.json",
            materials=[
                Material(
                    "bamboo.png",
                    normal_path="bamboo_normal.png",
                    specular_path="bamboo_specular.png",
                    shininess=16
                ),
                Material(
                    "leaves.jpg",
                    specular_path="leaves_specular.jpg",
                    shininess=64
                )
            ]
        )
        
        # Bamboo type 2
        plant2 = Model(
            "resources/models/bamboo2.json",
            materials=[
                Material(
                    "bamboo.png",
                    normal_path="bamboo_normal.png",
                    specular_path="bamboo_specular.png",
                    shininess=8
                ),
                Material(
                    "leaves.jpg",
                    specular_path="leaves_specular.jpg",
                    shininess=32
                )
            ]
        )
        
        # Vines
        plant3 = Model(
            "resources/models/vines.json",
            materials=[
                Material(
                    "leaves.jpg",
                    specular_path="leaves_specular.jpg",
                    shininess=8
                )
            ]
        )
        
        # Bamboo type 3
        plant4 = Model(
            "resources/models/bamboo3.json",
            materials=[
                Material(
                    "bamboo.png",
                    normal_path="bamboo_normal.png",
                    specular_path="bamboo_specular.png",
                    shininess=8
                ),
                Material(
                    "leaves.jpg",
                    specular_path="leaves_specular.jpg",
                    shininess=32
                )
            ]
        )
        
        # Rock behind vines
        rock1 = Model(
            "resources/models/rock1.json",
            materials=[
                Material(
                    "rock_diffuse.png",
                    normal_path="rock_normal.png",
                    displacement_path="rock_depth.png",
                    specular_path="rock_specular.png",
                    shininess=8,
                    height_scale=0.1
                )
            ]
        )
        
        # Rock type 2
        rock2 = Model(
            "resources/models/rock2.json",
            materials=[
                Material(
                    "rock_diffuse.png",
                    normal_path="rock_normal.png",
                    displacement_path="rock_depth.png",
                    specular_path="rock_specular.png",
                    shininess=8
                )
            ]
        )
        
        # Splined elephant (no texture coords in model)
        elephant = Model(
            "resources/models/elephant.json",
            materials=[
                Material(
                    "cube.jpg",
                    shininess=8
                )
            ]
        )
       
        # In a square, generate positions according to a wiggly function
        positions = []
        for i in range(-20, 20):
            for j in range(-20, 20):
                positions.append(
                    glm.vec3(
                        i, 
                        -0.143*math.sin(1.75*(i + 1.73)) - 0.180*math.sin(2.96*(i+4.98)) 
                            - 0.012*math.sin(6.23*(j+3.17)) + 0.288*math.sin(8.07*(j+i+4.63)),
                        j
                    )
                )
               
        # Set floor cube transforms to these positions
        cube.set_transforms([
            {"position": pos, "rotation": glm.vec3(), "scale": glm.vec3(1)} for pos in positions
        ])
        
        # Set vine transforms to along the left-hand side with random offsets
        plant3.set_transforms([
            {
                "position": glm.vec3(z-random.random(), 10-random.random()*2, -15),
                "rotation": glm.vec3(0.5, 0, 0),
                "scale": glm.vec3(0.1)
            }
            for z in range(-20, 24, 4)
        ])
        
        # Set rock to be behind the vines
        rock1.set_transforms([
            {"position": glm.vec3(0, 7, -25) , "rotation": glm.vec3(), "scale": glm.vec3(3, 2, 1)}
        ])
        
        # Set rock 2 to be on right hand side, in two positions
        rock2.set_transforms([
            {"position": glm.vec3(0, 7, 25) , "rotation": glm.vec3(0, 1.5, 0.8), "scale": glm.vec3(2, 1.6, 1)},
            {"position": glm.vec3(-10, 3, 25) , "rotation": glm.vec3(0, 0, 0.8), "scale": glm.vec3(1.5, 1, 1.1)},
        ])
        
        # Set bamboo type 1 across front side of scene, with random rotations
        plant.set_transforms([
            {
                "position": glm.vec3(20, 0, z-random.random()),
                "rotation": glm.vec3(
                    random.random()*360,
                    random.random()/2,
                    random.random()
                ),
                "scale": glm.vec3(0.07)
            }
            for z in range(-20, 24, 2)
        ])
        
        # Set bamboo type 1 across front side of scene, with random rotations
        plant2.set_transforms([
            {
                "position": glm.vec3(18, 0, z+random.random()*2),
                "rotation": glm.vec3(
                    random.random()*360,
                    random.random()/2,
                    0
                ),
                "scale": glm.vec3(0.03)
            }
            for z in range(-19, 21, 3)
        ])
        
        # Set bamboo type 3 across back side of scene, with random rotations
        plant4.set_transforms([
            {
                "position": glm.vec3(-20, 0, z-random.random()),
                "rotation": glm.vec3(
                    random.random()*360,
                    random.random()/2,
                    random.random()
                ),
                "scale": glm.vec3(0.04)
            }
            for z in range(-20, 24, 2)
        ])
        
        # Set campfire transforms (offset position due to model)
        campfire.set_transforms([
            {"position": self.point_light_positions[0]-glm.vec3(0, 0, 1), "rotation": glm.vec3(), "scale": glm.vec3(0.05)}
        ])
        
        # Add all models to render array
        self.objects.append(cube)
        self.objects.append(campfire)
        self.objects.append(plant)
        self.objects.append(plant2)
        self.objects.append(plant3)
        self.objects.append(rock1)
        self.objects.append(rock2)
        self.objects.append(plant4)
        self.objects.append(elephant)
        
    def initialise_shaders(self):
        """
        Initialise all shaders

        Returns
        -------
        None.

        """
        
        self.lighting_program = ShaderProgram('resources/shaders/vertex.vs', 'resources/shaders/fragment.fs')
        self.shadow_program = ShaderProgram('resources/shaders/depth_vertex.vs', 'resources/shaders/depth_fragment.fs')
        self.skybox_program = ShaderProgram('resources/shaders/skybox_vertex.vs', 'resources/shaders/skybox_fragment.fs')
        
    def mouse_callback(self, x: int, y: int):
        """
        Calculate delta of mouse position, and rotate camera by that

        Parameters
        ----------
        x : int
            New horizontal mouse position.
        y : int
            New vertical mouse position.

        Returns
        -------
        None.

        """
        
        # If we haven't yet moved the mouse, set the positions
        if not self.mouse_touched:
            self.last_mouse_x = x
            self.last_mouse_y = y
            self.mouse_touched = True
            
        # Calculate offset
        x_offset = x - self.last_mouse_x
        y_offset = self.last_mouse_y - y
        
        # Set previous mouse positions to this after calculating offset
        self.last_mouse_x = x
        self.last_mouse_y = y

        # Rotate camera by offset
        self.camera.rotate(x_offset, y_offset)
        
    def key_callback(self, key: int, action: int):
        """
        Callback for scene wide inputs.

        Parameters
        ----------
        key : int
            Key of the event.
        action : int
            Event type happening with the key.

        Returns
        -------
        None.

        """
        
        # Press P to pause time
        if key == glfw.KEY_P and action == glfw.PRESS:
            self.pause_colour = not self.pause_colour
            
        # Press L when paused to turn on full bright
        if key == glfw.KEY_L and action == glfw.PRESS:
            self.sky_colour = glm.vec3(1)
        
    def update(self, window, dt: float):
        """
        Update logic of scene objects. No rendering takes place here.

        Parameters
        ----------
        window : GLFWWindow
            The window we are hosted in.
        dt : float
            Delta time, the time passed since last cycle.

        Returns
        -------
        None.

        """
        
        # If we haven't paused...
        if not self.pause_colour:
            # Advance time
            self.ticks += 0.1
            
            # Move global light
            self.global_light_position.z = 20 * math.sin(self.ticks) * dt
            self.global_light_position.y = 20 * math.cos(self.ticks) * dt
            
            # Move campfire light in a small circle to 'flicker'
            self.point_light_positions[0].x += dt*math.sin(self.ticks*1000)
            self.point_light_positions[0].z += dt*math.cos(self.ticks*1000)
            
            # Update the light space matrix
            self.shadows.update_light_space_matrix(self.global_light_position)
            
            # Change the sky colour between night and day
            self.sky_colour = glm.vec3(math.sin(self.ticks) * 0.5, 0, math.cos(self.ticks) * 0.5)
            
            # Move elephant back and forward
            self.objects[8].set_transforms([
                {"position": glm.vec3(-9, 7, 12), "rotation": glm.vec3(180, 0.5*math.sin(self.ticks)*dt, 0), "scale": glm.vec3(4)}
            ])
        
        # Update camera
        self.camera.update(window, dt)
        
    def draw(self):
        """
        Draw all objects in scene

        Returns
        -------
        None.

        """
        
        # Clear buffer bits, colour sky according to time
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glClearColor(self.sky_colour.x, self.sky_colour.y, self.sky_colour.z, 1.0)
        
        # Draw skybox first, using camera to get view and projection matrices
        # Make sure to remove translation data from view matrix
        self.skybox_program.use()
        self.skybox_program.setMat4("view", glm.mat4(glm.mat3(self.camera.get_view())))
        self.skybox_program.setMat4("projection", self.camera.get_perspective(CONFIG['window_width'], CONFIG['window_height']))
        self.skybox.draw(self.skybox_program)
        
        # Start shadow pass.
        # The main shadows can be seen on the left-hand side of the scene as 
        # the light passes behind the right-hand rocks.
        self.shadows.start(self.shadow_program)
        for obj in self.objects:
            obj.draw(self.shadow_program)
        self.shadows.end(self.lighting_program)
        
        # Assign uniforms of main lighting program
        self.lighting_program.setMat4('viewProject', self.camera.get_perspective(CONFIG['window_width'], CONFIG['window_height']) * self.camera.get_view())
        self.lighting_program.setVec3('viewPos', self.camera.position)
        
        # Global light moves, and uses sky colour as light colour
        self.lighting_program.setVec3('globalLight.position', self.global_light_position)
        self.lighting_program.setVec3("globalLight.ambient", self.sky_colour*glm.vec3(0.2))
        self.lighting_program.setVec3("globalLight.diffuse", self.sky_colour)
        self.lighting_program.setVec3("globalLight.specular", glm.vec3(0))
        
        # Point light 0 is the campfire. Deep orange, bright, and flickers in 
        # diffuse intensity randomly.
        self.lighting_program.setVec3("pointLights[0].position", self.point_light_positions[0])
        self.lighting_program.setVec3("pointLights[0].ambient", glm.vec3(0.886, 0.345, 0.133))
        self.lighting_program.setVec3("pointLights[0].diffuse", glm.vec3(0.886, 0.345, 0.133)*random.gauss(1, 0.2))
        self.lighting_program.setVec3("pointLights[0].specular", glm.vec3(1))
        self.lighting_program.setFloat("pointLights[0].constant", 0.2)
        self.lighting_program.setFloat("pointLights[0].linear", 0.02)
        self.lighting_program.setFloat("pointLights[0].quadratic", 0.016)
        
        # The lighting shader computes the sum of all point lights in the array
        # This could be improved by using a uniform buffer object, to both
        # improve performance and surpass limits of array sizes in GLSL.
        
        # To add more lights, change the NUM_POINT_LIGHTS macro in the lighting
        # shader and define here.
        
        # self.lighting_program.setVec3("pointLights[1].position", self.point_light_positions[1])
        # self.lighting_program.setVec3("pointLights[1].ambient", glm.vec3(0.886, 0.345, 0.133))
        # self.lighting_program.setVec3("pointLights[1].diffuse", glm.vec3(0.886, 0.345, 0.133))
        # self.lighting_program.setVec3("pointLights[1].specular", glm.vec3(1))
        # self.lighting_program.setFloat("pointLights[1].constant", 1)
        # self.lighting_program.setFloat("pointLights[1].linear", 0.09)
        # self.lighting_program.setFloat("pointLights[1].quadratic", 0.032)

        # Finally, draw all objects in lighting pass.
        for obj in self.objects:
            obj.draw(self.lighting_program)
            
        
        
        
