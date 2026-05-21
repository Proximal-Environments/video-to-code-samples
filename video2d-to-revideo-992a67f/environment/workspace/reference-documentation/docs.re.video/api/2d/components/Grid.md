# Grid Component Documentation

## Overview

The `Grid` class extends `Shape` and provides functionality for rendering a two-dimensional grid pattern.

## Constructor

```typescript
public override new Grid(props: GridProps): Grid
```

## Key Properties

### Grid-Specific Properties

- **`end`**: Controls the percentage clipped from each grid line's end
- **`start`**: Controls the percentage clipped from each grid line's beginning
- **`spacing`**: Vector2Signal defining the spacing between grid lines

### Inherited Properties

All standard Shape properties: transform, visual, layout, edge shortcuts, effects.

## Example Usage

```typescript
export default makeScene2D(function* (view) {
  const grid = createRef<Grid>();
  view.add(
    <Grid
      ref={grid}
      width={'100%'}
      height={'100%'}
      stroke={'#666'}
      start={0}
      end={1}
    />,
  );
  yield* all(
    grid().end(0.5, 1).to(1, 1).wait(1),
    grid().start(0.5, 1).to(0, 1).wait(1),
  );
});
```
