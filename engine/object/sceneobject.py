import glm
import logging
import engine.constants as constants

from math import sin, cos, radians

"""
SceneObject

Base object for renderables in a scene. Holds axis and transform vectors.
"""
class SceneObject:
    def __init__(self, name: str, position: glm.vec3 = None, rotation: glm.vec3 = None, scale: glm.vec3 = None):
        """
        Initialises scene object transform and axis vectors.

        Parameters
        ----------
        name : str
            The name of the object, for use in logging
        position : glm.vec3, optional
            The initial position of the object. The default is None.
        rotation : glm.vec3, optional
            The initial rotation of the object. The default is None.
        scale : glm.vec3, optional
            The initial scale of the object. The default is None.

        Returns
        -------
        None.

        """
        
        logging.info(f"Instantiating scene object {name}")
        self.name = name
        
        # For each transform vector, if none was passed, set it to a default.
        if position == None:
            self.position = glm.vec3(0., 0., 0.)
        else:
            self.position = position

        if rotation == None:
            self.rotation = glm.vec2(0., 0.)
        else:
            self.rotation = rotation
            
        if scale == None:
            self.scale = glm.vec3(1., 1., 1.)
        else:
            self.scale = scale
            
        # Update axis vectors
        self.update_vectors()
        
    def update_vectors(self):
        """
        Updates axis vectors for the object.

        Returns
        -------
        None.

        """
        
        # Get direction vector from yaw and pitch Euler angles
        x = cos(radians(self.rotation.x)) * cos(radians(self.rotation.y))
        y = sin(radians(self.rotation.y))
        z = sin(radians(self.rotation.x)) * cos(radians(self.rotation.y))
        
        self.front = glm.normalize(glm.vec3(x, y, z))
        
        # Cross the direction vector with global world up vector to get 
        # the right vector
        self.right = glm.normalize(glm.cross(self.front, constants.WORLD_UP))
        
        # Cross the right and direction vectors to get local up vector
        self.up = glm.normalize(glm.cross(self.right, self.front))