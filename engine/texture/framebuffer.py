import logging
from OpenGL.GL import *

"""
FrameBuffer

A wrapper for a framebuffer
"""
class FrameBuffer:
    def __init__(self):
        """
        Initialises by generating a frame buffer object

        Returns
        -------
        None.

        """
        logging.info("Creating framebuffer")
        self.FBO = glGenFramebuffers(1)
        
    def check_complete(self):
        """
        Checks to see if the frame buffer is complete.

        Raises
        ------
        RuntimeError
            If the framebuffer is incomplete.

        Returns
        -------
        None.

        """
        
        # Framebuffers can be incomplete when no texture is attached, or when
        # read/write buffers have not been set properly.
        if glCheckFramebufferStatus(GL_FRAMEBUFFER) != GL_FRAMEBUFFER_COMPLETE:
            raise RuntimeError("Error when creating framebuffer.")
            
        # Unbind the frame buffer regardless
        self.unbind()

    def get_id(self) -> int:
        """
        Returns reference to the framebuffer

        Returns
        -------
        int
            The framebuffer reference.

        """
        
        return self.FBO

    def bind(self):
        """
        Binds the framebuffer.

        Returns
        -------
        None.

        """
        
        glBindFramebuffer(GL_FRAMEBUFFER, self.FBO)

    def unbind(self):
        """
        Unbinds the framebuffer.

        Returns
        -------
        None.

        """
        
        glBindFramebuffer(GL_FRAMEBUFFER, 0)
    
    def __del__(self):
        """
        On all references descoped, delete the framebuffer object.

        Returns
        -------
        None.

        """
        
        try:
            glDeleteFramebuffers(1, self.FBO)
            self.FBO = 0
        except:
            pass
        