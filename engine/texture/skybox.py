import glm
import numpy as np
from PIL import Image
from OpenGL.GL import *
from engine.texture.texture import Texture
from engine.object.model import Model
from engine.core.program import ShaderProgram

"""
Skybox

Inherits from Texture.
Loads, holds, and draws cubemap texture on cube model
"""
class Skybox(Texture):
    def __init__(self, right:str, left:str, top:str, bottom:str, back:str, front:str):
        """
        Calls Texture superclass constructor, loads cube model, and loads cube
        map.

        Parameters
        ----------
        right : str
            The path to the right cube texture
        left : str
            The path to the left cube texture.
        top : str
            The path to the top cube texture.
        bottom : str
            The path to the bottom cube texture.
        back : str
            The path to the back cube texture.
        front : str
            The path to the front cube texture.

        Returns
        -------
        None.

        """
        
        # Call Texture constructor with cube map type
        super().__init__(GL_TEXTURE_CUBE_MAP)
        
        # Load a basic cube model to apply the cube map to
        self.model = Model("resources/models/cube.json")
        
        # Load cube map from paths
        self.faces = [right, left, top, bottom, back, front]
        self.load_cube_map()
        
    def load_cube_map(self):
        """
        Load face textures and compile into a cube map texture.

        Returns
        -------
        None.

        """
        
        # Bind texture
        self.bind()
        
        # For each face, load the texture and set the cube map's face to it
        for i, path in enumerate(self.faces):
            image = Image.open(f"resources/skybox/{path}")
            image_bytes = image.convert('RGB').tobytes()
            glTexImage2D(
                GL_TEXTURE_CUBE_MAP_POSITIVE_X + i,
                0,
                GL_RGB,
                image.size[0],
                image.size[1],
                0,
                GL_RGB,
                GL_UNSIGNED_BYTE,
                image_bytes
            )
            
        # Set cube map's magnification function
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        
        # Clamp cube map to edges in 3D
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_R, GL_CLAMP_TO_EDGE)
        
    def draw(self, program: ShaderProgram):
        """
        Draws cube model with cubemap texture around the camera behind other
        objects

        Parameters
        ----------
        program : ShaderProgram
            The skybox shader program to draw with.

        Returns
        -------
        None.

        """
        
        # Disable depth mask to render behind everything
        glDepthMask(GL_FALSE)
        
        # Set 0th texture unit to skybox cube map
        glActiveTexture(GL_TEXTURE0)
        program.setInt("skybox", 0)
        self.bind()
        
        # Hijack cube model's mesh to draw similarly, but with cube map texture
        glBindVertexArray(self.model.meshes[0].VAO)
        
        # Create model matrix to draw around the center of the scene
        model_matrix = glm.mat4()
        model_matrix = glm.translate(model_matrix, glm.vec3());
        model_matrix = glm.rotate(model_matrix, glm.vec3().x, self.model.up)
        model_matrix = glm.rotate(model_matrix, glm.vec3().y, self.model.right)
        model_matrix = glm.scale(model_matrix, glm.vec3(10))
        program.setMat4("model", model_matrix)
        
        # Draw model with cube map texture
        glDrawElements(GL_TRIANGLES, len(self.model.meshes[0].indices), GL_UNSIGNED_INT, None)
        
        # Reenable depth masking
        glDepthMask(GL_TRUE)
        
        
        