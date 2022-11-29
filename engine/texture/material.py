from engine.core.cache import get_or_load_texture

"""
Material

Holds texture and exponent information
"""
class Material:
    def __init__(
        self,
        diffuse_path: str,
        normal_path: str = None,
        specular_path: str = None,
        displacement_path: str = None,
        shininess: int = 64,
        height_scale: float = 0
    ):
        """
        Loads each texture specified (if unloaded), and sets exponents.

        Parameters
        ----------
        diffuse_path : str
            The path to the diffuse texture file
        normal_path : str, optional
            The path to the normal texture file. The default is None.
        specular_path : str, optional
            The path to the specular texture file. The default is None.
        displacement_path : str, optional
            The path to the depth/displacement texture file. The default is None.
        shininess : int, optional
            Specular exponent. The default is 64.
        height_scale : float, optional
            Height scale for parallax mapping. 0 will result in no parallax mapping. The default is 0.

        Returns
        -------
        None.

        """
        
        self.diffuse = get_or_load_texture(diffuse_path)
        
        # All non-diffuse maps may be undefined, so set None if a path is not
        # passed
        self.normal = get_or_load_texture(normal_path) if normal_path else None
        self.specular = get_or_load_texture(specular_path) if specular_path else None
        self.depth = get_or_load_texture(displacement_path) if displacement_path else None
        
        # Set other properties
        self.shininess = shininess
        self.height_scale = height_scale
