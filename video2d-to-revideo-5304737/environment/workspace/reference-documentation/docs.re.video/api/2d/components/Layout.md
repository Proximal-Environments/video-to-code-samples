# Layout Component Documentation

## Overview

The `Layout` class extends `Node` and provides comprehensive flexbox/layout functionality for 2D animation components in Revideo.

## Constructor

```typescript
public override new Layout(props: LayoutProps): Layout
```

## Key Layout & Flexbox Properties

### Flex Direction & Flow
- **`direction`**: Controls flexbox direction (row/column)
- **`wrap`**: Manages flex wrapping behavior
- **`gap`**: Spacing between flex items
  - **`columnGap`** (accessor): Horizontal spacing
  - **`rowGap`** (accessor): Vertical spacing

### Flex Item Properties
- **`grow`**: Flex growth factor for items
- **`shrink`**: Flex shrink factor for items
- **`basis`**: Base size before free space distribution
- **`alignSelf`**: Individual item alignment override

### Container Alignment
- **`alignItems`**: Aligns items perpendicular to flex direction
- **`alignContent`**: Aligns flex lines (multi-line containers)
- **`justifyContent`**: Aligns items along main axis

### Spacing
- **`padding`**: Internal spacing (SpacingSignal)
- **`margin`**: External spacing (SpacingSignal)

### Sizing
- **`size`**: Width and height (Vector2LengthSignal)
  - **`width`** (accessor): Individual width control
  - **`height`** (accessor): Individual height control
- **`minWidth`**, **`minHeight`**: Minimum constraints
- **`maxWidth`**, **`maxHeight`**: Maximum constraints
- **`ratio`**: Aspect ratio constraint

### Positioning Shortcuts
- **`top`**, **`bottom`**, **`left`**, **`right`**: Edge positions
- **`topLeft`**, **`topRight`**, **`bottomLeft`**, **`bottomRight`**: Corner positions
- **`middle`**: Center position

### Text & Font Properties
- **`fontSize`**, **`fontFamily`**, **`fontWeight`**, **`fontStyle`**
- **`textAlign`**: Canvas text alignment
- **`textDirection`**: Text directionality
- **`textWrap`**: Text wrapping behavior
- **`letterSpacing`**, **`lineHeight`**: Text metrics

### Display & Layout Mode
- **`layout`**: Layout mode signal (LayoutMode)
- **`clip`**: Enables clipping of overflow content
- **`offset`**: Origin offset relative to node size

## Key Methods

### Layout Queries
- **`layoutEnabled()`**: Returns resolved layout mode with inheritance
- **`isLayoutRoot()`**: Checks if node is layout root
- **`computedPosition()`**: Gets computed position
- **`anchorPosition()`**: Returns anchor position

### Size Management
- **`lockSize()`**: Locks current size
- **`releaseSize()`**: Unlocks size
- **`layoutChildren()`**: Performs layout calculations
- **`updateLayout()`**: Updates layout state

### Transform Helpers
- **`localToParent()`**: Matrix from local to parent space
- **`moveOffset(offset)`**: Updates origin offset while maintaining position

### Event Handling
- **`hit(position)`**: Hit detection at given position
- **`drawOverlay(context, matrix)`**: Renders debug overlay

### State Management
- **`save()`**, **`restore()`**: Save/restore node states
- **`applyState(state)`**: Apply state snapshot

## Inherited Properties from Node

- **`position`**, **`scale`**, **`rotation`**, **`skew`**
- **`absolutePosition`**, **`absoluteScale`**, **`absoluteRotation`**
- **`opacity`**, **`filters`**, **`shaders`**
- **`shadowColor`**, **`shadowBlur`**, **`shadowOffset`**
- **`zIndex`**, **`composite`**, **`compositeOperation`**
- **`cache`**, **`cachePadding`**
- **`children`**, **`parent`**

## Usage Context

The `Layout` component serves as the foundation for styled 2D content with complete flexbox support, enabling responsive positioning, sizing, and alignment of animation elements.
