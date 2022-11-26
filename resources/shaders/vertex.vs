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
    vec4 fragPosLightSpace;
    vec3 normal;
} vs_out;

uniform mat4 viewProject;
uniform mat4 model;
uniform vec3 viewPos;
uniform mat4 lightSpaceMatrix;

void main() {
    vs_out.texCoords = aTexCoords;
    vs_out.fragPosition = vec3(model * vec4(aPos, 1.0));
    
    vs_out.normal = transpose(inverse(mat3(model))) * aNormal;
    
    vec3 T = normalize(vec3(model * vec4(aTangent, 0.0)));
    vec3 B = normalize(vec3(model * vec4(aBitangent, 0.0)));
    vec3 N = normalize(vec3(model * vec4(aNormal, 0.0)));
    mat3 TBN = transpose(mat3(T, B, N));
    
    vs_out.tangentViewPosition = TBN * viewPos;
    vs_out.tangentFragPosition = TBN * vs_out.fragPosition;
    vs_out.fragPosLightSpace = lightSpaceMatrix * vec4(vs_out.fragPosition, 1.0);
    
    gl_Position = viewProject * vec4(vs_out.fragPosition, 1.0);
}