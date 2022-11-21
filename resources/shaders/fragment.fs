#version 330 core

layout (location = 0) out vec4 FragColor;

in VS_OUT {
    vec3 fragPosition;
    vec2 texCoords;
    vec3 tangentViewPosition;
    vec3 tangentFragPosition;
} fs_in;

struct Material {
    sampler2D diffuseMap;
    sampler2D normalMap;
    sampler2D specularMap;
    sampler2D depthMap;
    float heightScale;
    float shininess;
};

struct Light {
    vec3 direction;
    vec3 colour;
};

uniform Material mat;
uniform Light light;

vec2 parallax(vec2 texCoords, vec3 viewDirection);

void main() {
    vec3 viewDirection = normalize(fs_in.tangentViewPosition - fs_in.tangentFragPosition);
    vec2 parallaxTexCoords = parallax(fs_in.texCoords, viewDirection);
    
    vec3 norm = texture(mat.normalMap, parallaxTexCoords).rgb;
    norm = normalize(norm * 2 - 1);
    
    // light information
    vec3 lightColour = vec3(0.886, 0.345, 0.133);
    vec3 lightDirection = normalize(-light.direction);
    
    // ambient lighting
    float ambientLightStrength = 0;
    vec3 ambientColour = vec3(1.0, 1.0, 1.0);
    vec3 ambientLighting = ambientLightStrength * ambientColour;
    
    // diffuse lighting
    vec3 diffuseLighting = max(dot(norm, lightDirection), 0.0) 
                           * lightColour
                           * vec3(texture(mat.diffuseMap, parallaxTexCoords));
    
    // specular lighting (Blinn-Phong)
    vec3 halfway = normalize(lightDirection + viewDirection);  
    vec3 specularLighting = pow(max(dot(viewDirection, halfway), 0.0), mat.shininess) 
                            * lightColour 
                            * vec3(texture(mat.specularMap, parallaxTexCoords));
    
    FragColor = vec4(ambientLighting + diffuseLighting + specularLighting, 1.0);
} 

vec2 parallax(vec2 texCoords, vec3 viewDirection) {
    const float numLayers = 10;
    float layerDepth = 1.0 / numLayers;
    float currentDepth = 0.0;
    vec2 p = viewDirection.xy * mat.heightScale; 
    vec2 coordShift = p / numLayers;
    
    vec2 currentTexCoords = texCoords;
    float currentMapValue = texture(mat.depthMap, currentTexCoords).r;
      
    while(currentDepth < currentMapValue) {
        currentTexCoords -= coordShift;
        currentMapValue = texture(mat.depthMap, currentTexCoords).r;  
        currentDepth += layerDepth;  
    }
    
    vec2 prevTexCoords = currentTexCoords + coordShift;
    float afterDepth = currentMapValue - currentDepth;
    float beforeDepth = texture(mat.depthMap, prevTexCoords).r - currentDepth + layerDepth;
    float weight = afterDepth / (afterDepth - beforeDepth);
    vec2 finalTexCoords = prevTexCoords * weight + currentTexCoords * (1.0 - weight);
    
    return finalTexCoords;  
}