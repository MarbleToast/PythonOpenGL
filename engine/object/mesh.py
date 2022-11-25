import numpy as np
import glm
from OpenGL.GL import (
    GL_ARRAY_BUFFER,
    GL_ELEMENT_ARRAY_BUFFER,
    GL_STATIC_DRAW,
    GL_DYNAMIC_DRAW,
    GL_FLOAT,
    GL_UNSIGNED_INT,
    GL_TRIANGLES,
    GL_TEXTURE0,
    GL_TEXTURE1,
    GL_TEXTURE2,
    GL_TEXTURE3,
    GL_TEXTURE4,
    glBufferData,
    glGenVertexArrays,
    glGenBuffers,
    glBindBuffer,
    glBindVertexArray,
    glVertexAttribPointer,
    glEnableVertexAttribArray,
    glDrawElementsInstanced,
    glDeleteVertexArrays,
    glDeleteBuffers,
    glVertexAttribDivisor,
    glDrawElements,
    glActiveTexture,
    glGetIntegerv,
    GL_TEXTURE_BINDING_2D
)
from OpenGL.error import NullFunctionError

class Mesh:
    def __init__(self, parent, data, material):
        self.indices = np.array(self.get_indices(data['faces']), dtype=np.uint32)
        self.vertices = np.array(data['vertices'], dtype=np.float32)
        self.normals = np.array(data['normals'], dtype=np.float32)
        self.texCoords = np.array(data['texturecoords'], dtype=np.float32) if "texturecoords" in data else np.array([])
        self.tangents = np.array(data['tangents'], dtype=np.float32) if "tangents" in data else np.array([])
        self.bitangents = np.array(data['bitangents'], dtype=np.float32) if "bitangents" in data else np.array([])
        
        self.transforms = np.array([])
        
        self.material = material
        
        self.parent = parent
        
        self.VAO = 0
        self.VBOs = {}
        
        self.bind()
        
    def bind(self):
        self.VAO = glGenVertexArrays(1)
        glBindVertexArray(self.VAO)
        
        self.EBO = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.EBO)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, self.indices, GL_STATIC_DRAW)
        
        self.bindVBO("aPos", self.vertices, 3)
        self.bindVBO("aNormal", self.normals, 3)
        self.bindVBO("aTexCoords", self.texCoords, 2)
        self.bindVBO("aTangent", self.tangents, 3)
        self.bindVBO("aBitangent", self.bitangents, 3)
        
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)
        
    def genVBO(self, name):
        self.VBOs[name] = glGenBuffers(1)
        return self.VBOs[name], list(self.VBOs.keys()).index(name)  
    
    def bindVBO(self, name, data, size, dynamic = False):
        vBO, location = self.genVBO(name)
    
        glBindBuffer(GL_ARRAY_BUFFER, vBO)
        glBufferData(GL_ARRAY_BUFFER, data, GL_STATIC_DRAW if dynamic == False else GL_DYNAMIC_DRAW)
        glVertexAttribPointer(location,
                              size,
                              GL_FLOAT,
                              False,
                              0,
                              None)
        glEnableVertexAttribArray(location)
        glVertexAttribDivisor(location, 0 if dynamic == False else 1)

    def get_indices(self, faces):
        indices = []
        for face in faces:
            for indice in face:
                indices.append(indice)
        return indices

    def set_transforms(self, transforms):
        self.transforms = np.array(transforms)
    
    def draw(self, program):
        glActiveTexture(GL_TEXTURE1)
        program.setInt('mat.diffuseMap', 1)
        self.material.diffuse.bind()
        
        if self.material.normal:
            glActiveTexture(GL_TEXTURE2)
            program.setInt('mat.normalMap', 2)
            self.material.normal.bind()

        if self.material.specular:
            glActiveTexture(GL_TEXTURE3)
            program.setInt('mat.specularMap', 3)
            self.material.specular.bind()
                
        if self.material.depth:
            glActiveTexture(GL_TEXTURE4)
            program.setInt('mat.depthMap', 4)
            self.material.depth.bind()
            
        program.setFloat('mat.shininess', self.material.shininess)
        program.setFloat('mat.heightScale', self.material.height_scale)
        
        glBindVertexArray(self.VAO)
        
        for trf in self.transforms:
            model = glm.mat4()
            model = glm.translate(model, trf["position"]);
            model = glm.rotate(model, trf["rotation"].x, self.parent.up)
            model = glm.rotate(model, trf["rotation"].y, self.parent.right)
            model = glm.scale(model, trf["scale"])
            program.setMat4('model', model)
            glDrawElements(GL_TRIANGLES, len(self.indices), GL_UNSIGNED_INT, None)
            
        glActiveTexture(GL_TEXTURE0)
        if self.material.normal:
            self.material.normal.unbind()
            
        if self.material.specular:
            self.material.specular.unbind()
            
        if self.material.depth:
            self.material.depth.unbind()

    def __del__(self):
        try:
            glDeleteVertexArrays(1, self.VAO)
            for name, buf in list(self.VBOs.items()):
                glDeleteBuffers(1, self.VBOs.pop(name))
        except (NullFunctionError, TypeError):
            pass 