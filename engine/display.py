import glfw
import logging
from engine.config import config

def initialise_display():
    width, height = config['window_width'], config['window_height']
    
    if not glfw.init():
        logging.error('Failed to initialize GLFW.')
        return
    
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 4)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 6)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, True)
    glfw.window_hint(glfw.SAMPLES, config['sampling_level'])
    
    if config['fullscreen']:
        mode = glfw.get_video_mode(glfw.get_primary_monitor())
        width, height = mode.size.width, mode.size.height
        window = glfw.create_window(mode.size.width, mode.size.height, config['app_name'], glfw.get_primary_monitor(), None)
    else:
        window = glfw.create_window(width, height, config['app_name'], None, None)

    if not window:
        logging.error('Failed to create GLFW Window.')
        glfw.terminate()
        return
    
    glfw.make_context_current(window)
    glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_DISABLED)
    
    return window
    