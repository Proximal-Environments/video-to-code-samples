# Knot Component Documentation

## Overview

The `Knot` class extends `Node` and represents a knot of a `Spline` component.

## Constructor

```typescript
public override new Knot(props: KnotProps): Knot
```

## Key Properties

### Handle Properties
- **`startHandle`**: Vector2Signal defining the knot's start handle position, relative to the knot's position. Default mirrors `endHandle`.
- **`endHandle`**: Vector2Signal defining the knot's end handle position, relative to the knot's position. Default mirrors `startHandle`.
- **`auto`**: KnotAutoSignal controlling blend between user-provided and auto-calculated handles. Default: `0`.

### Position and Transform
- `position`, `absolutePosition`, `rotation`, `absoluteRotation`, `scale`, `absoluteScale`, `skew`

### Visual Properties
- `opacity`, `zIndex`, `filters`, `shadowColor`, `shadowBlur`, `shadowOffset`

## Accessors

- `x`, `y`: Position components
- `startHandleAuto`, `endHandleAuto`: Auto-calculated handle signals

## Methods

- `points()`: Returns KnotInfo
- All standard Node methods: add, remove, save, restore, clone, findAll, etc.
