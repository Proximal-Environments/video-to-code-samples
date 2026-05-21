# Bezier Component Documentation

## Overview

The `Bezier` class is an abstract component that extends `Curve` in the Revideo 2D animation library. It serves as a base class for creating Bezier curve shapes.

## Class Hierarchy

- **Extended by:**
  - `CubicBezier`
  - `QuadBezier`

## Constructor

```typescript
public new Bezier(props: CurveProps): Bezier
```

## Key Properties

### Transform Properties
- `position`: Represents placement in local parent space
- `rotation`: Rotation in degrees relative to parent
- `scale`: Scale in local parent space
- `skew`: Skew transformation
- `absolutePosition`, `absoluteRotation`, `absoluteScale`: World-space variants

### Curve-Specific Properties
- `start`: Percentage from start before which curve is clipped
- `end`: Percentage from start after which curve is clipped
- `startOffset`: Pixel offset from curve start
- `endOffset`: Pixel offset from curve end
- `startArrow`: Display arrow at curve start
- `endArrow`: Display arrow at curve end
- `arrowSize`: Controls arrow dimensions
- `closed`: Whether curve endpoints connect

### Visual Properties
- `stroke`: Stroke styling
- `fill`: Fill color
- `lineWidth`: Stroke thickness
- `lineCap`: Canvas line cap style
- `lineJoin`: Canvas line join style
- `lineDash`: Dashed line pattern
- `opacity`: Transparency (0-1 range)

### Layout Properties
- `size`: Two-dimensional dimensions
- `offset`: Origin offset relative to node size
- `margin`, `padding`: Spacing properties
- `layout`: Layout mode configuration
- `alignItems`, `alignContent`, `justifyContent`: Flexbox alignment

### Effects
- `filters`: Visual filter effects
- `shadowBlur`, `shadowColor`, `shadowOffset`: Shadow effects
- `cache`: Enable canvas caching
- `cachePadding`: Cached canvas padding
- `shaders`: Experimental shader configuration

## Methods

### Transformation Methods
- `localToParent()`: Matrix mapping local to parent space
- `localToWorld()`: Matrix mapping local to world space
- `worldToLocal()`: Matrix mapping world to local space
- `worldToParent()`: Matrix mapping world to parent space

### Curve Analysis
- `arcLength()`: Returns visible arc length accounting for offsets and start/end
- `baseArcLength()`: Returns complete curve length
- `offsetArcLength()`: Returns length accounting for offsets only
- `completion()`: Percentage of visible curve relative to offset length
- `getPointAtPercentage(value: number)`: Retrieves point at percentage along curve
- `distanceToPercentage(value: number)`: Converts distance to percentage
- `percentageToDistance(value: number)`: Converts percentage to distance

### Node Manipulation
- `add(node: ComponentChildren)`: Append child nodes
- `insert(node: ComponentChildren, index?: number)`: Insert child at position
- `remove()`: Remove node from tree
- `clone(customProps?: NodeState)`: Create copy with optional property overrides
- `snapshotClone(customProps?: NodeState)`: Copy with reactive values calculated
- `reactiveClone(customProps?: NodeState)`: Reactive copy with dynamic updates

### State Management
- `save()`: Push current state to stack
- `restore()`: Pop and restore previous state
- `getState()`: Snapshot current signal values
- `applyState(state: NodeState, duration?, timing?)`: Apply state with optional animation

### Rendering
- `render(context: CanvasRenderingContext2D)`: Draw onto canvas
- `drawOverlay(context: CanvasRenderingContext2D, matrix: DOMMatrix)`: Draw inspection overlay

### Search & Query
- `findAll(predicate)`: Locate all matching descendants
- `findFirst(predicate)`: Find first matching descendant
- `findLast(predicate)`: Find last matching descendant
- `findAncestor(predicate)`: Find closest matching ancestor
- `childAs<T>(index: number)`: Retrieve child cast to type
- `childrenAs<T>()`: Get children array cast to type

### Child Management
- `removeChildren()`: Remove all children
- `reparent(newParent: Node)`: Change parent while maintaining position
