# View2D Component Documentation

## Overview

`View2D` extends `Rect` and serves as a 2D view component — the root of a scene's node tree.

## Constructor

```typescript
public override new View2D(props: View2DProps): View2D
```

## Key Properties

### Transform Properties
- `position`, `rotation`, `scale`, `skew`, `offset`
- `absolutePosition`, `absoluteRotation`, `absoluteScale`

### Size & Layout
- `size`, `width`, `height`
- `layout`, `direction`, `justifyContent`, `alignItems`, `alignContent`
- `gap`, `padding`, `margin`, `basis`, `grow`, `shrink`

### Appearance
- `fill`, `stroke`, `opacity`, `lineWidth`, `radius`
- `smoothCorners`, `cornerSharpness`

### Edge & Position Shortcuts
- `top`, `bottom`, `left`, `right`, `topLeft`, `topRight`, `bottomLeft`, `bottomRight`, `middle`

### Playback & Time
- `fps`, `globalTime`, `playbackState`

### Effects & Rendering
- `filters`, `shadows`, `cache`, `cachePadding`, `shaders`

## Key Methods

### Search
- `findKey<T>(key: string)`: Find node by key

### All standard Rect/Curve/Shape/Layout/Node methods

Transform, state, hierarchy, rendering, search, clone, curve operations.

## Key Concepts

- **Origin Offset**: Controls pivot point for rotation/scaling (-1 to 1 range)
- **Flex Layout**: Standard flex properties for automatic child positioning
- **World vs Local Space**: `absolutePosition` for world coords, `position` for parent-local
- **Curve Clipping**: `start`, `end` properties for animating curves appearing/disappearing
- **Smooth Corners**: Bezier-based corner rounding via `smoothCorners` and `cornerSharpness`
