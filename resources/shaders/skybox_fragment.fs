#version 330 core
out vec4 FragColor;

in vec3 texCoords;

uniform samplerCube skybox;

void main() {    
    FragColor = vec4(1, 1, 1, 1);
}