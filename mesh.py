from sys import getsizeof
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
    glBindVertexArray,
    glVertexAttribPointer,
    glEnableVertexAttribArray
)

vertex_shader = """
#version 330
in vec4 position;
void main()
{
   gl_Position = position;
}
"""

fragment_shader = """
#version 330
void main()
{
   gl_FragColor = vec4(1.0f, 1.0f, 1.0f, 1.0f);
}
"""


class Mesh:
    def __init__(self, mesh):
        self.vertices, self.indices = np.unique([face for face in mesh.faces], return_inverse=True, axis=0)
        self.normals = np.zeros([self.vertices.shape(), 3])
        
    def bind(self):
        # Allocate and assign Vertex Array Object
        VAO = glGenVertexArrays(1)
        # Set VAO as current bound vertex array object
        glBindVertexArray(VAO)
        
        # Allocate and assign Vertex Buffer Object
        VBO = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, VBO)
        glBufferData(GL_ARRAY_BUFFER, self.vertices, GL_STATIC_DRAW)

        # Allocate and assign Element Buffer Object
        EBO = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, self.indices, GL_STATIC_DRAW)
        
        glBindVertexArray(0)
        
