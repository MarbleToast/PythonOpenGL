#version 330 core

layout (location = 0) out vec4 FragColor;

in VS_OUT {
    vec3 fragPosition;
    vec2 texCoords;
    vec3 tangentViewPosition;
    vec3 tangentFragPosition;
    vec4 fragPosLightSpace;
    vec3 normal;
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
    vec3 colour;
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
uniform DirectionalLight dirLight;
#define NUM_LIGHT_POINTS 2
uniform PointLight pointLights[NUM_LIGHT_POINTS];
uniform sampler2D shadowMap;

vec2 parallax(vec3 viewDirection);
vec3 addDirectionalLight(DirectionalLight dirLight, vec3 normal, vec3 viewDirection, vec2 coords);
vec3 addPointLight(PointLight dirLight, vec3 normal, vec3 fragPosition, vec3 viewDirection, vec2 coords);
float addDirectionalShadows(DirectionalLight dirLight, vec4 fragPosLightSpace);

void main() {
    vec3 viewDirection = normalize(fs_in.tangentViewPosition - fs_in.tangentFragPosition);
    vec2 parallaxTexCoords = mat.heightScale > 0 ? parallax(viewDirection) : fs_in.texCoords;
    
    vec3 normal = texture(mat.normalMap, parallaxTexCoords).rgb;
    normal = normalize(normal * 2 - 1);
    
    vec3 totalLighting = addDirectionalLight(dirLight, normal, viewDirection, parallaxTexCoords);
    for (int i = 0; i < NUM_LIGHT_POINTS;) {
        totalLighting += addPointLight(pointLights[i], normal, fs_in.fragPosition, viewDirection, parallaxTexCoords);
        ++i;
    }
    
    FragColor = vec4(totalLighting, 1.0);
} 

float addDirectionalShadows(vec3 lightDirection) {
    vec3 projCoords = fs_in.fragPosLightSpace.xyz / fs_in.fragPosLightSpace.w;
    projCoords = projCoords * 0.5 + 0.5;
    float closestDepth = texture(shadowMap, projCoords.xy).r; 
    float currentDepth = projCoords.z;
    
    float bias = max(0.05 * (1.0 - dot(fs_in.normal, lightDirection)), 0.005);
    float shadow = 0.0;
    vec2 texelSize = 1.0 / textureSize(shadowMap, 0);
    for (int x = -1; x <= 1; ++x) {
        for (int y = -1; y <= 1; ++y) {
            float pcfDepth = texture(shadowMap, projCoords.xy + vec2(x, y) * texelSize).r; 
            shadow += currentDepth - bias > pcfDepth ? 1.0 : 0.0;        
        }    
    }
    shadow /= 16.0;
    if (projCoords.z > 1.0)
        shadow = 0.0;
    return shadow;
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
    float shadow = addDirectionalShadows(lightDirection);
    return (ambientLighting + (1.0 - shadow)) * (diffuseLighting + specularLighting);
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
    const float numLayers = 10;
    float layerDepth = 1.0 / numLayers;
    float currentDepth = 0.0;
    vec2 p = viewDirection.xy * mat.heightScale; 
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