from gameobject import GameObject
from camera import Camera
from event import add_tick_listener
from transform import Transform

class Scene:
    def __init__(self, default_shaders):
        self.objects = []
        self.camera = None
        self.default_shaders = default_shaders
        self.default_shaders.compile()
    
    def add_static_model(self, filename, transform = Transform()):
        obj = GameObject(filename + str(len(self.objects)), self, transform, filename)
        self.objects.append(obj)
        add_tick_listener(obj)
        
    def create_camera(self, viewport_width, viewport_height):
        self.camera = Camera(viewport_width, viewport_height)
        add_tick_listener(self.camera)
        
    def render(self):
        for obj in self.objects:
            if obj.model:
                obj.model.draw()