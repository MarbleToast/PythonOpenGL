from OpenGL.GL import (
    glGenTextures,
    glTexImage2D,
    GL_TEXTURE_2D,
    GL_RGBA,
    GL_UNSIGNED_BYTE,
    glGenerateMipmap,
    glTexParameteri,
    GL_TEXTURE_WRAP_S,
    GL_REPEAT,
    GL_TEXTURE_WRAP_T,
    GL_TEXTURE_MIN_FILTER,
    GL_LINEAR_MIPMAP_LINEAR,
    GL_TEXTURE_MAG_FILTER,
    GL_LINEAR,
    glBindTexture,
    glDeleteTextures
)
from OpenGL.error import NullFunctionError
from PIL import Image

class Texture:
    def __init__(self, path, type):
        self.path = path
        self.type = type
        self.texture = glGenTextures(1)
        self.load()
        
    def load(self):
        self.bind()
        image = Image.open(f"resources/textures/{self.path}")
        image = image.transpose(Image.FLIP_TOP_BOTTOM)
        image_bytes = image.convert('RGBA').tobytes()
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image.width, image.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, image_bytes)

        glGenerateMipmap(GL_TEXTURE_2D)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    
    def getId(self):
        return self.texture
    
    def bind(self):
        glBindTexture(self.type, self.texture)

    def unbind(self):
        glBindTexture(self.type, 0)

    def __del__(self):
        try:
            glDeleteTextures(1, self.texture)
            self.texture = 0
        except (NullFunctionError, TypeError):
            pass
