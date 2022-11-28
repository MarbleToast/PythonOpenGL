import glfw
import logging
from OpenGL.GL import *
from engine.scene import Scene

class Application:
    def __init__(self, window):
        self.scene = None
        self.window = window
        
        self.initialise_scene()
        self.initialise_callbacks()
        
    def initialise_scene(self):
        self.scene = Scene("Main")

    def initialise_callbacks(self):
        glfw.set_cursor_pos_callback(self.window, self.mouse_callback)
        glfw.set_key_callback(self.window, self.key_callback)
        glfw.set_window_refresh_callback(self.window, self.window_refresh_callback)
        
    def mouse_callback(self, window, x, y):
        self.scene.mouse_callback(x, y)

    def key_callback(self, window, key, scancode, action, mods):
        if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
            glfw.set_window_should_close(window, True)
        else:
            self.scene.key_callback(key, action)
            
    def window_refresh_callback(self, window):
        logging.warning("Window refreshing!")
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glfw.swap_buffers(self.window)
        
    def run(self):        
        lastTime = glfw.get_time()
        while not glfw.window_should_close(self.window):

            currentTime = glfw.get_time()
            deltaTime = currentTime - lastTime
            lastTime = currentTime
            
            self.scene.update(self.window, deltaTime)
            self.scene.draw()

            glfw.poll_events()
            glfw.swap_buffers(self.window)

        glfw.terminate()