# Path Component Documentation

## Overview

The `Path` class extends `Curve` and represents an SVG path element for drawing custom shapes.

## Constructor

```typescript
public override new Path(props: PathProps): Path
```

## Key Properties

### `data`
```typescript
readonly public data: SimpleSignal<string, Path>
```
Defines the SVG path data string that determines the shape to be rendered.

### Inherited Properties

All Curve properties: closed, start, end, startOffset, endOffset, arrows, stroke, fill, lineWidth, transform, layout, effects.

## Methods

### Arc Length Methods
- `arcLength()`: Visible arc length
- `baseArcLength()`: Complete curve length
- `offsetArcLength()`: Length accounting for offsets

### Point Retrieval
- `getPointAtPercentage(value)`: Point at specified percentage
- `getPointAtDistance(value)`: Point at specified pixel distance

### Drawing
- `drawOverlay(context, matrix)`: Renders inspector overlay
- `profile()`: Returns curve profile information

### All standard node methods
Transform, state, hierarchy, search, clone, render.
