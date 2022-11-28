# -*- coding: utf-8 -*-
"""

"""
import glm
import numpy as np
from PIL import Image
from OpenGL.GL import *
from engine.texture.texture import Texture
from engine.object.model import Model

class Skybox(Texture):
    def __init__(self, right, left, top, bottom, back, front):
        super().__init__(GL_TEXTURE_CUBE_MAP)
        self.model = Model("resources/models/cube.json")
        
        self.faces = [right, left, top, bottom, back, front]
        self.load_cube_map()
        
    def load_cube_map(self):
        self.bind()
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
            
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_R, GL_CLAMP_TO_EDGE)
        
        
    def draw(self):
        glDepthMask(GL_FALSE)
        
        glActiveTexture(GL_TEXTURE0)
        self.skybox_program.setMat4("skybox", 0)
        self.bind()
        
        glBindVertexArray(self.model.VAO)
        
        model_matrix = glm.mat4()
        model_matrix = glm.translate(model_matrix, glm.vec3());
        model_matrix = glm.rotate(model_matrix, glm.vec3().x, self.model.up)
        model_matrix = glm.rotate(model_matrix, glm.vec3().y, self.model.right)
        model_matrix = glm.scale(model_matrix, glm.vec3(10))
        self.skybox_program.setMat4("model", model_matrix)
        
        glDrawElements(GL_TRIANGLES, len(self.model.indices), GL_UNSIGNED_INT, None)
        glDepthMask(GL_TRUE)
        
        
        