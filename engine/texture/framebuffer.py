from OpenGL.GL import *

class FrameBuffer:
    def __init__(self):
        self.FBO = glGenFramebuffers(1)
        
    def check_complete(self):
        if glCheckFramebufferStatus(GL_FRAMEBUFFER) != GL_FRAMEBUFFER_COMPLETE:
            raise RuntimeError("Error when creating framebuffer.")
        self.unbind()

    def get_id(self):
        return self.FBO

    def bind(self):
        glBindFramebuffer(GL_FRAMEBUFFER, self.FBO)

    def unbind(self):
        glBindFramebuffer(GL_FRAMEBUFFER, 0)
    
    def __del__(self):
        try:
            glDeleteFramebuffers(1, self.FBO)
            self.FBO = 0
        except:
            pass
        