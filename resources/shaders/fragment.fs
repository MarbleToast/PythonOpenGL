#version 330 core

// output is colour of point
layout (location = 0) out vec4 FragColor;

// in interface block passed from vertex shader
in VS_OUT {
    vec3 fragPosition;
    vec2 texCoords;
    vec3 tangentViewPosition;
    vec3 tangentFragPosition;
    vec4 fragPosLightSpace;
    vec3 normal;
    vec3 tangentGlobalLightPosition;
} fs_in;

// material info struct
struct Material {
    sampler2D diffuseMap;
    sampler2D normalMap;
    sampler2D specularMap;
    sampler2D depthMap;
    float heightScale;
    float shininess;
};

// point light struct
struct PointLight {
    vec3 position;
    vec3 ambient;
    vec3 specular;
    vec3 diffuse;
    float constant;
    float linear;
    float quadratic;
};

// global light struct
struct GlobalLight {
    vec3 position;
    vec3 ambient;
    vec3 diffuse;
    vec3 specular;
};


// material uniform
uniform Material mat;

// define lights
// changing length of pointLights allows for more, additive point lights
// Must have same length as lights set, else undefined elements set all lighting to 0
#define NUM_LIGHT_POINTS 1
uniform PointLight pointLights[NUM_LIGHT_POINTS];
uniform GlobalLight globalLight;

// shadow map uniform
uniform sampler2D shadowMap;

// forward declaration of functions
// parallax mapping of tex coords
vec2 parallax(vec3 viewDirection);

// calculate directional lighting
vec3 addDirectionalLight(vec3 normal, vec3 viewDirection, vec2 coords);

// calculate point lighting
vec3 addPointLight(PointLight dirLight, vec3 normal, vec3 fragPosition, vec3 viewDirection, vec2 coords);

// calculate shadows from directional light
float addDirectionalShadows();

void main() {
    // get view direction in tangent space
    vec3 viewDirection = normalize(fs_in.tangentViewPosition - fs_in.tangentFragPosition);
    
    // if material height scale is defined, parallax map the tex coords for better three-dimensionality
    vec2 parallaxTexCoords = mat.heightScale > 0 ? parallax(viewDirection) : fs_in.texCoords;
    
    // get normal at tex coords on material normal map
    vec3 normal = texture(mat.normalMap, parallaxTexCoords).rgb;
    
    // normalise between 0 and 1
    normal = normalize(normal * 2 - 1);
    
    // add together directional and sum of all point lights
    vec3 totalLighting = addDirectionalLight(normal, viewDirection, parallaxTexCoords);
    for (int i = 0; i < NUM_LIGHT_POINTS;) {
        totalLighting += addPointLight(pointLights[i], normal, fs_in.fragPosition, viewDirection, parallaxTexCoords);
        ++i;
    }
    
    // set output to total lighting
    FragColor = vec4(totalLighting, 1.0);
} 

float addDirectionalShadows() {
    // get light direction in world space 
    vec3 lightDirection = normalize(globalLight.position - fs_in.fragPosition);
    
    // divide perspective
    vec3 projCoords = fs_in.fragPosLightSpace.xyz / fs_in.fragPosLightSpace.w;
    
    // normalise coords between 0 and 1
    projCoords = projCoords * 0.5 + 0.5;
    
    // get the closest depth from the shadow map
    float closestDepth = texture(shadowMap, projCoords.xy).r;
    
    // get depth of coords
    float currentDepth = projCoords.z;

    // calculate bias to offset shadow acne
    float bias = max(0.05 * (1.0 - dot(normalize(fs_in.normal), lightDirection)), 0.005);
    
    // percentage-closer filtering
    float shadow = 0.0;
    vec2 texelSize = 1.0 / textureSize(shadowMap, 0);
    for (int x = -1; x <= 1; ++x) {
        for (int y = -1; y <= 1; ++y) {
            float pcfDepth = texture(shadowMap, projCoords.xy + vec2(x, y) * texelSize).r; 
            shadow += currentDepth - bias > pcfDepth ? 1.0 : 0.0;        
        }    
    }
    shadow /= 16;
    
    // fix for oversampling
    if (projCoords.z > 1.0) {
        shadow = 0.0;
    }
 
    return shadow;
}

