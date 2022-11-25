class DirectionalLight:
    def __init__(self, direction, ambient, specular, diffuse):
        self.direction = direction
        self.ambient = ambient
        self.diffuse = diffuse
        self.specular = specular
        
class PointLight:
    def __init__(self, position, ambient, diffuse, specular, constant, linear, quadratic):
        self.position = position
        self.ambient = ambient
        self.diffuse = diffuse
        self.specular = specular
        self.constant = constant
        self.linear = linear
        self.quadratic = quadratic