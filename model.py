import resource_cache
from mesh import Mesh

class Model:
    def __init__(self, filename):
        self.filename = filename
        self._process_meshes(resource_cache.get_or_load_model(filename))
        
    def _process_meshes(self, obj):
        self.meshes = []
        for mesh_data in obj.mesh_list:
            self.meshes.append(Mesh(mesh_data))
        # self.materials = [resource_cache.get_or_load_texture(mat) for mat in obj.materials]
    
        