vec3 addDirectionalLight(vec3 norm, vec3 viewDirection, vec2 coords) {
    // get light direction in tangent space
    vec3 lightDirection = normalize(fs_in.tangentGlobalLightPosition - fs_in.tangentFragPosition);
    
    // calculate diffuse lighting from normal, light direction, material's main texture, and light colour
    vec3 diffuseLighting = max(dot(norm, lightDirection), 0.0)
                       * vec3(texture(mat.diffuseMap, coords))
                       * globalLight.diffuse;
                   
    // calculate Phong-Blinn specular lighting
    // uses material shininess as phong exponent, specular map, and light specular colour
    vec3 halfway = normalize(lightDirection + viewDirection);
    vec3 specularLighting = pow(max(dot(viewDirection, halfway), 0.0), mat.shininess)
                        * vec3(texture(mat.specularMap, coords))
                        * globalLight.specular;

    // calculate ambient lighting from diffuse map and light ambient colour
    vec3 ambientLighting = globalLight.ambient * vec3(texture(mat.diffuseMap, coords));
    
    // calculate shadows
    float shadow = addDirectionalShadows();
    
    // return big old sum of lighting colours, using shadow as modifier for ambient colour
    return (ambientLighting + (1.0 - shadow) * (diffuseLighting + specularLighting));
}

vec3 addPointLight(PointLight pointLight, vec3 norm, vec3 fragPosition, vec3 viewDirection, vec2 coords) {
    // get light direction
    vec3 lightDirection = normalize(pointLight.position - fragPosition);
    
    // calculate distance of point from light source
    float distance = length(pointLight.position - fragPosition);
    
    // calculate attenuation from light falloff values
    float attenuation = 1.0 / (pointLight.constant + pointLight.linear * distance + 
  			     pointLight.quadratic * (distance * distance));    
    
    // calculate diffuse lighting
    // uses normal, light direction, material's main texture, light colour, and attenuation
    vec3 diffuseLighting = max(dot(norm, lightDirection), 0.0)
                           * vec3(texture(mat.diffuseMap, coords))
                           * pointLight.diffuse
                           * attenuation;

    // calculate Phong-Blinn specular lighting
    // uses material shininess as phong exponent, specular map, light specular colour, and attenuation
    vec3 halfway = normalize(lightDirection + viewDirection);
    vec3 specularLighting = pow(max(dot(viewDirection, halfway), 0.0), mat.shininess)
                            * vec3(texture(mat.specularMap, coords))
                            * pointLight.specular
                            * attenuation;

    // calculate ambient lighting from diffuse map, light ambient colour, and attenuation
    vec3 ambientLighting = pointLight.ambient * vec3(texture(mat.diffuseMap, coords)) * attenuation;

    // return sum of lighting
    return diffuseLighting + ambientLighting + specularLighting;
}

vec2 parallax(vec3 viewDirection) {
    // calculate offset in specific tex coord depending on depth map value and view direction
    
    // find number of displacement layers based on our viewing angle
    // more perpendicular means less layers, as the algorithm needs to do less work for a convincing effect
    const float minLayers = 8;
    const float maxLayers = 32;
    float numLayers = mix(maxLayers, minLayers, max(dot(vec3(0, 0, 1), viewDirection), 0)); 
    
    // we have our layers with a total depth of 1. according to the height scale of the material,
    // we find the coord shift based on vector P and the number of layers
    float layerDepth = 1 / numLayers;
    float currentDepth = 0;
    vec2 p = viewDirection.xy * mat.heightScale; 
    vec2 coordShift = p / numLayers;
    
    // set initial values of the map and tex coords
    vec2 currentTexCoords = fs_in.texCoords;
    float currentMapValue = texture(mat.depthMap, currentTexCoords).r;
      
    // for each layer, starting at the top, we gradually offset the tex coord until we hit
    // a point in the depth map that would displace us lower than the current depth.
    
    // while out current depth is lower than the map value...
    while(currentDepth < currentMapValue) {
        // shift our tex coords by the amount derived
        currentTexCoords -= coordShift;
        
        // find the depth map value of that new position
        currentMapValue = texture(mat.depthMap, currentTexCoords).r;  
        
        // get depth of the next layer
        currentDepth += layerDepth;  
    }
    
    // parallax occlusion mapping
    // we linearly interpolate between depth before and after shifting our coords at each layer
    vec2 prevTexCoords = currentTexCoords + coordShift;
    float afterDepth = currentMapValue - currentDepth;
    float beforeDepth = texture(mat.depthMap, prevTexCoords).r - currentDepth + layerDepth;
    float weight = afterDepth / (afterDepth - beforeDepth);
    vec2 finalTexCoords = prevTexCoords * weight + currentTexCoords * (1.0 - weight);
    
    // shifted coords have a depth to them generated entirely by shifting positions
    return finalTexCoords;  
}