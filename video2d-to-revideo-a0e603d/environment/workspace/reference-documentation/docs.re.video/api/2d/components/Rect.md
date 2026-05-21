# Rect Component Documentation

## Overview

The `Rect` class extends `Curve` and represents a rectangular shape component in Revideo's 2D animation library. It serves as a foundational element for creating rectangular shapes with extensive customization options.

## Key Features

**Shape Properties:**
- Rounded corners via the `radius` signal, supporting individual corner radii
- Smooth corner rendering through `smoothCorners` and `cornerSharpness` properties
- Full inheritance of curve properties including stroke, fill, and drawing options

**Layout & Transform:**
The component supports comprehensive positioning through signals like `absolutePosition`, `position`, `scale`, `rotation`, and `skew`. Edge positioning helpers include `top`, `bottom`, `left`, `right`, and corner-specific accessors like `topLeft` and `bottomRight`.

**Styling:**
Inherits extensive styling capabilities including fill colors, stroke properties, opacity, shadows, and filters. The component supports text properties like `fontFamily`, `fontSize`, and `textAlign`.

**Child Management:**
Full support for hierarchical composition with methods including `add()`, `insert()`, `remove()`, and `removeChildren()`.

## Notable Methods

The component provides transformation utilities (`localToWorld()`, `worldToLocal()`), state management (`save()`, `restore()`, `getState()`, `applyState()`), and rendering functionality. Specialized curve methods include `arcLength()`, `getPointAtPercentage()`, and distance/percentage conversion utilities.

**Clone Operations:**
Three cloning strategies are available: `clone()` (preserves reactivity), `snapshotClone()` (captures current values), and `reactiveClone()` (creates dynamically synchronized copies).

## Properties

### Core Properties

| Property | Type | Description |
|----------|------|-------------|
| `position` | `Vector2Signal` | Represents the position of this node in local space of its parent |
| `x` | `SimpleSignal<number>` | X-axis position (accessor) |
| `y` | `SimpleSignal<number>` | Y-axis position (accessor) |
| `size` | `Vector2LengthSignal` | Represents the size of this node where x=width, y=height |
| `width` | `SignalLength` | Width dimension (accessor) |
| `height` | `SignalLength` | Height dimension (accessor) |
| `scale` | `Vector2Signal` | Represents the scale of this node in local space of its parent |
| `rotation` | `SimpleSignal<number>` | Rotation in degrees relative to parent |
| `opacity` | `SimpleSignal<number>` | Range 0-1, clamped value |
| `offset` | `Vector2Signal` | Represents the offset of this node's origin (pivot point for transforms) |

### Visual Properties

| Property | Type | Description |
|----------|------|-------------|
| `fill` | `CanvasStyleSignal` | Fill color/style |
| `stroke` | `CanvasStyleSignal` | Stroke color/style |
| `lineWidth` | `SimpleSignal<number>` | Stroke width in pixels |
| `radius` | `SpacingSignal` | Rounds the corners of this rectangle |
| `smoothCorners` | `SimpleSignal<boolean>` | Enables corner smoothing using Bézier curves |
| `cornerSharpness` | `SimpleSignal<number>` | Controls smoothing curve sharpness (0-1 range) |
| `lineCap` | `SimpleSignal<CanvasLineCap>` | Line ending style |
| `lineJoin` | `SimpleSignal<CanvasLineJoin>` | Line joining style |
| `lineDash` | `SimpleSignal<number[]>` | Dash pattern array |
| `lineDashOffset` | `SimpleSignal<number>` | Dash pattern offset |

### Layout & Positioning

| Property | Type | Description |
|----------|------|-------------|
| `clip` | `SimpleSignal<boolean>` | Enable clipping to bounds |
| `absolutePosition` | `SimpleVector2Signal` | A helper signal for operating on the position in world space |
| `absoluteRotation` | `SimpleSignal<number>` | Rotation in world space |
| `absoluteScale` | `SimpleVector2Signal` | Scale in world space |
| `middle` | `SimpleVector2Signal` | Center position |
| `top` | `SimpleVector2Signal` | Top edge position |
| `bottom` | `SimpleVector2Signal` | Bottom edge position |
| `left` | `SimpleVector2Signal` | Left edge position |
| `right` | `SimpleVector2Signal` | Right edge position |
| `topLeft` | `SimpleVector2Signal` | Top-left corner position |
| `topRight` | `SimpleVector2Signal` | Top-right corner position |
| `bottomLeft` | `SimpleVector2Signal` | Bottom-left corner position |
| `bottomRight` | `SimpleVector2Signal` | Bottom-right corner position |

### Flex Layout

