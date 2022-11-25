import os, json
# import numpy as np
from engine.object.mesh import Mesh 
from engine.object.sceneobject import SceneObject
from engine.texture.material import Material
# from engine.core.cache import get_or_load_materials

def get_property_from_material(key, material):
    return next((p for p in material["properties"] if p["key"] == key), None)

class Model(SceneObject):
    def __init__(self, path, position = None, rotation = None, scale = None, texture_set = "default"):
        """
        

        Parameters
        ----------
        path : str
            DESCRIPTION.
        position : glm.vec3, optional
            DESCRIPTION. The default is None.
        rotation : glm.vec3, optional
            DESCRIPTION. The default is None.
        scale : glm.vec3, optional
            DESCRIPTION. The default is None.
        textures : dict["name", "diffuse", "normal", "specular", "depth"], optional
            DESCRIPTION. The default is None.

        Raises
        ------
        RuntimeError
            DESCRIPTION.

        """
        if not os.path.exists(path):
            raise RuntimeError(f'Model source file {path} does not exists.')
            
        super().__init__(path, None, position, rotation, scale)   
        
        self.meshes = []

        data = self.load_data(path)
        for mesh_data in data['meshes']:
            mesh_mat = Material(texture_set)
            self.meshes.append(Mesh(self, mesh_data, mesh_mat))
        
        
    def load_data(self, path):
        data = None
        with open(path) as file:
            data = json.load(file)
        return data       

    def set_transforms(self, transforms):
        for mesh in self.meshes:
            mesh.set_transforms(transforms)
            
    def get_transforms(self):
        return self.meshes[0].transforms

    def draw(self, program):
        program.use()
        for mesh in self.meshes:
            mesh.draw(program)

    def __del__(self):
        self.meshes.clear()
