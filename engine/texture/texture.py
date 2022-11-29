import os
from OpenGL.GL import *
from PIL import Image

"""
Texture

Loads and holds reference to texture
"""
class Texture:
    def __init__(self, type: int, path: str = None):
        """
        Generates a texture object, and, if supplied a path (and if the texture
        is standalone), loads the texture.

        Parameters
        ----------
        type : int
            The type of the texture object.
        path : str, optional
            The path to the texture file. The default is None.

        Raises
        ------
        RuntimeError
            If the texture file does not exist at the given path.

        Returns
        -------
        None.

        """
        
        if path and not os.path.exists(f"resources/textures/{path}"):
            raise RuntimeError(f'Texture file {path} does not exist.')
            
        # Generate a texture object
        self.type = type
        self.texture = glGenTextures(1)
        
        # For depthbuffers and cube maps, we do not want to load a texture
        if path and type == GL_TEXTURE_2D:
            self.load(path)
        
    def load(self, path: str):
        """
        Loads texture from file.

        Parameters
        ----------
        path : str
            The path to the image for the texture.

        Returns
        -------
        None.

        """
        
        # Bind texture object
        self.bind()
        
        # Load image
        image = Image.open(f"resources/textures/{path}")
        
        # Flip for OpenGL
        image = image.transpose(Image.FLIP_TOP_BOTTOM)
        
        # Convert image to bytes and pass as data for texture object
        image_bytes = image.convert('RGBA').tobytes()
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image.width, image.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, image_bytes)

        # Generate mipmaps for performant distance rendering
        glGenerateMipmap(GL_TEXTURE_2D)
        
        # Set parameters to repeat on edge and to set magnification function
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    
    def get_id(self) -> int:
        """
        Gets texture reference.

        Returns
        -------
        int
            The texture reference.

        """
        
        return self.texture
    
    def bind(self):
        """
        Binds the texture object to the type.

        Returns
        -------
        None.

        """
        
        glBindTexture(self.type, self.texture)

    def unbind(self):
        """
        Unbinds the texture of this type.

        Returns
        -------
        None.

        """
        
        glBindTexture(self.type, 0)

    def __del__(self):
        """
        On all references descoped, delete texture object.

        Returns
        -------
        None.

        """
        
        try:
            glDeleteTextures(1, self.texture)
            self.texture = 0
        except:
            pass
