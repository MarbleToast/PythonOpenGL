import os, json
# import numpy as np
from engine.object.mesh import Mesh 
from engine.object.sceneobject import SceneObject
from engine.texture.material import Material
# from engine.core.cache import get_or_load_materials

class Model(SceneObject):
    def __init__(self, path, position = None, rotation = None, scale = None):
        if not os.path.exists(path):
            raise RuntimeError(f'Model source file {path} does not exists.')
            
        super().__init__(path, None, position, rotation, scale)   
        
        self.meshes = []

        data = self.load_data(path)
        for meshData in data['meshes']:
            newmat = Material("main_mat",
                              "depth.jpg",
                              "normal.jpg",
                              "specular.jpg",
                              "depth.jpg")
            self.meshes.append(Mesh(self, meshData, newmat))
        
        
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
