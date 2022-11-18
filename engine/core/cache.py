# import numpy as np
from engine.texture.texture import Texture
# from engine.texture.material import Material
from OpenGL.GL import GL_TEXTURE_2D

# Textures can and should be reused between materials

TEXTURE_CACHE = {}

def get_or_load_texture(path: str):
    if not path in TEXTURE_CACHE.keys():
        TEXTURE_CACHE[path] = Texture(path, GL_TEXTURE_2D)
    
    return TEXTURE_CACHE[path]


"""MATERIAL_CACHE: dict[str, dict[str, Material]] = {}

def get_or_load_materials(path: str):
    if not path in MATERIAL_CACHE.keys():
        MATERIAL_CACHE[path] = process_material_library(path)
    
    return MATERIAL_CACHE[path]

def get_or_load_material(path: str):
    if not path in MATERIAL_CACHE.keys():
        MATERIAL_CACHE[path] = process_material_library(path)
    
    return MATERIAL_CACHE[path].values()

def process_material_library(lib_name):
    materials = {}
    current_material = None
    with open(f"resources/models/{lib_name}") as library:
        for line in library:
            fields = line.split()
            if not fields or line[0] == '#': continue
            if fields[0] == "newmtl":
                if current_material is not None:
                    materials[fields[1]] = current_material
                current_material = Material(fields[1])
            elif fields[0] == 'Ka':
                current_material.Ka = np.array(fields[1:], 'f')
            elif fields[0] == 'Kd':
                current_material.Kd = np.array(fields[1:], 'f')
            elif fields[0] == 'Ks':
                current_material.Ks = np.array(fields[1:], 'f')
            elif fields[0] == 'Ke':
                current_material.Ke = np.array(fields[1:], 'f')
                
            elif fields[0] == 'Ns':
                current_material.Ns = float(fields[1])
            elif fields[0] == 'd':
                current_material.d = float(fields[1])
            elif fields[0] == 'Tr':
                current_material.d = 1.0 - float(fields[1])
            elif fields[0] == 'illum':
                current_material.illumination = int(fields[1])
                
            elif fields[0] == 'map_Kd':
                current_material.diffuse = get_or_load_texture(fields[1])
            elif fields[0] == 'map_Ks':
                current_material.depth = get_or_load_texture(fields[1])
            elif fields[0] == 'map_bump':
                current_material.normal = get_or_load_texture(fields[1])
            elif fields[0] == 'map_Ka':
                current_material.specular = get_or_load_texture(fields[1])
                
    materials[current_material.path] = current_material
    return materials"""