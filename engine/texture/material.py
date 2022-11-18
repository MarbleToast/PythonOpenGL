from engine.core.cache import get_or_load_texture
class Material:
    def __init__(self, path, diffuse_path, normal_path = None, specular_path = None, displacement_path = None):
        self.path = path
            
        self.diffuse = get_or_load_texture(diffuse_path)
        self.normal = get_or_load_texture(normal_path) if normal_path else None
        self.specular = get_or_load_texture(specular_path) if specular_path else None
        self.depth = get_or_load_texture(displacement_path) if displacement_path else None
