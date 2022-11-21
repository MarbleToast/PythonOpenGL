#version 330 core

layout (location = 0) in vec3 aPos;
layout (location = 1) in vec3 aNormal;
layout (location = 2) in vec2 aTexCoords;
layout (location = 3) in vec3 aTangent;
layout (location = 4) in vec3 aBitangent;

out VS_OUT {
    vec3 fragPosition;
    vec2 texCoords;
    vec3 tangentViewPosition;
    vec3 tangentFragPosition;
} vs_out;

uniform mat4 viewProject;
uniform mat4 model;
uniform vec3 viewPos;

void main() {
    vs_out.texCoords = aTexCoords;
    vs_out.fragPosition = vec3(model * vec4(aPos, 1.0));
    
    mat3 normalMatrix = transpose(inverse(mat3(model)));
    
    vec3 T = normalize(normalMatrix * aTangent);
    vec3 B = normalize(normalMatrix * aBitangent);
    vec3 N = normalize(normalMatrix * aNormal);
    mat3 TBN = transpose(mat3(T, B, N));
    
    vs_out.tangentViewPosition = TBN * viewPos;
    vs_out.tangentFragPosition = TBN * vs_out.fragPosition;
    
    gl_Position = viewProject * vec4(vs_out.fragPosition, 1.0);
}