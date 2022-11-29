import glm
import glfw
from engine.constants import WORLD_UP
from engine.object.sceneobject import SceneObject
from engine.config import CONFIG

"""
Camera

Inherits from SceneObject
Object for calculating and controlling the view and perspective matrices.
"""
class Camera(SceneObject):
    def __init__(self, fov: int = 45, position: glm.vec3 = None, speed: int = 10):
        """
        Initialises the Camera object, plus its SceneObject superclass.

        Parameters
        ----------
        fov : int, optional
            The FOV for the perspective in degrees. The default is 45.
        position : glm.vec3, optional
            The default for initial location. Passing None passes None to the
            SceneObject superclass, which sets the location to (0, 0, 0).
        speed : int, optional
            Multiplier for movement. The default is 10.

        Returns
        -------
        None.

        """
        
        # Initialise SceneObject superclass
        super().__init__("Camera", position=position)
        
        # Set attributes
        # fov: angle with which to create the perspective projection matrix
        # speed: movement multiplier
        # sensitivity: mouse movement multiplier
        self.fov = fov
        self.speed = speed
        self.sensitivity = 0.25
        
    def update(self, win, dt: float):
        """
        Handle keyboard input, plus other effects as defined in the parent
        scene's .update() method.

        Parameters
        ----------
        win : GLFWWindow
            The reference for the window to check events in
        dt : float
            Delta time (time in seconds since the last scene update/draw step)

        Returns
        -------
        None.

        """
        
        # For each key that has an effect, check if pressed. If so, modify
        # the position vector.
        if glfw.get_key(win, glfw.KEY_W) == glfw.PRESS:
            self.position += self.front * (self.speed * dt)
        if glfw.get_key(win, glfw.KEY_S) == glfw.PRESS:
            self.position -= self.front * (self.speed * dt)
        if glfw.get_key(win, glfw.KEY_A) == glfw.PRESS:
            self.position -= self.right * (self.speed * dt)
        if glfw.get_key(win, glfw.KEY_D) == glfw.PRESS:
            self.position += self.right * (self.speed * dt)
        if glfw.get_key(win, glfw.KEY_SPACE) == glfw.PRESS:
            self.position += WORLD_UP * (self.speed * dt)
        if glfw.get_key(win, glfw.KEY_LEFT_SHIFT) == glfw.PRESS:
            self.position -= WORLD_UP * (self.speed * dt)

    def rotate(self, offsetX: int, offsetY: int):
        """
        Handle for rotation of the camera. Calls SceneObject.update_vectors()
        to propagate rotational effects to the axis vectors.

        Parameters
        ----------
        offsetX : int
            Change in horizontal mouse position
        offsetY : int
            Change in vertical mouse position

        Returns
        -------
        None.

        """
        
        # Change rotation vector
        self.rotation.x += offsetX * self.sensitivity
        self.rotation.y += offsetY * self.sensitivity
        
        # Clamp vertical rotation
        if self.rotation.y > 89:
            self.rotation.y = 89
        elif self.rotation.y < -89:
            self.rotation.y = -89
            
        # Propagate changes to axis vectors
        self.update_vectors()
        
    def get_perspective(self, width: int, height: int) -> glm.mat4:
        """
        Returns perspective projection matrix for given viewport aspect ratio,
        fov, and near/far plane distances.

        Parameters
        ----------
        width : int
            Viewport width
        height : int
            Viewport height

        Returns
        -------
        glm.mat4
            The perspective projection matrix

        """
        
        return glm.perspective(self.fov, width/height, CONFIG["near_plane"], CONFIG["far_plane"])

    def get_view(self) -> glm.mat4:
        """
        Returns look-at/view matrix for the camera's position, the position
        pointed to by the camera, and the camera's y axis vector.


        Returns
        -------
        glm.mat4
            The view matrix

        """
        
        # We calculate the center vector by adding our front axis vector to our
        # current position
        return glm.lookAt(self.position, self.position + self.front, self.up)