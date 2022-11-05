from engine.texture.texture import Texture
from OpenGL.GL import GL_TEXTURE_2D

TEXTURE_CACHE = {}

def get_or_load_texture(path: str):
    if path in TEXTURE_CACHE.keys():
        return TEXTURE_CACHE[path]
    
    TEXTURE_CACHE[path] = Texture(path, GL_TEXTURE_2D)
    return TEXTURE_CACHE[path]
