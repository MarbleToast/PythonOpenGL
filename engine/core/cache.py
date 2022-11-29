import logging
from engine.texture.texture import Texture
from OpenGL.GL import GL_TEXTURE_2D

# Textures can and should be reused between materials. Therefore we use a 
# texture cache to hold pointers to preloaded textures.

TEXTURE_CACHE = {}

def get_or_load_texture(path: str):
    """
    Load a texture, or fetch reference if already loaded

    Parameters
    ----------
    path : str
        The path to the texture.

    Returns
    -------
    Texture
        The texture instance.

    """
    
    logging.info(f"Loading {path}")
    if not path in TEXTURE_CACHE.keys():
        TEXTURE_CACHE[path] = Texture(GL_TEXTURE_2D, path)
    
    return TEXTURE_CACHE[path]
