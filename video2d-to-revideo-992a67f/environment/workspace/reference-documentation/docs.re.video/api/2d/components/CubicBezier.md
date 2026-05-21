# CubicBezier Component Documentation

## Overview

The `CubicBezier` class extends `Bezier` and provides functionality for drawing a cubic Bezier curve.

## Constructor

```typescript
public override new CubicBezier(props: CubicBezierProps): CubicBezier
```

## Core Properties

### Control Points

- **`p0`**: Vector2Signal - The start point of the Bezier curve
- **`p1`**: Vector2Signal - The first control point of the Bezier curve
- **`p2`**: Vector2Signal - The second control point of the Bezier curve
- **`p3`**: Vector2Signal - The end point of the Bezier curve

### Curve Visibility

- **`start`**: Percentage from the start before which the curve is clipped
- **`end`**: Percentage from the start after which the curve is clipped
- **`startOffset`**: Offset in pixels from the curve's start
- **`endOffset`**: Offset in pixels from the curve's end

### Arrow Properties

- **`startArrow`**: Displays arrow at the curve's start
- **`endArrow`**: Displays arrow at the curve's end
- **`arrowSize`**: Controls arrow dimensions

### Styling, Transform, Layout, Visual Effects

Inherits all properties from Bezier/Curve/Shape including stroke, fill, lineWidth, position, rotation, scale, opacity, filters, shadows, layout properties, etc.

## Key Methods

- `arcLength()`: Visible arc length
- `baseArcLength()`: Complete curve length
- `getPointAtPercentage(value)`: Point at percentage along curve
- `profile()`: Curve profile information
- All standard node methods (add, remove, clone, save, restore, etc.)

## Example Usage

```typescript
const bezier = createRef<CubicBezier>();
view.add(
  <CubicBezier
    ref={bezier}
    lineWidth={4}
    stroke={'lightseagreen'}
    p0={[-200, -100]}
    p1={[100, -100]}
    p2={[-100, 100]}
    p3={[200, 100]}
    end={0}
  />
);
yield* bezier().end(1, 1);
yield* bezier().start(1, 1).to(0, 1);
```
