import numpy as np
from OpenGL.GL import (
    glBufferData,
    glGenVertexArrays,
    glGenBuffers,
    glBindBuffer,
    GL_ARRAY_BUFFER,
    GL_ELEMENT_ARRAY_BUFFER,
    GL_STATIC_DRAW,
    GL_FLOAT,
    GL_UNSIGNED_INT,
    GL_TRIANGLES,
    glBindVertexArray,
    glVertexAttribPointer,
    glEnableVertexAttribArray,
    glBindAttribLocation,
    glDrawElements
)

class Mesh:
    def __init__(self, mesh, model):
        self.model = model
        self.vertices, self.indices = np.unique([face for face in mesh.faces], return_inverse=True, axis=0)
        self.normals = np.zeros((self.vertices.shape[0], 3), dtype='f')
        self.colours = np.ones((self.vertices.shape[0], 3), dtype='f')
        
        self.VAO = 0
        self.VBOs = {}
        
    def bind_VBO(self, name, data):
        self.VBOs[name] = glGenBuffers(1)
        attr_value = list(self.VBOs.keys()).index(name)
        print(attr_value)
        
        shaders = self.model.parent_object.scene.default_shaders.program
        if self.model.custom_shaders:
            shaders = self.model.custom_shaders.program
        
        glBindAttribLocation(shaders, attr_value, name)
            
        # Allocate and assign Vertex Buffer Object
        
        glBindBuffer(GL_ARRAY_BUFFER, self.VBOs[name])
        
        glEnableVertexAttribArray(attr_value)
        glVertexAttribPointer(attr_value, data.shape[1], GL_FLOAT, False, 0, None)
        glBufferData(GL_ARRAY_BUFFER, data, GL_STATIC_DRAW)
        
    def bind(self):
        # Allocate and assign Vertex Array Object
        self.VAO = glGenVertexArrays(1)
        # Set VAO as current bound vertex array object
        glBindVertexArray(self.VAO)
        
        self.bind_VBO('aPos', self.vertices)
        
        # Allocate and assign Element Buffer Object
        EBO = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, self.indices, GL_STATIC_DRAW)
        
        glBindVertexArray(0)
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        
    def draw(self):            
        glBindVertexArray(self.VAO)
        glDrawElements(GL_TRIANGLES, len(self.indices), GL_UNSIGNED_INT, None)
        glBindVertexArray(0)
