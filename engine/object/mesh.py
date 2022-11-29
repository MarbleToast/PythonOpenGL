import glm
import logging
import numpy as np
from OpenGL.GL import *
from engine.texture.material import Material
from engine.core.program import ShaderProgram

"""
Mesh

Creates and stores VAO and VBO data, and manages rendering, for each mesh
"""
class Mesh:
    def __init__(self, parent, data: dict, material: Material):
        """
        Initialises mesh properties, then calls to bind the mesh. 

        Parameters
        ----------
        parent : Model
            The parent model
        data : dict
            Dictionary passed from the model for this mesh containing all data
        material : Material
            The material and textures with which to render this mesh.

        Returns
        -------
        None.

        """
        
        # The JSON format captures vertex indices in a 2D array, so we unpack
        self.indices = np.array(data['faces']).flatten()
        self.vertices = np.array(data['vertices'], dtype=np.float32)
        self.normals = np.array(data['normals'], dtype=np.float32)
        
        # The JSON format may not contain texturecoords, tangents, or bitangents
        self.texCoords = np.array(data['texturecoords'], dtype=np.float32) if "texturecoords" in data else np.array([])
        self.tangents = np.array(data['tangents'], dtype=np.float32) if "tangents" in data else np.array([])
        self.bitangents = np.array(data['bitangents'], dtype=np.float32) if "bitangents" in data else np.array([])
        
        # Initialise transforms as empty to start
        self.transforms = np.array([])
        
        self.material = material

        self.parent = parent
        
        self.VAO = 0
        self.VBOs = {}
        
        self.bind()
        
    def bind(self):
        """
        Generates the VAO, VBOs, and EBO to store the mesh information

        Returns
        -------
        None.

        """
        
        logging.info(f"Generating and binding VAO and VBOs for mesh in {self.parent.name}")
        
        # Generate and bind new VAO
        self.VAO = glGenVertexArrays(1)
        glBindVertexArray(self.VAO)
        
        # Generate and bind EBO, then fill it with the mesh's indices
        # GL_STATIC_DRAW is used as the indices themselves won't change
        self.EBO = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.EBO)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, self.indices, GL_STATIC_DRAW)
        
        # Generate, bind, and fill each VBO, with vector sizes given
        self.bindVBO("pos", self.vertices, 3)
        self.bindVBO("aNormal", self.normals, 3)
        self.bindVBO("aTexCoords", self.texCoords, 2)
        self.bindVBO("aTangent", self.tangents, 3)
        self.bindVBO("aBitangent", self.bitangents, 3)
        
        # Unbind VAO and VBO (optional)
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)
        
    def genVBO(self, name: str) -> (int, int):
        """
        Generates a VBO and store a reference in the mesh's VBO dictionary. 
        Parameters
        ----------
        name : str
            The name of the VBO

        Returns
        -------
        (int, int)
            Reference to the buffer object itself, and the location to use in
            shader layout declarations (ie, layout (location = _) in vec3 aPos).

        """
        
        # Generate and store buffer
        self.VBOs[name] = glGenBuffers(1)
        return self.VBOs[name], list(self.VBOs.keys()).index(name)  
    
    def bindVBO(self, name: str, data: np.array, size: int):
        """
        Handles for binding a VBO, filling it with data, and setting the
        properties of attributes its location for use in shaders

        Parameters
        ----------
        name : str
            The name of the VBO to be generated
        data : np.array
            The data to be stored in the VBO. Must be an np.array, as PyOpenGL
            does not support Python lists.
        size : int
            Size of the attribute. Must be 1 to 4.

        Returns
        -------
        None.

        """
        
        # Generate VBO, get its handle and location in dictionary
        vBO, location = self.genVBO(name)
    
        # Bind VBO, fill VBO. We use GL_STATIC_DRAW to state the contents of
        # the buffer will not change. For instanced rendering (as was here
        # before removal), whereby the locations/transforms of objects, and by
        # extension the VBO contents, could change, use GL_DYNAMIC_DRAW.
        glBindBuffer(GL_ARRAY_BUFFER, vBO)
        glBufferData(GL_ARRAY_BUFFER, data, GL_STATIC_DRAW)
        
        # Specify location, size, and type of currently bound VBO
        glVertexAttribPointer(location,
                              size,
                              GL_FLOAT,
                              False,
                              0,
                              None)
        
        # Enable the attribute array at the location
        glEnableVertexAttribArray(location)

    def set_transforms(self, transforms: list[dict[str, glm.vec3]]):
        """
        Set the mesh's transforms. 
        Each transform must be a dict of the following shape:
            
                {
                    position: glm.vec3,
                    rotation: glm.vec3,
                    scale: glm.vec3
                }

        Parameters
        ----------
        transforms : list[dict[str, glm.vec3]]
            The list of transformation dicts

        Returns
        -------
        None.

        """
        
        self.transforms = np.array(transforms)
    
    def draw(self, program: ShaderProgram):
        """
        Draws the mesh with the given shader program.

        Parameters
        ----------
        program : ShaderProgram
            The shader program to use

        Returns
        -------
        None.

        """
        
        # First step: iterate through the textures of the material (for where
        # they exist) and bind them to texture units. We then inform the shader
        # being used to draw the mesh the texture unit to use for each texture.
        
        glActiveTexture(GL_TEXTURE1)
        program.setInt('mat.diffuseMap', 1)
        self.material.diffuse.bind()
        
        if self.material.normal:
            glActiveTexture(GL_TEXTURE2)
            program.setInt('mat.normalMap', 2)
            self.material.normal.bind()

        if self.material.specular:
            glActiveTexture(GL_TEXTURE3)
            program.setInt('mat.specularMap', 3)
            self.material.specular.bind()
                
        if self.material.depth:
            glActiveTexture(GL_TEXTURE4)
            program.setInt('mat.depthMap', 4)
            self.material.depth.bind()
            
        # We also set specular exponent and parallax height scale in the shader
        program.setFloat('mat.shininess', self.material.shininess)
        program.setFloat('mat.heightScale', self.material.height_scale)
        
        # Bind VAO to begin rendering
        glBindVertexArray(self.VAO)
        
        # For each transform...
        for trf in self.transforms:
            # We construct a model matrix from the transform.
            model = glm.mat4()
            model = glm.translate(model, trf["position"]);
            model = glm.rotate(model, trf["rotation"].x, self.parent.up)
            model = glm.rotate(model, trf["rotation"].y, self.parent.right)
            model = glm.scale(model, trf["scale"])
            
            # Set the completed model matrix in the shader
            program.setMat4('model', model)
            
            # Draw!
            glDrawElements(GL_TRIANGLES, len(self.indices), GL_UNSIGNED_INT, None)
            
        # As a side note, this could be replaced by instanced rendering when
        # the number of transforms are high, and in fact it used to be used for
        # all rendering. For a smaller demo scene, however, I realised there was
        # a performance hit.
        
        # Manually setting the model uniform in the shader is also inefficient.
        # In future, this could be replaced with a Uniform Buffer Object of
        # model matrices, but implementing this using 4x4 matrices as the data
        # type was difficult and too time consuming.
            

    def __del__(self):
        """
        On all references descoping, delete the VAO, EBO, and all VBOs.

        Returns
        -------
        None.

        """
        try:
            glDeleteVertexArrays(1, self.VAO)
            glDeleteBuffers(1, self.EBO)
            for name in list(self.VBOs.keys()):
                glDeleteBuffers(1, self.VBOs.pop(name))
        except:
            pass 