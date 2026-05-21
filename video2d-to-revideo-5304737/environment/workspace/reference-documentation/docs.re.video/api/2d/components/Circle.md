# Circle Component Documentation

## Overview

The `Circle` class is a node component in Revideo's 2D library used for rendering circular shapes, including circles, ellipses, arcs, and sectors (pie charts). It extends the `Curve` class.

## Constructor

```typescript
public override new Circle(props: CircleProps): Circle
```

## Key Properties

### Angle Properties
- **`startAngle`**: Beginning angle in degrees (default: 0)
- **`endAngle`**: Ending angle in degrees (default: 360)
- **`counterclockwise`**: Boolean to reverse drawing direction

### Path Properties
- **`closed`**: Whether the path should start and end at center (default: false)
- **`size`**: Two-dimensional vector for width and height
- **`fill`**: Canvas style signal for fill color
- **`stroke`**: Canvas style signal for stroke color

### Inherited Curve Properties
The Circle inherits numerous properties from Curve including:
- Positioning: `position`, `absolutePosition`, `rotation`, `scale`
- Styling: `lineWidth`, `lineCap`, `lineJoin`, `opacity`, `filters`
- Layout: `margin`, `padding`, `layout`, `alignItems`, `justifyContent`
- Text: `fontSize`, `fontFamily`, `fontStyle`, `fontWeight`
- Effects: `shadowColor`, `shadowBlur`, `shadowOffset`, `cache`, `shaders`

## Key Methods

**Transformation Methods:**
- `localToWorld()`, `worldToLocal()` - Matrix transformations
- `absoluteOpacity()` - Calculate opacity in world space
- `move()`, `moveUp()`, `moveDown()` - Reorder siblings

**Curve Methods:**
- `arcLength()` - Get visible arc length
- `baseArcLength()` - Get full curve length
- `getPointAtPercentage(value)` - Get point along curve
- `distanceToPercentage(value)` - Convert distance to percentage

**Clone Methods:**
- `clone(customProps)` - Create copy with overrides
- `reactiveClone(customProps)` - Create reactive copy
- `snapshotClone(customProps)` - Create snapshot copy

**State Management:**
- `save()`, `restore()` - Save/restore node state
- `getState()`, `applyState()` - Get/apply state snapshot

## Usage Example

```typescript
export default makeScene2D(function* (view) {
  view.add(
    <Circle
      size={160}
      fill={'lightseagreen'}
    />
  );
});
```

## Key Features

The Circle node supports rendering various shapes by manipulating angle and fill/stroke properties. The `closed` property determines whether the path includes a line segment from the arc back to the center, useful for sector rendering. All standard positioning, styling, and layout properties inherited from parent classes are available.
