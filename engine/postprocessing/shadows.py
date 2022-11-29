import glm
from OpenGL.GL import *
from engine.texture.framebuffer import FrameBuffer
from engine.texture.depthbuffer import DepthBuffer
from engine.core.program import ShaderProgram
from engine.config import CONFIG

"""
ShadowsEffect

Handles shadow casting and updating the light space matrix
"""
class ShadowsEffect:
    def __init__(self, light_position: glm.vec3):
        """
        Initialises the effect by creating the light space matrix

        Parameters
        ----------
        light_position : glm.vec3
            Current position of shadow-casting light

        Returns
        -------
        None.

        """
        
        self.update_light_space_matrix(light_position)
    
    def update_light_space_matrix(self, light_position: glm.vec3):
        """
        Updates the light space matrix for use in shadow calculations.

        Parameters
        ----------
        light_position : glm.vec3
            The position of the shadow-casting light

        Returns
        -------
        None.

        """
        
        # Generate view and projection matrices from the light's perspective
        # looking towards the centre of the scene. Importantly, the aspect
        # ratio of the shadows are not of the screen height, but the shadow
        # resolution.
        projection = glm.perspective(45, CONFIG["shadow_width"]/CONFIG["shadow_height"], CONFIG["near_plane"], CONFIG["far_plane"])
        view = glm.lookAt(light_position, glm.vec3(0), glm.vec3(0, 1, 0))
        self.light_space_matrix = projection * view

    def create(self):
        """
        Create the depth and frame buffers, and attachs the generated depth
        buffer to the frame buffer.

        Returns
        -------
        None.

        """
        
        # Generate depth and frame bufferss
        self.depth_buffer = DepthBuffer()
        self.frame_buffer = FrameBuffer()
        
        # Bind FBO
        self.frame_buffer.bind()
        
        # Create depth buffer texture with shadow resolution from config
        self.depth_buffer.generate(CONFIG["shadow_width"], CONFIG["shadow_height"])
        
        # Attach depth buffer texture to framebuffer
        self.depth_buffer.attach()
        
        # Check for errors
        self.frame_buffer.check_complete()

    def start(self, program: ShaderProgram):  
        """
        Begin shadow pass

        Parameters
        ----------
        program : ShaderProgram
            The depth shader program

        Returns
        -------
        None.

        """
        
        # Bind the frame buffer with depth buffer attached
        self.frame_buffer.bind()
        
        # Set the viewport to the size of the shadow resolution
        glViewport(0, 0, CONFIG["shadow_width"], CONFIG["shadow_height"])
        
        # Clear the depth buffer bit
        glClear(GL_DEPTH_BUFFER_BIT)
        
        # Use the depth program and set its light space matrix uniform
        program.use()
        program.setMat4('lightSpaceMatrix', self.light_space_matrix)
        
    def end(self, program: ShaderProgram):
        """
        Finish shadow pass

        Parameters
        ----------
        program : ShaderProgram
            The lighting program to switch to after shadow pass

        Returns
        -------
        None.

        """
        
        
        # Unbind the frame buffer
        self.frame_buffer.unbind()
        
        # Reset the viewport to window size
        glViewport(0, 0, CONFIG["window_width"], CONFIG["window_height"])
        
        # Clear both colour and depth buffer bits
        glClear(GL_DEPTH_BUFFER_BIT | GL_COLOR_BUFFER_BIT)
        
        # Use the new shader program for lighting pass
        program.use()
        
        # Set the 10th texture unit to the depth buffer's shadow map texture
        glActiveTexture(GL_TEXTURE10)
        self.depth_buffer.bind()
        
        # Set the uniforms in the lighting shader for light space matrix and
        # shadow map unit
        program.setMat4('lightSpaceMatrix', self.light_space_matrix)
        program.setInt('shadowMap', 10)
        