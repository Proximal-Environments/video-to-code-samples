# Ray Component Documentation

## Overview

The `Ray` class extends `Curve` and represents a node for drawing an individual line segment.

## Constructor

```typescript
public override new Ray(props: RayProps): Ray
```

## Core Properties

### Geometry Properties

- **`from`**: Vector2Signal - The starting point of the ray
- **`to`**: Vector2Signal - The ending point of the ray

### Inherited Properties

All Curve properties: start, end, offsets, arrows, closed, stroke, fill, lineWidth, transform, layout, effects, text.

## Example Usage

```typescript
const ray = createRef<Ray>();
view.add(
  <Ray
    ref={ray}
    lineWidth={8}
    endArrow
    stroke={'lightseagreen'}
    fromX={-200}
    toX={200}
  />,
);
yield* ray().start(1, 1);
yield* ray().start(0).end(0).start(1, 1);
```
