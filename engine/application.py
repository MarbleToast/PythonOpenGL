import glfw
import glm
import logging
import random
import numpy as np
from OpenGL.GL import *
from engine.core.program import ShaderProgram
from engine.object.model import Model
from engine.config import config
from engine.display import initialise_display
from engine.scene import Scene

class Application:
    def __init__(self):
        self.window = initialise_display()
        self.width, self.height = glfw.get_window_size(self.window)
        
        self.mouse_touched = False
        self.last_mouse_x, self.last_mouse_y = 0, 0
        
        glEnable(GL_MULTISAMPLE)
        glEnable(GL_CULL_FACE)
        glCullFace(GL_BACK)
        
        glViewport(0, 0, self.width, self.height)
        
        self.generate_perspective()
        
        glfw.set_framebuffer_size_callback(self.window, self.resize_callback)
        glfw.set_cursor_pos_callback(self.window, self.mouse_callback)
        glfw.set_key_callback(self.window, self.key_callback)
        glfw.set_window_refresh_callback(self.window, self.window_refresh_callback)
        
    def generate_perspective(self):
        self.perspective = glm.perspective(45, self.width/self.height, config['near_plane'], config['far_plane'])
        
    def resize_callback(self, window, w, h):
        self.width, self.height = w, h
        glViewport(0, 0, self.width, self.height)
        self.generate_perspective()
        
    def mouse_callback(self, window, x, y):
        if not self.mouse_touched:
            self.last_mouse_x = x
            self.last_mouse_y = y
            self.mouse_touched = True
            
        x_offset = x - self.last_mouse_x
        y_offset = self.last_mouse_y - y
        
        self.last_mouse_x = x
        self.last_mouse_y = y

        self.scene.camera.rotate(x_offset, y_offset)

    def key_callback(self, window, key, scancode, action, mods):
        if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
            glfw.set_window_should_close(window, True)
            
    def window_refresh_callback(self, window):
        logging.warning("Window refreshing!")
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glfw.swap_buffers(self.window)
        
    def run(self):
        program = ShaderProgram('resources/shaders/vertex.vs', 'resources/shaders/fragment.fs')
        
        self.scene = Scene("Main", self.perspective)

        lastTime = glfw.get_time()
        while not glfw.window_should_close(self.window):

            currentTime = glfw.get_time()
            deltaTime = currentTime - lastTime
            lastTime = currentTime
            
            self.scene.update(self.window, deltaTime)
            
            self.scene.draw(program)

            glfw.poll_events()
            glfw.swap_buffers(self.window)

        glfw.terminate()