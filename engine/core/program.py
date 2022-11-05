import glm
from OpenGL.GL import (
    glUseProgram,
    glGetAttribLocation,
    glGetUniformLocation,
    glUniform1i,
    glUniform1f,
    glUniform2fv,
    glUniform3fv,
    glUniform4fv,
    glUniformMatrix2fv,
    glUniformMatrix3fv,
    glUniformMatrix4fv,
    shaders
)

class ShaderProgram:
    def __init__(self, vertPath, fragPath):
        self.id = 0
        self.vertSource = self.loadSource(vertPath)
        self.fragSource = self.loadSource(fragPath)
        self.link()
        
    def loadSource(self, path):
        with open(path) as file:
            source = file.read()
        return source

    def link(self):
        self.id = shaders.compileProgram(
            shaders.compileShader(self.vertSource, shaders.GL_VERTEX_SHADER),
            shaders.compileShader(self.fragSource, shaders.GL_FRAGMENT_SHADER)
        )

    def use(self):
        glUseProgram(self.id)

    def getId(self):
        return self.id

    def getAttribLocation(self, name):
        return glGetAttribLocation(self.id, name)

    def getUniformLocation(self, name):
        return glGetUniformLocation(self.id, name)

    def setInt(self, name, value):
        glUniform1i(self.getUniformLocation(name), value)

    def setFloat(self, name, value):
        glUniform1f(self.getUniformLocation(name), value)

    def setVec2(self, name, vec):
        glUniform2fv(self.getUniformLocation(name), 1, glm.value_ptr(vec))

    def setVec3(self, name, vec):
        glUniform3fv(self.getUniformLocation(name), 1, glm.value_ptr(vec))

    def setVec4(self, name, vec):
        glUniform4fv(self.getUniformLocation(name), 1, glm.value_ptr(vec))

    def setMat2(self, name, mat):
        glUniformMatrix2fv(self.getUniformLocation(name), 1, False, glm.value_ptr(mat))

    def setMat3(self, name, mat):
        glUniformMatrix3fv(self.getUniformLocation(name), 1, False, glm.value_ptr(mat))

    def setMat4(self, name, mat):
        glUniformMatrix4fv(self.getUniformLocation(name), 1, False, glm.value_ptr(mat))