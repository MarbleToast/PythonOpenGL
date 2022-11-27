import glm
from OpenGL.GL import *
from engine.texture.framebuffer import FrameBuffer
from engine.texture.depthbuffer import DepthBuffer

class ShadowsEffect:
    def __init__(self, light_position, z_near, z_far):
        self.update_light_space_matrix(light_position, z_near, z_far)
    
    def update_light_space_matrix(self, light_position, z_near, z_far):
        projection = glm.ortho(-10, 10, -10, 10, z_near, z_far)
        view = glm.lookAt(light_position, glm.vec3(0), glm.vec3(0, 1, 0))
        self.light_space_matrix = projection * view

    def create(self, width, height):
        self.width = width
        self.height = height
        self.depth_buffer = DepthBuffer()
        self.frame_buffer = FrameBuffer()
        
        # Bind FBO
        self.frame_buffer.bind()
        
        # Create depth buffer texture
        self.depth_buffer.generate(width, height)
        
        # Attach depth buffer texture to framebuffer
        self.depth_buffer.attach()
        
        # Check for errors
        self.frame_buffer.check_complete()

    def start(self, program):
        glDisable(GL_CULL_FACE)
        
        program.use()
        print(self.light_space_matrix)
        program.setMat4('lightSpaceMatrix', self.light_space_matrix)
        glViewport(0, 0, self.width, self.height)
        self.frame_buffer.bind()
        glClear(GL_DEPTH_BUFFER_BIT)
        
    def end(self, program):
        self.frame_buffer.unbind()
        program.use()
        program.setMat4('lightSpaceMatrix', self.light_space_matrix)
        program.setInt('shadowMap', 10)
        glActiveTexture(GL_TEXTURE10)
        self.depth_buffer.bind()
        
        glEnable(GL_CULL_FACE)

    def __del__(self):
        del self.frame_buffer
        del self.depth_buffer