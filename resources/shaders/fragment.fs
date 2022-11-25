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

struct DirectionalLight {
    vec3 direction;
    vec3 ambient;
    vec3 specular;
    vec3 diffuse;
};

struct PointLight {
    vec3 position;
    vec3 ambient;
    vec3 specular;
    vec3 diffuse;
    float constant;
    float linear;
    float quadratic;
};

uniform Material mat;
uniform DirectionalLight directionalLight;
#define NUM_LIGHT_POINTS 2
uniform PointLight pointLights[NUM_LIGHT_POINTS];

vec2 parallax(vec3 viewDirection);
vec3 addDirectionalLight(DirectionalLight dirLight, vec3 normal, vec3 viewDirection, vec2 coords);
vec3 addPointLight(PointLight dirLight, vec3 normal, vec3 fragPosition, vec3 viewDirection, vec2 coords);

void main() {
    vec3 viewDirection = normalize(fs_in.tangentViewPosition - fs_in.tangentFragPosition);
    vec2 parallaxTexCoords = mat.heightScale > 0 ? parallax(viewDirection) : fs_in.texCoords;
    vec3 norm = texture(mat.normalMap, parallaxTexCoords).rgb;
    norm = normalize(norm * 2 - 1);
    
    vec3 totalLighting = addDirectionalLight(directionalLight, norm, viewDirection, parallaxTexCoords);
    for (int i = 0; i < NUM_LIGHT_POINTS; i++) {
        totalLighting += addPointLight(pointLights[i], norm, fs_in.tangentFragPosition, viewDirection, parallaxTexCoords);
    }
    
    FragColor = vec4(totalLighting, 1.0);
}

vec3 addDirectionalLight(DirectionalLight dirLight, vec3 norm, vec3 viewDirection, vec2 coords) {
    vec3 lightDirection = normalize(-dirLight.direction);
    
    vec3 diffuseLighting = max(dot(norm, lightDirection), 0.0)
                           * vec3(texture(mat.diffuseMap, coords))
                           * dirLight.diffuse;
                           
    vec3 halfway = normalize(lightDirection + viewDirection);  
    vec3 specularLighting = pow(max(dot(viewDirection, halfway), 0.0), mat.shininess)
                            * vec3(texture(mat.specularMap, coords))
                            * dirLight.specular;
    
    vec3 ambientLighting = dirLight.ambient * vec3(texture(mat.diffuseMap, coords));
    
    return diffuseLighting + ambientLighting + specularLighting;
}

vec3 addPointLight(PointLight pointLight, vec3 norm, vec3 fragPosition, vec3 viewDirection, vec2 coords) {
    vec3 lightDirection = normalize(pointLight.position - fragPosition);
    float distance = length(pointLight.position - fragPosition);
    float attenuation = 1.0 / (pointLight.constant + pointLight.linear * distance + 
  			     pointLight.quadratic * (distance * distance));    
  			     
    vec3 diffuseLighting = max(dot(norm, lightDirection), 0.0)
                           * vec3(texture(mat.diffuseMap, coords))
                           * pointLight.diffuse
                           * attenuation;
                           
    vec3 halfway = normalize(lightDirection + viewDirection);
    vec3 specularLighting = pow(max(dot(viewDirection, halfway), 0.0), mat.shininess)
                            * vec3(texture(mat.specularMap, coords))
                            * pointLight.specular
                            * attenuation;
                            
    vec3 ambientLighting = pointLight.ambient * vec3(texture(mat.diffuseMap, coords)) * attenuation;

    return diffuseLighting + ambientLighting + specularLighting;
}

vec2 parallax(vec3 viewDirection) {
    const float minLayers = 4;
    const float maxLayers = 32;
    float numLayers = mix(maxLayers, minLayers, abs(dot(vec3(0.0, 0.0, 1.0), viewDirection)));  
    float layerDepth = 1.0 / numLayers;
    float currentDepth = 0.0;
    vec2 p = viewDirection.xy / viewDirection.z * mat.heightScale; 
    vec2 coordShift = p / numLayers;
    
    vec2 currentTexCoords = fs_in.texCoords;
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