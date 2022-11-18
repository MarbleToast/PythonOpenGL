#version 330 core

layout (location = 0) in vec3 aPos;
layout (location = 1) in vec3 aNormal;
layout (location = 2) in vec2 aTexCoords;
layout (location = 3) in vec3 aTangent;
layout (location = 4) in vec3 aInstancePos;

out vec3 fragPosition;
out vec3 viewPosition;
out vec3 normal;
out vec2 texCoords;
out vec3 lightPosition;

uniform mat4 viewProject;
uniform mat4 model;
uniform vec3 viewPos;
uniform vec3 lightPos;

void main() {
    texCoords = aTexCoords;
    lightPosition = lightPos;
    viewPosition = viewPos;
    
    fragPosition = vec3(model * vec4(aPos + aInstancePos, 1.0));
    normal = transpose(inverse(mat3(model))) * aNormal + aInstancePos;
    gl_Position = viewProject * vec4(fragPosition, 1.0);
}