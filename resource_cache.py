import pywavefront
import logging
import os

ModelCache = {}

def get_or_load_model(filename: str):
    logging.info(f"Attempting to load {filename}")
    
    if filename in ModelCache.keys():
        return ModelCache[filename]
    
    path = os.path.join(os.path.dirname(__file__), filename)
    
    model = pywavefront.Wavefront(path, collect_faces=True)
    if not model:
        logging.error(f"Failed to load {filename}")
        
    ModelCache[filename] = model
    return model
