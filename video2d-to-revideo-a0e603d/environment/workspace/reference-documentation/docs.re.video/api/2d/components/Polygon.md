# Polygon Component Documentation

## Overview

The `Polygon` class extends `Curve` and is used to render regular polygons such as triangles, pentagons, and hexagons. The polygon is inscribed in a circle defined by height and width dimensions.

## Key Properties

### `sides`
Controls the number of polygon sides. A value of 6 creates a hexagon.

### `radius`
Defines the radius of the polygon's corners, allowing for rounded vertices.

### `size`
A two-dimensional vector representing width and height. The polygon inscribes within the resulting circle or ellipse.

## Constructor

```typescript
public new Polygon(props: PolygonProps): Polygon
```

## Notable Inherited Properties

The Polygon component inherits extensive properties from `Curve`, including:

- **Transform**: `position`, `rotation`, `scale`, `skew`, `offset`
- **Appearance**: `fill`, `stroke`, `lineWidth`, `opacity`
- **Layout**: `size`, `margin`, `padding`
- **Curve-specific**: `start`, `end`, `startOffset`, `endOffset`, `closed`

## Key Methods

### Drawing and Layout
- `profile()`: Returns curve profile information
- `render()`: Renders the polygon onto a canvas
- `draw()`: Performs the actual drawing operations

### Transform Methods
- `localToWorld()`: Converts local to world space
- `worldToLocal()`: Converts world to local space
- `getPointAtPercentage()`: Returns a point along the curve

### State Management
- `save()`: Saves current state
- `restore()`: Restores previously saved state
- `getState()`: Returns snapshot of signal values
- `applyState()`: Applies state to the node

### Hierarchy Operations
- `add()`, `insert()`, `remove()`: Manage child nodes
- `moveUp()`, `moveDown()`, `moveToTop()`: Reorder siblings

## Example Usage

```typescript
import { makeScene2D, createRef, Polygon } from '@revideo/2d';

export default makeScene2D(function* (view) {
  const ref = createRef<Polygon>();
  
  view.add(
    <Polygon
      ref={ref}
      sides={6}
      size={160}
      fill={'lightseagreen'}
    />
  );
  
  yield* ref().sides(3, 2).to(6, 2);
});
```

This example creates a hexagon that animates its sides from 3 to 6 over 4 seconds.

## Important Notes

- Polygons are inscribed in circles; unequal height/width creates ellipse inscription
- Low side counts may show visible differences between displayed and bounding dimensions
- The component supports all standard node features: filters, shadows, caching, and layout
