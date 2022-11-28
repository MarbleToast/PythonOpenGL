import glm
from OpenGL.GL import *
from engine.texture.framebuffer import FrameBuffer
from engine.texture.depthbuffer import DepthBuffer
from engine.config import CONFIG

class ShadowsEffect:
    def __init__(self, light_position):
        self.update_light_space_matrix(light_position)
    
    def update_light_space_matrix(self, light_position):
        projection = glm.perspective(45, CONFIG["shadow_width"]/CONFIG["shadow_height"], CONFIG["near_plane"], CONFIG["far_plane"])
        view = glm.lookAt(light_position, glm.vec3(0), glm.vec3(0, 1, 0))
        self.light_space_matrix = projection * view

    def create(self):
        self.depth_buffer = DepthBuffer()
        self.frame_buffer = FrameBuffer()
        
        # Bind FBO
        self.frame_buffer.bind()
        
        # Create depth buffer texture
        self.depth_buffer.generate(CONFIG["shadow_width"], CONFIG["shadow_height"])
        
        # Attach depth buffer texture to framebuffer
        self.depth_buffer.attach()
        
        # Check for errors
        self.frame_buffer.check_complete()

    def start(self, program):  
        self.frame_buffer.bind()
        glViewport(0, 0, CONFIG["shadow_width"], CONFIG["shadow_height"])
        glClear(GL_DEPTH_BUFFER_BIT)
        program.use()
        program.setMat4('lightSpaceMatrix', self.light_space_matrix)
        
    def end(self, program):
        self.frame_buffer.unbind()
        glViewport(0, 0, CONFIG["window_width"], CONFIG["window_height"])
        glClear(GL_DEPTH_BUFFER_BIT | GL_COLOR_BUFFER_BIT)
        
        program.use()
        glActiveTexture(GL_TEXTURE10)
        self.depth_buffer.bind()
        
        program.setMat4('lightSpaceMatrix', self.light_space_matrix)
        program.setInt('shadowMap', 10)