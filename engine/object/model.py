import os, json, glm
from engine.object.mesh import Mesh 
from engine.object.sceneobject import SceneObject
from engine.texture.material import Material

class Model(SceneObject):
    def __init__(self, path, position = None, rotation = None, scale = None):
        if not os.path.exists(path):
            raise RuntimeError(f'Model source file {path} does not exists.')
        
        super().__init__(path, None, position, rotation, scale)
        self.meshes = []
        
        self.path = path

        data = self.load_data()
        for meshData in data['meshes']:
            newmat = Material("main_mat",
                              "resources/textures/diffuse.jpg",
                              "resources/textures/normal.jpg",
                              "resources/textures/specular.jpg",
                              "resources/textures/depth.jpg")
            self.meshes.append(Mesh(meshData, newmat))

    def load_data(self):
        data = None
        with open(self.path) as file:
            data = json.load(file)
        return data

    def set_positions(self, positions):
        for mesh in self.meshes:
            mesh.set_positions(positions)

    def draw(self, program):
        program.use()
        
        model = glm.mat4()
        model = glm.translate(model, self.position);
        model = glm.rotate(model, self.rotation.x, self.up)
        model = glm.rotate(model, self.rotation.y, self.right)
        model = glm.scale(model, self.scale)
        program.setMat4('model', model)
        
        for mesh in self.meshes:
            mesh.draw(program)

    def __del__(self):
        self.meshes.clear()
