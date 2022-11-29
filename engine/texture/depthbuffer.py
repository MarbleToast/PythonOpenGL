import logging
from OpenGL.GL import *
from engine.texture.texture import Texture

"""
DepthBuffer

Inherits from Texture.
Holds and generates shadow map texture
"""
class DepthBuffer(Texture):
    def __init__(self):
        """
        Initialises Texture superclass constructor with 2D texture type

        Returns
        -------
        None.

        """
        
        logging.info("Creating depthbuffer")
        super().__init__(GL_TEXTURE_2D)

    def generate(self, width: int, height: int):
        """
        Binds and generates 2D texture for shadow map.

        Parameters
        ----------
        width : int
            Horizontal shadow resolution.
        height : int
            Vertical shadow resolution.

        Returns
        -------
        None.

        """
        
        # Bind shadow map texture
        self.bind()
        
        # Specify texture with clamped depth format, width, and height
        glTexImage2D(GL_TEXTURE_2D, 0, GL_DEPTH_COMPONENT, width, height, 0, GL_DEPTH_COMPONENT, GL_FLOAT, None)
        
        # Sets texture magnification function
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        
        # Clamp shadows to border to keep shadows constrained properly to
        # perspective.
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_BORDER)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_BORDER)
        glTexParameterfv(GL_TEXTURE_2D, GL_TEXTURE_BORDER_COLOR, [1.0, 1.0, 1.0, 1.0])
        
        # Unbind texture
        self.unbind()

    def attach(self):
        """
        Attachs current shadow map texture to the framebuffer.

        Returns
        -------
        None.

        """
        
        # Attach texture to bound framebuffer
        glFramebufferTexture2D(GL_FRAMEBUFFER, GL_DEPTH_ATTACHMENT, GL_TEXTURE_2D, self.get_id(), 0)
        
        # Set read/write buffers to none, as we aren't rendering any colour
        # data
        glDrawBuffer(GL_NONE)
        glReadBuffer(GL_NONE)