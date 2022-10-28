import resource_cache
import helpers
import numpy as np
from mesh import Mesh

class Model:
    def __init__(self, filename, parent_object, custom_shaders=None):
        self.filename = filename
        self.parent_object = parent_object
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
        shaders = self.parent_object.scene.default_shaders
        if self.custom_shaders:
            shaders = self.custom_shaders
            
        model = np.ones((4, 4))
        model = helpers.translate(model, self.parent_object.transform.position)
        
        shaders.bind(self.parent_object.scene.camera.frustrum, self.parent_object.scene.camera.get_view(), model)
        for mesh in self.meshes:
            mesh.draw()