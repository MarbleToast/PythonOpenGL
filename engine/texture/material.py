from engine.core.cache import get_or_load_texture
import os.path
class Material:
    def __init__(self, name):
        self.name = name
        
        self.diffuse = get_or_load_texture(f"{name}_diffuse.png")
        self.normal = None
        self.specular = None
        self.depth = None
        
        if os.path.isfile(f"resources/textures/{name}_normal.png"):
            self.normal = get_or_load_texture(f"{name}_normal.png")
        if os.path.isfile(f"resources/textures/{name}_specular.png"):
            self.specular = get_or_load_texture(f"{name}_specular.png")
        if os.path.isfile(f"resources/textures/{name}_depth.png"):
            self.depth = get_or_load_texture(f"{name}_depth.png")
        
        self.shininess = 0.5
        self.height_scale = 0
