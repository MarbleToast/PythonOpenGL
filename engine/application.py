import glfw
import logging
from OpenGL.GL import *
from engine.scene import Scene

"""
Application

Controls logic to do with application main loop.
"""
class Application:
    def __init__(self, window):
        """
        Initialises application with given window.

        Parameters
        ----------
        window : GLFWWindow
            The window to render to.

        Returns
        -------
        None.

        """
        
        self.scene = None
        self.window = window
        
        self.initialise_scene()
        self.initialise_callbacks()
        
    def initialise_scene(self):
        """
        Initialises scene.

        Returns
        -------
        None.

        """
        
        self.scene = Scene()

    def initialise_callbacks(self):
        """
        Initialises callbacks.

        Returns
        -------
        None.

        """
        
        # Mouse movement callback
        glfw.set_cursor_pos_callback(self.window, self.mouse_callback)
        
        # Keyboard callback
        glfw.set_key_callback(self.window, self.key_callback)
        
        # Window refresh callback
        glfw.set_window_refresh_callback(self.window, self.window_refresh_callback)
        
    def mouse_callback(self, window, x: int, y: int):
        """
        Calls the scene's mouse callback. The function signature conforms to 
        the GLFW call without having to pass unnecessary parameters to the
        scene.

        Parameters
        ----------
        window : GLFWWindow
            Unused. The window firing the callback.
        x : int
            The x of the new mouse position.
        y : int
            The y of the new mouse position.

        Returns
        -------
        None.

        """
        
        self.scene.mouse_callback(x, y)

    def key_callback(self, window, key: int, scancode: int, action: int, mods: int):
        """
        Calls the scene's key callback. The function signature conforms to 
        the GLFW call without having to pass unnecessary parameters to the
        scene.

        Parameters
        ----------
        window : GLFWWindow
            Unused. The window firing the event.
        key : int
            The key of the event.
        scancode : int
            Unused. System specific key scancode.
        action : int
            The event happening to the key (key held, key pressed, etc.).
        mods : int
            Unused. Number detailing modifier keys held (shift, control, etc.)

        Returns
        -------
        None.

        """
        
        # Regardless of scene, if ESC pressed, quit
        if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
            glfw.set_window_should_close(window, True)
        else:
            self.scene.key_callback(key, action)
            
    def window_refresh_callback(self, window):
        """
        On window refresh (when the window is damaged etc), repair.

        Parameters
        ----------
        window : GLFWWindow
            The window firing the event.

        Returns
        -------
        None.

        """
        
        # Clear buffer bits and swap render buffers.
        logging.warning("Window refreshing!")
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glfw.swap_buffers(self.window)
        
    def run(self):   
        """
        Run the main loop, updating and drawing the scene.

        Returns
        -------
        None.

        """
        
        # Get time of the program
        lastTime = glfw.get_time()
        while not glfw.window_should_close(self.window):

            # Calculate delta time for performance independent movements
            currentTime = glfw.get_time()
            deltaTime = currentTime - lastTime
            lastTime = currentTime
            
            # Update the scene, then draw the scene
            self.scene.update(self.window, deltaTime)
            self.scene.draw()

            # Check for events
            glfw.poll_events()
            
            # Swap render buffers
            glfw.swap_buffers(self.window)

        # On end of loop, terminate GLFW.
        glfw.terminate()