# imports all openGL functions
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GL import shaders

# we will use numpy to store data in arrays
import numpy as np

class ShaderProgram:
    def __init__(self, vertex_shader = None, fragment_shader = None):        
        # load the vertex shader GLSL code
        if vertex_shader is None:
            self.vertex_shader_source = '''
                #version 460 core
                layout (location = 0) in vec3 aPos;
                // layout (location = 1) in vec2 aTexCoord;
                
                // out vec2 TexCoord;
                
                uniform mat4 model;
                uniform mat4 view;
                uniform mat4 projection;
                
                void main()
                {
                    // TexCoord = vec2(aTexCoord.x, aTexCoord.y);    
                    gl_Position = projection * view * model * vec4(aPos, 1.0);
                }
            '''
        else:
            print('Load vertex shader from file: {}'.format(vertex_shader))
            with open(vertex_shader, 'r') as file:
                self.vertex_shader_source = file.read()
            print(self.vertex_shader_source)

        # load the fragment shader GLSL code
        if fragment_shader is None:
            self.fragment_shader_source = '''
                #version 130
                // parameters interpolated from the output of the vertex shader
                // in vec3 vertex_color;      // the vertex colour is received from the vertex shader
                
                // main function of the shader
                void main() {                   
                      gl_FragColor = vec4(1.0, 1.0, 1.0, 1.0);      // for now, we just apply the colour uniformly
                }
            '''
        else:
            print('Load fragment shader from file: {}'.format(fragment_shader))
            with open(fragment_shader, 'r') as file:
                self.fragment_shader_source = file.read()
            print(self.fragment_shader_source)

    def compile(self):
        self.program = shaders.compileProgram(
            shaders.compileShader(self.vertex_shader_source, shaders.GL_VERTEX_SHADER),
            shaders.compileShader(self.fragment_shader_source, shaders.GL_FRAGMENT_SHADER)
        )
        
    def setMat4(self, name, mat):
        glUniformMatrix4fv(glGetUniformLocation(self.program, name), 1, GL_FALSE, mat);

    def bind(self, projection, view, model):
        # tell OpenGL to use this shader program for rendering
        glUseProgram(self.program)

        # set the PVM matrix uniform
        self.setMat4('projection', projection)
        self.setMat4('view', view)
        self.setMat4('model', model)

    def unbind(self):
        glUseProgram(0)