import resource_cache
import numpy as np

class Model:
    def __init__(self, filename):
        self.filename = filename
        self._process_node(resource_cache.get_or_load_model(filename))
        
    def _process_node(self, obj):
        vertices = np.array(obj.vertices, dtype='f')
        faces = np.array([[face for face in mesh.faces] for mesh in obj.mesh_list], dtype=np.int32)
        print(faces, vertices)
        