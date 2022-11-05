import numpy as np
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
)
from OpenGL.error import NullFunctionError

class Mesh:
    def __init__(self, data, material):
        self.indices = np.array(self.getIndices(data['faces']), dtype=np.uint32)
        self.vertices = np.array(data['vertices'], dtype=np.float32)
        self.normals = np.array(data['normals'], dtype=np.float32)
        self.texCoords = np.array(data['texturecoords'], dtype=np.float32)
        self.tangents = np.array(data['tangents'], dtype=np.float32)
        self.positions = np.array([[0, 0, 0]], dtype=np.float32)
        
        self.material = material
        
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
        self.bindVBO("aInstancePos", self.positions, 3, dynamic=True)
        
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

    def getIndices(self, assimpIndices):
        indicesList = []
        for face in assimpIndices:
            for indice in face:
                indicesList.append(indice)
        return indicesList

    def set_positions(self, positions):
        self.positions = np.array(positions, dtype=np.float32)
        
        glBindVertexArray(self.VAO)
        glBindBuffer(GL_ARRAY_BUFFER, self.VBOs["aInstancePos"])
        glBufferData(GL_ARRAY_BUFFER, self.positions, GL_DYNAMIC_DRAW)
        glBindVertexArray(0)

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
        
        glBindVertexArray(self.VAO)
        if len(self.positions) > 1:
            glDrawElementsInstanced(GL_TRIANGLES, len(self.indices), GL_UNSIGNED_INT, None, len(self.positions))
        else:
            glDrawElements(GL_TRIANGLES, len(self.indices), GL_UNSIGNED_INT, None)
            
        glActiveTexture(GL_TEXTURE0)

    def __del__(self):
        try:
            glDeleteVertexArrays(1, self.VAO)
            for name, buf in list(self.VBOs.items()):
                glDeleteBuffers(1, self.VBOs.pop(name))
        except (NullFunctionError, TypeError):
            pass 