| Property | Type | Description |
|----------|------|-------------|
| `layout` | `SimpleSignal<LayoutMode>` | Layout mode configuration |
| `direction` | `SimpleSignal<FlexDirection>` | Flex direction |
| `justifyContent` | `SimpleSignal<FlexContent>` | Main axis alignment |
| `alignItems` | `SimpleSignal<FlexItems>` | Cross axis alignment |
| `alignContent` | `SimpleSignal<FlexContent>` | Multi-line alignment |
| `alignSelf` | `SimpleSignal<FlexItems>` | Individual item alignment |
| `gap` | `Vector2LengthSignal` | Space between flex items |
| `padding` | `SpacingSignal` | Internal spacing |
| `margin` | `SpacingSignal` | External spacing |
| `basis` | `SimpleSignal<FlexBasis>` | Default item size |
| `grow` | `SimpleSignal<number>` | Growth factor |
| `shrink` | `SimpleSignal<number>` | Shrink factor |
| `wrap` | `SimpleSignal<FlexWrap>` | Wrapping behavior |

### Effects & Styling

| Property | Type | Description |
|----------|------|-------------|
| `shadowColor` | `ColorSignal` | Shadow color |
| `shadowBlur` | `SimpleSignal<number>` | Shadow blur radius |
| `shadowOffset` | `Vector2Signal` | Shadow displacement |
| `filters` | `FiltersSignal` | Visual filters |
| `shaders` | `Signal<ShaderConfig[]>` | Custom shader effects (experimental) |
| `cache` | `SimpleSignal<boolean>` | Enable render caching |
| `cachePadding` | `SpacingSignal` | Cache area padding |
| `composite` | `SimpleSignal<boolean>` | Composite blending |
| `compositeOperation` | `SimpleSignal<GlobalCompositeOperation>` | Blending mode |

### Text Properties

| Property | Type | Description |
|----------|------|-------------|
| `fontFamily` | `SimpleSignal<string>` | Font typeface |
| `fontSize` | `SimpleSignal<number>` | Font size |
| `fontWeight` | `SimpleSignal<number>` | Font weight |
| `fontStyle` | `SimpleSignal<string>` | Font style (italic, etc.) |
| `letterSpacing` | `SimpleSignal<number>` | Space between characters |
| `lineHeight` | `SimpleSignal<Length>` | Line height |
| `textAlign` | `SimpleSignal<CanvasTextAlign>` | Text alignment |
| `textDirection` | `SimpleSignal<CanvasDirection>` | Text direction |
| `textWrap` | `SimpleSignal<TextWrap>` | Text wrapping mode |

### Curve Properties (inherited from Curve)

| Property | Type | Description |
|----------|------|-------------|
| `start` | `SimpleSignal<number>` | Clip percentage from start (0-1) |
| `end` | `SimpleSignal<number>` | Clip percentage to end (0-1) |
| `startOffset` | `SimpleSignal<number>` | Pixel offset from curve start |
| `endOffset` | `SimpleSignal<number>` | Pixel offset from curve end |
| `startArrow` | `SimpleSignal<boolean>` | Display start arrow |
| `endArrow` | `SimpleSignal<boolean>` | Display end arrow |
| `arrowSize` | `SimpleSignal<number>` | Arrow size |
| `closed` | `SimpleSignal<boolean>` | Whether the curve should be closed |

### Hierarchy & Structure

| Property | Type | Description |
|----------|------|-------------|
| `children` | `Signal<Node[]>` | Child nodes |
| `parent` | `SimpleSignal<Node \| null>` | Parent node |
| `key` | `string` | Unique identifier |
| `zIndex` | `SimpleSignal<number>` | Rendering order |

## Key Methods

| Method | Returns | Purpose |
|--------|---------|---------|
| `add(node)` | `Rect` | Append child nodes |
| `insert(node, index)` | `Rect` | Insert children at position |
| `remove()` | `Rect` | Remove from parent |
| `clone(customProps)` | `Rect` | Create duplicate |
| `save()` | `void` | Store current state |
| `restore()` | `void \| Thread` | Restore saved state |
| `applyState(state)` | `void \| Thread` | Apply state snapshot |
| `getState()` | `NodeState` | Get current state snapshot |
| `localToWorld()` | `DOMMatrix` | Transform matrix to world space |
| `worldToLocal()` | `DOMMatrix` | Transform matrix from world space |
| `hit(position)` | `Node \| null` | Detect intersection |
| `arcLength()` | `number` | Visible curve length |
| `moveUp() / moveDown()` | `Rect` | Reorder siblings |
| `reparent(newParent)` | `void` | Change parent (keep position) |
