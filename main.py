import glfw
import logging
from engine.config import CONFIG
from engine.application import Application
from OpenGL.GL import *

def initialise_glfw():
    """
    Initialise GLFW, the OpenGL wrapper library, and sets flags for the
    GL context.

    Raises
    ------
    RuntimeError
        If GLFW cannot be initialised.

    Returns
    -------
    None.

    """
    if not glfw.init():
        raise RuntimeError("Failed to initialize GLFW.")

    # OpenGL 4.6
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 4)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 6)
    
    # Use Core profile in forwards compatability mode
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, True)
    
    # Multisampling level
    glfw.window_hint(glfw.SAMPLES, CONFIG['sampling_level'])

def initialise_display():
    """
    Initialises window with information from config file.

    Returns
    -------
    window : GLFWWindow
        The handle for the window.

    """
    width, height = CONFIG['window_width'], CONFIG['window_height']
    
    # Create window of specified size with title from config
    window = glfw.create_window(
        width,
        height,
        CONFIG['app_name'],
        None,
        None
    )

    # Handle GLFW failing
    if not window:
        logging.error('Failed to create GLFW Window.')
        glfw.terminate()
        return
    
    # Set window as context, then hide cursor
    glfw.make_context_current(window)
    glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_DISABLED)
    
    return window

def initialise_gl_flags():
    """
    Initialise persistent flags for the GL context.

    Returns
    -------
    None.

    """
    # Enable depth testing
    glEnable(GL_DEPTH_TEST)
    
    # Enable multisampling explicitly
    glEnable(GL_MULTISAMPLE)
    
    # Enable back face culling 
    glEnable(GL_CULL_FACE)
    glCullFace(GL_BACK)
    
    # Enable alpha blending for PNG transparencies
    glEnable(GL_BLEND);
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
    
if __name__ == '__main__': 
    logging.root.setLevel(logging.INFO)
    initialise_glfw()
    app = Application(initialise_display())
    initialise_gl_flags()
    app.run()