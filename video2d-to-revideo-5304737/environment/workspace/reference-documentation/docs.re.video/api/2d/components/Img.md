# Img Component Documentation

## Overview

The `Img` class is a node for displaying images. It extends `Asset` and provides functionality for rendering and manipulating images within animations.

## Constructor

```typescript
public override new Img(props: ImgProps): Img
```

## Key Properties

### Image-Specific Properties

- **`alpha`**: Controls transparency of the image itself (affects only the image, leaving fill/stroke/children intact)
- **`smoothing`**: Boolean for image interpolation; when disabled, images appear pixelated
- **`src`**: Source path or URL for the image asset
- **`ratio`**: Optional aspect ratio constraint

### Transform, Layout, Visual Properties

Inherits all standard properties from Asset/Shape/Layout/Node.

## Key Methods

### Color Sampling

- `getColorAtPoint(position): Color` - Samples color at position in local space
- `getPixelColor(position): Color` - Samples color at pixel location

### Size Information

- `naturalSize(): Vector2` - Returns original image dimensions unaffected by size/scale

### All standard node methods

add, remove, clone, save, restore, render, findAll, etc.

## Extended By

- `Icon`
- `Latex`

## Example Usage

```typescript
const ref = createRef<Img>();
yield view.add(
  <Img
    ref={ref}
    src="https://images.unsplash.com/photo-1679218407381-a6f1660d60e9"
    width={300}
    radius={20}
  />,
);
ref().fill(ref().getColorAtPoint(0));
yield* all(
  ref().size([100, 100], 1).to([300, null], 1),
  ref().radius(50, 1).to(20, 1),
  ref().alpha(0, 1).to(1, 1),
);
```
