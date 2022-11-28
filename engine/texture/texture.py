from OpenGL.GL import *
from PIL import Image

class Texture:
    def __init__(self, type, path = None):
        self.type = type
        self.texture = glGenTextures(1)
        if path:
            self.load(path)
        
    def load(self, path):
        if self.type == GL_TEXTURE_2D:
            self.bind()
            image = Image.open(f"resources/textures/{path}")
            image = image.transpose(Image.FLIP_TOP_BOTTOM)
            image_bytes = image.convert('RGBA').tobytes()
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image.width, image.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, image_bytes)
    
            glGenerateMipmap(GL_TEXTURE_2D)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    
    def get_id(self):
        return self.texture
    
    def bind(self):
        glBindTexture(self.type, self.texture)

    def unbind(self):
        glBindTexture(self.type, 0)

    def __del__(self):
        try:
            glDeleteTextures(1, self.texture)
            self.texture = 0
        except:
            pass
