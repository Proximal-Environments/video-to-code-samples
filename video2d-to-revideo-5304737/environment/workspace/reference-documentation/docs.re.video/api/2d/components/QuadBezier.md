# QuadBezier Component Documentation

## Overview

QuadBezier is a node for drawing a quadratic Bezier curve. It extends the `Bezier` class.

## Constructor

```typescript
public override new QuadBezier(props: QuadBezierProps): QuadBezier
```

## Core Properties

### Control Points

- **`p0`**: Vector2Signal - The start point of the curve
- **`p1`**: Vector2Signal - The control point that influences the curve's shape
- **`p2`**: Vector2Signal - The end point of the curve

### Inherited Properties

All Bezier/Curve properties: start, end, offsets, arrows, stroke, fill, lineWidth, transform, layout, effects.

## Example Usage

```typescript
const bezier = createRef<QuadBezier>();
view.add(
  <QuadBezier
    ref={bezier}
    lineWidth={4}
    stroke={'lightseagreen'}
    p0={[-200, 0]}
    p1={[0, -200]}
    p2={[200, 0]}
    end={0}
  />
);
yield* bezier().end(1, 1);
yield* bezier().start(1, 1).to(0, 1);
```
