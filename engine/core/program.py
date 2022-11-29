import glm
import logging
from OpenGL.GL import *
from OpenGL.GL import shaders

"""
ShaderProgram

Handles loading, linking, and compiling a shader from source. Holds a reference
to the compiled shader for future use.
"""
class ShaderProgram:
    def __init__(self, vertPath: str, fragPath: str):
        """
        Constructor for a shader program. Handles source loading and 
        compilation, ready to be bound via ShaderProgram.use()

        Parameters
        ----------
        vertPath : str
            Path to the vertex shader
        fragPath : str
            Path to the fragment shader

        """
        # Shader ID as 0 to start (unassigned)
        self.id = 0
        
        # Load source files from paths
        self.vertSource = self.loadSource(vertPath)
        self.fragSource = self.loadSource(fragPath)
        
        # Link shaders.
        self.link()
        
    def loadSource(self, path: str):
        """
        Loads a shader source from a file

        Parameters
        ----------
        path : str
            DESCRIPTION.

        Returns
        -------
        source : str
            Contents of the file at the path specified.

        """
        logging.info(f"Loading shader from {path}")
        with open(path) as file:
            source = file.read()
        return source

    def link(self):
        """
        Compiles and links shaders and shader program, and sets self.id to the
        return for future use.

        Returns
        -------
        None.

        """
        
        # Compile shaders via PyOpenGL's .shaders subpackage
        self.id = shaders.compileProgram(
            shaders.compileShader(self.vertSource, shaders.GL_VERTEX_SHADER),
            shaders.compileShader(self.fragSource, shaders.GL_FRAGMENT_SHADER)
        )
        logging.info(f"Compiled shader program {self.id}")

    def use(self):
        """
        Uses the program.

        Returns
        -------
        None.

        """
        glUseProgram(self.id)

    def getId(self):
        """
        Returns the ID for the program

        Returns
        -------
        int
            The ID

        """
        return self.id

    def getUniformLocation(self, name: str):
        """
        Returns the location for a uniform in the program

        Parameters
        ----------
        name : str
            The uniform identifier to find the location of

        Returns
        -------
        int
            The uniform's location

        """
        
        return glGetUniformLocation(self.id, name)

    def setInt(self, name: str, value: int):
        """
        Sets an integer uniform

        Parameters
        ----------
        name : str
            The uniform to set
        value : int
            The value to set the uniform to

        Returns
        -------
        None.

        """
        
        glUniform1i(self.getUniformLocation(name), value)

    def setFloat(self, name: str, value: float):
        """
        Sets a float uniform

        Parameters
        ----------
        name : str
            The uniform to set
        value : float
            The value to set the uniform to

        Returns
        -------
        None.

        """
        
        glUniform1f(self.getUniformLocation(name), value)

    def setVec2(self, name: str, vec: glm.vec2):
        """
        Sets a vec2 uniform

        Parameters
        ----------
        name : str
            The uniform to set
        value : vec2
            The value to set the uniform to

        Returns
        -------
        None.

        """
        
        glUniform2fv(self.getUniformLocation(name), 1, glm.value_ptr(vec))

    def setVec3(self, name: str, vec: glm.vec3):
        """
        Sets a vec3 uniform

        Parameters
        ----------
        name : str
            The uniform to set
        value : vec3
            The value to set the uniform to

        Returns
        -------
        None.

        """
        
        glUniform3fv(self.getUniformLocation(name), 1, glm.value_ptr(vec))

    def setVec4(self, name: str, vec: glm.vec4):
        """
        Sets a vec4 uniform

        Parameters
        ----------
        name : str
            The uniform to set
        value : vec4
            The value to set the uniform to

        Returns
        -------
        None.

        """
        
        glUniform4fv(self.getUniformLocation(name), 1, glm.value_ptr(vec))

    def setMat2(self, name: str, mat: glm.mat2):
        """
        Sets a mat2 uniform

        Parameters
        ----------
        name : str
            The uniform to set
        value : mat2
            The value to set the uniform to

        Returns
        -------
        None.

        """
        
        glUniformMatrix2fv(self.getUniformLocation(name), 1, False, glm.value_ptr(mat))

    def setMat3(self, name: str, mat: glm.mat3):
        """
        Sets a mat3 uniform

        Parameters
        ----------
        name : str
            The uniform to set
        value : mat3
            The value to set the uniform to

        Returns
        -------
        None.

        """
        
        glUniformMatrix3fv(self.getUniformLocation(name), 1, False, glm.value_ptr(mat))

    def setMat4(self, name: str, mat: glm.mat4):
        """
        Sets a mat4 uniform

        Parameters
        ----------
        name : str
            The uniform to set
        value : mat4
            The value to set the uniform to

        Returns
        -------
        None.

        """
        
        glUniformMatrix4fv(self.getUniformLocation(name), 1, False, glm.value_ptr(mat))