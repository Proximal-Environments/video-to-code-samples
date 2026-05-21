# Shape Class Documentation

## Overview

The `Shape` class is an abstract class extending `Layout` that serves as the base for rendering visual elements in Revideo. It provides properties and methods for styling, transformation, and rendering shapes on canvas.

## Class Hierarchy

**Extends:** `Layout`

**Extended by:** `Code`, `Curve`, `Grid`, `SVG`, `Txt`

## Constructor

```typescript
public override new Shape(props: ShapeProps): Shape
```

## Key Properties

### Visual Styling
- `fill` - Canvas style signal for fill color
- `stroke` - Canvas style signal for stroke color
- `lineWidth` - Signal controlling stroke width
- `lineCap` - Canvas line cap style
- `lineJoin` - Canvas line join style
- `lineDash` - Array of dash pattern numbers
- `lineDashOffset` - Offset for dash pattern
- `strokeFirst` - Boolean determining stroke render order
- `antialiased` - Boolean for antialiasing

### Transformation & Layout
Inherited from Layout:
- `position` - Local space positioning
- `scale` - 2D scaling vector
- `rotation` - Rotation in degrees
- `skew` - 2D skew vector
- `absolutePosition` - World space positioning helper
- `absoluteRotation` - World space rotation helper
- `absoluteScale` - World space scale helper
- `offset` - Origin offset relative to node size

### Positioning Helpers
- `middle` - Center position
- `top`, `bottom`, `left`, `right` - Edge positions
- `topLeft`, `topRight`, `bottomLeft`, `bottomRight` - Corner positions

### Layout Properties
- `size` - 2D dimensions (width/height as Length type)
- `margin` - Spacing outside boundaries
- `padding` - Spacing inside boundaries
- `gap` - Space between flex children
- `layout` - Layout mode (flex or default)
- `direction` - Flex direction
- `alignItems`, `alignContent`, `justifyContent` - Flex alignment
- `grow`, `shrink`, `basis` - Flex sizing

### Visual Effects
- `opacity` - Transparency (0-1)
- `filters` - Canvas filter effects
- `shadowColor`, `shadowBlur`, `shadowOffset` - Shadow styling
- `composite` - Composite mode enabled
- `compositeOperation` - Global composite operation
- `clip` - Clipping enabled
- `cache` - Canvas caching enabled
- `cachePadding` - Cache expansion padding

### Typography
- `fontFamily` - Font name
- `fontSize` - Text size
- `fontStyle` - Font style
- `fontWeight` - Font weight
- `lineHeight` - Line spacing
- `letterSpacing` - Character spacing
- `textAlign` - Canvas text alignment
- `textDirection` - Text direction
- `textWrap` - Text wrapping mode

### Other Properties
- `children` - Child node signal
- `parent` - Parent node reference
- `zIndex` - Stacking order
- `key` - Unique identifier
- `shaders` - Custom shader configurations (experimental)

## Core Methods

### Rendering
- `render(context)` - Render node to canvas context
- `drawOverlay(context, matrix)` - Draw inspection overlay

### State Management
- `getState()` - Return snapshot of current signal values
- `applyState(state)` - Apply state snapshot to node
- `save()` - Push state to stack
- `restore()` - Pop and restore previous state

### Tree Operations
- `add(node)` - Append child nodes
- `insert(node, index)` - Insert children at position
- `remove()` - Remove from parent
- `removeChildren()` - Clear all children
- `move(by)` - Rearrange relative to siblings
- `moveTo(index)` - Move to specific index
- `moveUp()`, `moveDown()` - Adjust z-order
- `moveToTop()`, `moveToBottom()` - Extreme z-order
- `moveAbove(node)`, `moveBelow(node)` - Move relative to sibling
- `reparent(newParent)` - Change parent while maintaining position

### Finding Nodes
- `findAll(predicate)` - Find matching descendants
- `findFirst(predicate)` - Get first match
- `findLast(predicate)` - Get last match
- `findAncestor(predicate)` - Find matching ancestor
- `childAs<T>(index)` - Get typed child
- `childrenAs<T>()` - Get typed children array
- `parentAs<T>()` - Get typed parent

### Cloning
- `clone(customProps)` - Create copy with properties
- `snapshotClone(customProps)` - Clone with calculated values
- `reactiveClone(customProps)` - Create reactive copy

### Transformation
- `localToParent()` - Get local-to-parent matrix
- `localToWorld()` - Get local-to-world matrix
- `worldToLocal()` - Get world-to-local matrix
- `worldToParent()` - Get world-to-parent matrix
- `compositeToWorld()` - Get composite-to-world matrix
- `moveOffset(offset)` - Update origin and adjust position

### Layout
- `layoutEnabled()` - Get resolved layout mode
- `isLayoutRoot()` - Check if layout root
- `hit(position)` - Find node at position
- `cacheBBox()` - Get bounding box

### Utilities
- `instantiate(props)` - Create instance of class
- `toPromise()` - Wait for async resources
- `dispose()` - Cleanup before garbage collection
- `ripple(duration)` - Trigger ripple effect

## Type Information

`ShapeProps` - Constructor properties interface for Shape configuration
