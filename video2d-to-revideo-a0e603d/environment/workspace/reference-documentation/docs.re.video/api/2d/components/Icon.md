# Icon Component Documentation

## Overview

The Icon component is a specialized image component that provides access to over 150,000 icons from [Icones](https://icones.js.org/collection/all).

## Constructor

```typescript
public override new Icon(props: IconProps): Icon
```

## Key Properties

### `icon`
- Type: `SimpleSignal<string>`
- Required property specifying the icon identifier
- Format examples: `mdi:language-typescript`, `ph:anchor-simple-bold`

### `color`
- Type: `ColorSignal`
- Specifies the icon color
- Accepts named colors, hex strings
- Default: `'white'`

### Inherited Properties

All Img properties: transform, layout, appearance, curve, effects.

## Class Hierarchy

Icon extends `Img`.
