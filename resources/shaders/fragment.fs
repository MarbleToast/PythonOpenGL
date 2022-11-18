#version 330 core

layout (location = 0) out vec4 FragColor;

in vec3 fragPosition;
in vec3 viewPosition;
in vec3 normal;
in vec2 texCoords;
in vec3 lightPosition;

struct Textures
{
    sampler2D diffuseMap;
    sampler2D normalMap;
    sampler2D specularMap;
    sampler2D depthMap;
    float heightScale;
    float shininess;
};

uniform Textures mat;

void main() {
    vec3 norm = normalize(normal);
    
    // light information
    vec3 lightColour = vec3(0.886, 0.345, 0.133);
    vec3 lightDirection = normalize(lightPosition - vec3(0, 0, 0));  
    
    // ambient lighting
    float ambientLightStrength = 0.2;
    vec3 ambientColour = vec3(1.0, 1.0, 1.0);
    vec3 ambientLighting = ambientLightStrength * ambientColour;
    
    // diffuse lighting
    vec3 diffuseLighting = max(dot(norm, lightDirection), 0.0) * lightColour;
    
    // specular lighting
    float specularLightStrength = 0.5;
    vec3 viewDirection = normalize(viewPosition - fragPosition);
    vec3 reflectDirection = reflect(-lightDirection, norm);  
    vec3 specularLighting = pow(max(dot(viewDirection, reflectDirection), 0.0), 32)
                            * specularLightStrength 
                            * lightColour; 
    
    FragColor = vec4(ambientLighting + diffuseLighting + specularLighting, 1.0) 
                * texture(mat.diffuseMap, texCoords);
} 