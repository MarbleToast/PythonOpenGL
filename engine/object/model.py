import os, json, glm
# import numpy as np
from engine.object.mesh import Mesh 
from engine.object.sceneobject import SceneObject
from engine.texture.material import Material
# from engine.core.cache import get_or_load_materials

"""def load_model(path):
    model_data = {
        "vertices": [],
        "texture_coords": [],
        "normals": [],
        "indices": [],
        "materials": [],
        "material_names": [],
        "mesh_count": 0,
        "mesh_list": []
    }

    material_name = None
    
    with open(path) as f:
        for line in f:
            fields = line.split()
            if not fields or line[0] == '#': continue
            if fields[0] == "mtllib":
                model_data["materials"] = get_or_load_materials(fields[1])
                
            elif fields[0] == 'v':
                model_data["vertices"].extend(fields[1:])
            elif fields[0] == "vt":
                model_data["texture_coords"].extend(fields[1:])
            elif fields[0] == "vn":
                model_data["normals"].extend(fields[1:])

            elif fields[0] == "usemtl":
                material_name = fields[1]
                model_data["mesh_count"] += 1
                
            elif fields[0] == "f":
                model_data["indices"].extend([np.uint32(v.split('/')[0])-1 for v in fields[1:]])  
                model_data["mesh_list"].append(model_data["mesh_count"])
                model_data["material_names"].append(material_name)
                
    # Calculate tangents  
    return build_meshes(model_data)

def build_meshes(model_data):
    mesh_id = 1
    meshes = []

    last_mesh_endpoint = 0
    material_name = model_data["material_names"][last_mesh_endpoint]
    
    # For the index of each face in our indices list...
    for index in range(int(len(model_data["indices"])/3)):
        print(index, mesh_id, model_data["mesh_list"][index])
        # If we are moving to a new mesh, create the mesh from the indices 
        # we just went over
        if mesh_id != model_data["mesh_list"][index]:
            meshes.append(Mesh({
                    "indices": model_data["indices"][last_mesh_endpoint:index],
                    "vertices": model_data["vertices"][last_mesh_endpoint:index],
                    "texture_coords": [model_data["texture_coords"][last_mesh_endpoint:index]],
                    "normals": model_data["normals"][last_mesh_endpoint:index],
                    "tangents": np.zeros(len(model_data["normals"]))
                },
                model_data["materials"][material_name]
            ))

            mesh_id = model_data["mesh_list"][index]
            last_mesh_endpoint = index
            material_name = model_data["material_names"][last_mesh_endpoint]
            
    meshes.append(Mesh({
            "indices": model_data["indices"][last_mesh_endpoint:index],
            "vertices": model_data["vertices"][last_mesh_endpoint:index],
            "texture_coords": [model_data["texture_coords"][last_mesh_endpoint:index]],
            "normals": model_data["normals"][last_mesh_endpoint:index],
            "tangents": np.zeros(len(model_data["normals"]))
        },
        model_data["materials"][material_name]
    ))
    
    return meshes
"""

class Model(SceneObject):
    def __init__(self, path, position = None, rotation = None, scale = None):
        if not os.path.exists(path):
            raise RuntimeError(f'Model source file {path} does not exists.')
            
        super().__init__(path, None, position, rotation, scale)   
        
        self.meshes = []

        data = self.load_data(path)
        for meshData in data['meshes']:
            newmat = Material("main_mat",
                              "cube.jpg",
                              "normal.jpg",
                              "specular.jpg",
                              "depth.jpg")
            self.meshes.append(Mesh(meshData, newmat))
        
        
    def load_data(self, path):
        data = None
        with open(path) as file:
            data = json.load(file)
        return data       

    def set_positions(self, positions):
        for mesh in self.meshes:
            mesh.set_positions(positions)
            
    def get_positions(self):
        return self.meshes[0].positions

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
