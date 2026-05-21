# Txt Component API Documentation

## Overview

The `Txt` class is a text rendering component that extends `Shape`. It provides comprehensive text rendering capabilities with extensive positioning, styling, and transformation options.

## Class Definition

```typescript
class Txt extends Shape
```

## Constructor

```typescript
public override new Txt{...}: TxtProps: Txt
```

## Core Properties

### Text Content
- **`text`**: `SimpleSignal<string, Txt>` - The text content to render

### Positioning Properties
- **`position`**: `Vector2Signal<Txt>` - Local position relative to parent
- **`absolutePosition`**: `SimpleVector2Signal<Txt>` - World space positioning
- **`x`** / **`y`**: `SimpleSignal<number, this>` - Individual axis positioning

### Size Properties
- **`size`**: `Vector2LengthSignal<Txt>` - Width and height dimensions
- **`width`** / **`height`**: `Signal<Length | number, this>` - Individual dimensions
- **`maxWidth`** / **`maxHeight`**: `SimpleSignal<LengthLimit, Txt>` - Maximum constraints
- **`minWidth`** / **`minHeight`**: `SimpleSignal<LengthLimit, Txt>` - Minimum constraints

### Transform Properties
- **`rotation`**: `SimpleSignal<number, Txt>` - Rotation in degrees
- **`scale`**: `Vector2Signal<Txt>` - Scale transformation
- **`skew`**: `Vector2Signal<Txt>` - Skew transformation
- **`absoluteRotation`**: `SimpleSignal<number, Txt>` - World space rotation
- **`absoluteScale`**: `SimpleVector2Signal<Txt>` - World space scale
- **`offset`**: `Vector2Signal<Txt>` - Origin offset for transformations

### Edge Positioning
- **`top`** / **`bottom`** / **`left`** / **`right`**: `SimpleVector2Signal<Txt>` - Edge positions
- **`topLeft`** / **`topRight`** / **`bottomLeft`** / **`bottomRight`**: `SimpleVector2Signal<Txt>` - Corner positions
- **`middle`**: `SimpleVector2Signal<Txt>` - Center position

### Typography Properties
- **`fontSize`**: `SimpleSignal<number, Txt>` - Font size in pixels
- **`fontFamily`**: `SimpleSignal<string, Txt>` - Font family name
- **`fontWeight`**: `SimpleSignal<number, Txt>` - Font weight (numeric)
- **`fontStyle`**: `SimpleSignal<string, Txt>` - Font style (e.g., 'italic')
- **`letterSpacing`**: `SimpleSignal<number, Txt>` - Spacing between characters
- **`lineHeight`**: `SimpleSignal<Length, Txt>` - Line height measurement
- **`textAlign`**: `SimpleSignal<CanvasTextAlign, Txt>` - Text alignment
- **`textDirection`**: `SimpleSignal<CanvasDirection, Txt>` - Text direction (ltr/rtl)
- **`textWrap`**: `SimpleSignal<TextWrap, Txt>` - Text wrapping behavior

### Visual Properties
- **`fill`**: `CanvasStyleSignal<Txt>` - Fill color/style
- **`stroke`**: `CanvasStyleSignal<Txt>` - Stroke color/style
- **`lineWidth`**: `SimpleSignal<number, Txt>` - Stroke width
- **`lineCap`**: `SimpleSignal<CanvasLineCap, Txt>` - Line cap style
- **`lineJoin`**: `SimpleSignal<CanvasLineJoin, Txt>` - Line join style
- **`lineDash`**: `SimpleSignal<number[], Txt>` - Dashed line pattern
- **`lineDashOffset`**: `SimpleSignal<number, Txt>` - Dash offset
- **`opacity`**: `SimpleSignal<number, Txt>` - Opacity (0-1 range)
- **`antialiased`**: `SimpleSignal<boolean, Txt>` - Antialiasing control
- **`cache`**: `SimpleSignal<boolean, Txt>` - Canvas caching
- **`cachePadding`**: `SpacingSignal<Txt>` - Cache padding expansion
- **`composite`**: `SimpleSignal<boolean, Txt>` - Composite rendering
- **`compositeOperation`**: `SimpleSignal<GlobalCompositeOperation, Txt>` - Blend mode
- **`clip`**: `SimpleSignal<boolean, Txt>` - Clipping behavior

### Shadow Properties
- **`shadowColor`**: `ColorSignal<Txt>` - Shadow color
- **`shadowBlur`**: `SimpleSignal<number, Txt>` - Shadow blur radius
- **`shadowOffset`**: `Vector2Signal<Txt>` - Shadow offset

### Layout Properties
- **`layout`**: `SimpleSignal<LayoutMode, Txt>` - Layout mode (flex/none)
- **`direction`**: `SimpleSignal<FlexDirection, Txt>` - Flex direction
- **`alignContent`**: `SimpleSignal<FlexContent, Txt>` - Align content
- **`alignItems`**: `SimpleSignal<FlexItems, Txt>` - Align items
- **`alignSelf`**: `SimpleSignal<FlexItems, Txt>` - Align self
- **`justifyContent`**: `SimpleSignal<FlexContent, Txt>` - Justify content
- **`gap`**: `Vector2LengthSignal<Txt>` - Gap between items
- **`columnGap`** / **`rowGap`**: `Signal<Length | number, this>` - Directional gaps
- **`wrap`**: `SimpleSignal<FlexWrap, Txt>` - Flex wrapping
- **`basis`**: `SimpleSignal<FlexBasis, Txt>` - Flex basis
- **`grow`**: `SimpleSignal<number, Txt>` - Flex grow
- **`shrink`**: `SimpleSignal<number, Txt>` - Flex shrink
- **`margin`**: `SpacingSignal<Txt>` - Margin spacing
- **`padding`**: `SpacingSignal<Txt>` - Padding spacing
- **`ratio`**: `SimpleSignal<null | number, Txt>` - Aspect ratio

### Meta Properties
- **`key`**: `string` - Component identifier
- **`children`**: `Signal<ComponentChildren<Node>[], SignalContext>` - Child nodes
- **`parent`**: `SimpleSignal<null | Node, void>` - Parent node
- **`zIndex`**: `SimpleSignal<number, Txt>` - Stacking order

## Static Methods

**`Txt.b(props: TxtProps)`**: `Txt` - Shortcut for creating bold text: `<Txt fontWeight={700} />`

**`Txt.i(props: TxtProps)`**: `Txt` - Shortcut for creating italic text: `<Txt fontStyle={'italic'} />`
