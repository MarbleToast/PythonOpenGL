import resource_cache
from mesh import Mesh

class Model:
    def __init__(self, filename, scene, custom_shaders=None):
        self.filename = filename
        self.scene = scene
        self.custom_shaders = custom_shaders
        self.meshes = []
        self._process_meshes(resource_cache.get_or_load_model(filename))
        
    def _process_meshes(self, obj):
        for mesh_data in obj.mesh_list:
            mesh = Mesh(mesh_data, self)
            mesh.bind()
            self.meshes.append(mesh)
            
        # self.materials = [resource_cache.get_or_load_texture(mat) for mat in obj.materials]
    
    def draw(self):
        for mesh in self.meshes:
            mesh.draw()