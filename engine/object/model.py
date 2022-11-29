import os
import json
import glm
from engine.object.mesh import Mesh 
from engine.object.sceneobject import SceneObject
from engine.texture.material import Material
from engine.core.program import ShaderProgram

"""
Model

Inherits from SceneObject.
Loads model JSON object from file, and creates and stores meshes.
"""
class Model(SceneObject):
    def __init__(self, path: str, materials: list[Material] = None):
        """
        Calls superclass constructor, loads data from path, and creates meshes
        with given materials.

        Parameters
        ----------
        path : str
            The path for the model file
        materials : list[Material], optional
            A list of materials, where the mesh's materialindex will fetch the
            element of the same index in this list. The default is None.

        Raises
        ------
        RuntimeError
            If the given path does not exist.

        Returns
        -------
        None.

        """
        
        if not os.path.exists(path):
            raise RuntimeError(f'Model source file {path} does not exist.')
            
        # Call SceneObject constructor
        super().__init__(path)   
        
        # Initialise empty meshes list
        self.meshes = []

        # Load data
        data = self.load_data(path)
        
        # Iterate through meshes
        for mesh_data in data['meshes']:
            
            # If we have materials supplied, and the mesh has a materialindex,
            # use the supplied material at that index
            if materials and "materialindex" in mesh_data:
                self.meshes.append(Mesh(self, mesh_data, materials[mesh_data["materialindex"]]))
            else:
                # Otherwise use a default material
                default = Material(
                    "diffuse.jpg",
                    "normal.jpg",
                    "specular.jpg",
                    "depth.jpg",
                    height_scale=0.12
                )
                self.meshes.append(Mesh(self, mesh_data, default))
        
    def load_data(self, path: str) -> dict:
        """
        Load dictionary of model from JSON source file.

        Parameters
        ----------
        path : str
            The path to the JSON source file

        Returns
        -------
        dict
            The loaded JSON as a Python dict.

        """
        
        # We use JSON as our file format as it is much more interpretable, both
        # for human inspection and in file loading. We use Assimp2JSON, a CLI
        # command to convert OBJs to JSON files, which also computes certain
        # elements not found in OBJs by default.
        data = None
        with open(path) as file:
            data = json.load(file)
        return data       

    def set_transforms(self, transforms: list[dict[str, glm.vec3]]):
        """
        Sets the transforms of each mesh in the model.
        Each transform must be a dict of the following shape:
            
                {
                    position: glm.vec3,
                    rotation: glm.vec3,
                    scale: glm.vec3
                }


        Parameters
        ----------
        transforms : list[dict[str, glm.vec3]]
            The list of transforms.

        Returns
        -------
        None.

        """
        
        for mesh in self.meshes:
            mesh.set_transforms(transforms)

    def draw(self, program: ShaderProgram):
        """
        Draw each mesh in the model with a given shader.

        Parameters
        ----------
        program : ShaderProgram
            The shader to draw each mesh with.

        Returns
        -------
        None.

        """
        
        for mesh in self.meshes:
            mesh.draw(program)

    def __del__(self):
        """
        On delete, clear the meshes array.

        Returns
        -------
        None.

        """
        
        self.meshes.clear()
