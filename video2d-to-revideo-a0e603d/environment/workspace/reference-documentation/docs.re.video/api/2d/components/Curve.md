# Curve Component Documentation

## Overview

`Curve` is an abstract class extending `Shape` that provides foundational functionality for curve-based components.

## Extended By

- `Bezier`, `Circle`, `Line`, `Path`, `Polygon`, `Ray`, `Rect`, `Spline`

## Constructor

```typescript
public override new Curve(props: CurveProps): Curve
```

## Key Properties

### Curve Visibility & Rendering

- **`closed`**: Whether the curve should be closed (start and end points connected)
- **`start`**: A percentage from the start before which the curve should be clipped
- **`end`**: A percentage from the start after which the curve should be clipped
- **`startOffset`**: The offset in pixels from the start of the curve
- **`endOffset`**: The offset in pixels from the end of the curve

### Arrow Properties

- **`arrowSize`**: Controls the size of the end and start arrows
- **`startArrow`**: Whether to display an arrow at the start of the visible curve
- **`endArrow`**: Whether to display an arrow at the end of the visible curve

## Methods

### Arc Length Calculations

- `arcLength()`: The visible arc length accounting for both offset and start/end properties
- `baseArcLength()`: The entire length of this curve, not accounting for offsets
- `offsetArcLength()`: The length accounting for offsets

### Percentage & Distance Conversion

- `completion()`: Ratio between visible length and offset length
- `distanceToPercentage(value: number)`: Converts distance to percentage
- `percentageToDistance(value: number)`: Converts percentage to distance

### Point Retrieval

- `getPointAtPercentage(value: number): CurvePoint`: Retrieves point at specified percentage

### Profiling

- `profile(): CurveProfile`: Abstract method for curve profile information

## Inherited Properties

Transform, layout, visual, and edge position properties from `Shape`.
