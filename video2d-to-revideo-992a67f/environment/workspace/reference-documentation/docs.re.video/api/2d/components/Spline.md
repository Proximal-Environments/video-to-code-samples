# Spline Component Documentation

## Overview

The `Spline` class extends `Curve` and is a node for drawing a smooth line through a number of points. This node uses Bezier curves for drawing each segment of the spline.

## Constructor

```typescript
public override new Spline(props: SplineProps): Spline
```

## Key Properties

### `points`
```typescript
readonly public points: SimpleSignal<null | SignalValue<PossibleVector2 | number[]>, Spline>
```
The knots of the spline as an array with auto-calculated handles.

### `smoothness`
```typescript
readonly public smoothness: SimpleSignal<number, void>
```
Controls the smoothness of the resulting curve when using auto-calculated handles. Default: `0.4`. Only applies to knots without explicit handles.

### Inherited Properties

All Curve properties: closed, start, end, offsets, arrows, stroke, fill, lineWidth, transform, layout, effects.

## Key Methods

- `knots()`: Returns KnotInfo[] for the spline
- `profile()`: Returns curve profile information
- `drawOverlay(context, matrix)`: Draws inspection overlay
- All standard curve and node methods
