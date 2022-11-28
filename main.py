import glfw
import logging
from engine.config import CONFIG
from engine.application import Application
from OpenGL.GL import *

def initialise_glfw():
    if not glfw.init():
        raise RuntimeError("Failed to initialize GLFW.")

    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 4)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 6)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, True)
    glfw.window_hint(glfw.SAMPLES, CONFIG['sampling_level'])

def initialise_display():
    width, height = CONFIG['window_width'], CONFIG['window_height']
    
    if CONFIG['fullscreen']:
        mode = glfw.get_video_mode(glfw.get_primary_monitor())
        width, height = mode.size.width, mode.size.height
        window = glfw.create_window(
            mode.size.width,
            mode.size.height,
            CONFIG['app_name'],
            glfw.get_primary_monitor(),
            None
        )
    else:
        window = glfw.create_window(
            width,
            height,
            CONFIG['app_name'],
            None,
            None
        )

    if not window:
        logging.error('Failed to create GLFW Window.')
        glfw.terminate()
        return
    
    glfw.make_context_current(window)
    glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_DISABLED)
    
    return window

def initialise_gl_flags():
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_MULTISAMPLE)
    glEnable(GL_CULL_FACE)
    glCullFace(GL_BACK)
    glEnable(GL_BLEND);
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
    
if __name__ == '__main__':
    initialise_glfw()
    app = Application(initialise_display())
    initialise_gl_flags()
    app.run()