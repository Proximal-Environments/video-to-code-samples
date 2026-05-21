# Shaders

_Note: These docs were adopted from the original Motion Canvas docs_

Shaders allow you to apply custom effects to any node using WebGL.

**Experimental**

This is an experimental feature. The behavior and API may change drastically between minor releases.

### Basic Usage

Shaders can be specified using the `shaders` property. In the simplest case, the value should be a string containing the GLSL code for the fragment shader:

```typescript
import myShader from './myShader.glsl';

//...
view.add(
  <Circle
    size={200}
    fill="lightseagreen"
    shaders={myShader}
  />,
);
```

Below is an example of a simple shader that inverts the colors of the node:

**myShader.glsl**
```glsl
#version 300 es
precision highp float;

#include "@revideo/core/shaders/common.glsl"

void main() {
    outColor = texture(sourceTexture, sourceUV);
    outColor.rgb = 1.0 - outColor.rgb;
}
```

### GLSL Preprocessor

Motion Canvas comes with a simple GLSL preprocessor that lets you include files using the `#include` directive:

```glsl
#include "path-to-file"
```

The path is resolved using the same rules as `import` statements in JavaScript. It can point to a relative file:

```glsl
#include "../utils/math.glsl"
```

Or to a file from another package:

```glsl
#include "@revideo/core/shaders/common.glsl"
```

### Default Uniforms

The following uniforms are available in all shaders:

```glsl
in vec2 screenUV;
in vec2 sourceUV;
in vec2 destinationUV;
out vec4 outColor;
uniform float time;
uniform float deltaTime;
uniform float framerate;
uniform int frame;
uniform vec2 resolution;
uniform sampler2D sourceTexture;
uniform sampler2D destinationTexture;
uniform mat4 sourceMatrix;
uniform mat4 destinationMatrix;
```

They can be included using the following directive:

```glsl
#include "@revideo/core/shaders/common.glsl"
```

### Source and Destination

Shaders in Motion Canvas follow the same idea as `globalCompositeOperation` in 2D canvas. The `sourceTexture` contains the node being rendered, and the `destinationTexture` contains what has already been rendered to the screen. These two can be sampled using `sourceUV` and `destinationUV` respectively, and then combined in various ways to produce the desired result.

### Custom Uniforms

You can pass custom uniforms to the shader by replacing the shader string with a configuration object:

```typescript
import myShader from './myShader.glsl';

//...
view.add(
  <Circle
    size={200}
    fill="lightseagreen"
    shaders={{
      fragment: myShader,
      uniforms: {
        myFloat: 0.5,
        myVec2: new Vector2(2, 5),
        myColor: new Color('blue'),
      },
    }}
  />,
);
```

The type of the uniform is inferred from the value:

| TypeScript | GLSL |
|---|---|
| `number` | `float` |
| `[number, number]` | `vec2` |
| `[number, number, number]` | `vec3` |
| `[number, number, number, number]` | `vec4` |
| `Color` | `vec4` |
| `Vector2` | `vec2` |
| `BBox` | `vec4` |
| `Spacing` | `vec4` |

### Caching

When a node is cached, its contents are first rendered to a separate canvas and then transferred to the screen. When a shader is applied to a descendant of a cached node, the `destinationTexture` will only contain the things drawn in the context of that cached node and nothing else.

Any node with a shader is automatically cached. The `cachePadding` property can be used to specify extra space around the node that should be included in the cache.
