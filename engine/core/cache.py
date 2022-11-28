# import numpy as np
from engine.texture.texture import Texture
# from engine.texture.material import Material
from OpenGL.GL import GL_TEXTURE_2D

# Textures can and should be reused between materials

TEXTURE_CACHE = {}

def get_or_load_texture(path: str):
    if not path in TEXTURE_CACHE.keys():
        TEXTURE_CACHE[path] = Texture(GL_TEXTURE_2D, path)
    
    return TEXTURE_CACHE[path]
