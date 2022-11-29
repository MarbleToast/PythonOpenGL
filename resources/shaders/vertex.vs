#version 330 core

// VBOs being passed in
layout (location = 0) in vec3 aPos;
layout (location = 1) in vec3 aNormal;
layout (location = 2) in vec2 aTexCoords;
layout (location = 3) in vec3 aTangent;
layout (location = 4) in vec3 aBitangent;

// VS_OUT interface block
out VS_OUT {
    vec3 fragPosition;
    vec2 texCoords;
    vec3 tangentViewPosition;
    vec3 tangentFragPosition;
    vec4 fragPosLightSpace;
    vec3 normal;
    vec3 tangentGlobalLightPosition;
} vs_out;

// Global light struct
struct GlobalLight {
    vec3 position;
    vec3 ambient;
    vec3 diffuse;
    vec3 specular;
};

uniform mat4 viewProject; // View * Projection matrix
uniform mat4 model; // Transformation matrix for the current object
uniform vec3 viewPos; // Position vector of camera
uniform mat4 lightSpaceMatrix; // Light space matrix from global light
uniform GlobalLight globalLight; // Global light information

void main() {
    
    // Pass simple outs
    // pass current tex coords
    vs_out.texCoords = aTexCoords;
    
    // pass frag position as model matrix * vertex position
    vs_out.fragPosition = vec3(model * vec4(aPos, 1.0));
    
    // pass normal as model (cast down, inverted, and transposed) * normal
    vs_out.normal = transpose(inverse(mat3(model))) * aNormal;
    
    // build tangent-bitangent-normal matrix for converting vectors to tangent space
    vec3 T = normalize(vec3(model * vec4(aTangent, 0.0)));
    vec3 B = normalize(vec3(model * vec4(aBitangent, 0.0)));
    vec3 N = normalize(vec3(model * vec4(aNormal, 0.0)));
    mat3 TBN = transpose(mat3(T, B, N));
    
    // pass tangent frag, view, and global light positions for normal mapping
    vs_out.tangentViewPosition = TBN * viewPos;
    vs_out.tangentFragPosition = TBN * vs_out.fragPosition;
    vs_out.tangentGlobalLightPosition = TBN * globalLight.position;
    
    // pass frag position * light space matrix for shadow calculation
    vs_out.fragPosLightSpace = lightSpaceMatrix * vec4(vs_out.fragPosition, 1.0);
    
    // set overall vertex position as view * projection * model
    gl_Position = viewProject * vec4(vs_out.fragPosition, 1.0);
}