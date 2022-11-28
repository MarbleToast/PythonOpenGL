import glm
import glfw
from engine.constants import WORLD_UP
from engine.object.sceneobject import SceneObject
from engine.config import CONFIG

class Camera(SceneObject):
    def __init__(self, fov = 45, position = None, speed = 10):
        super().__init__("Camera", None, position)
        self.fov = fov
        self.speed = speed
        self.sensitivity = 0.25
        
    def update(self, win, dt):
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

    def rotate(self, offsetX, offsetY):
        self.rotation.x += offsetX * self.sensitivity
        self.rotation.y += offsetY * self.sensitivity
        if self.rotation.y > 89:
            self.rotation.y = 89
        elif self.rotation.y < -89:
            self.rotation.y = -89
        self.update_vectors()
        
    def get_perspective(self, width, height):
        return glm.perspective(self.fov, width/height, CONFIG["near_plane"], CONFIG["far_plane"])

    def get_view(self):
        return glm.lookAt(self.position, self.position + self.front, self.up)