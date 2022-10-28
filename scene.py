from model import Model
from camera import Camera
from event import add_tick_listener

class Scene:
    def __init__(self, default_shaders):
        self.models = []
        self.camera = None
        self.default_shaders = default_shaders
        self.default_shaders.compile()
    
    def add_model(self, filename):
        self.models.append(Model(filename, self))
        
    def create_camera(self, viewport_width, viewport_height):
        self.camera = Camera(viewport_width, viewport_height)
        add_tick_listener(self.camera)
        
    def render(self):
        for model in self.models:
            model.draw()