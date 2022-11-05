import glm
from OpenGL.GL import *
from engine.object.camera import Camera

class Scene:
    def __init__(self, path, perspective):
        self.path = path
        self.camera = Camera()
        self.objects = []
        self.light_position = glm.vec3(10, 100, 0)
        self.perspective = perspective
        
    def load_from_file(self):
        pass
        
    def add_object(self, object):
        self.objects.append(object)
        
    def update(self, window, dt):
        self.camera.update(window, dt)
        
    def draw(self, program):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glClearColor(0.1, 0.2, 0.8, 1)
        
        program.use()
        program.setMat4('viewProject', self.perspective * self.camera.get_view())
        program.setVec3('viewPos', self.camera.position)
        program.setVec3('lightPos', self.light_position)
        
        program.setFloat('mat.shininess', 128)
        program.setFloat('mat.heightScale', 0.12)
        for obj in self.objects:
            obj.draw(program)
        

