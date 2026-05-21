# Audio Component Documentation

## Overview

The `Audio` class extends `Media` and represents an audio component in Revideo's 2D animation framework.

## Constructor

```typescript
public override new Audio(props: MediaProps): Audio
```

Creates a new Audio instance with the provided MediaProps configuration.

## Key Properties

The Audio component inherits numerous properties from Media, including:

- **Position & Transform**: `position`, `rotation`, `scale`, `offset`, `skew`
- **Dimensions**: `size`, `width`, `height`
- **Appearance**: `opacity`, `fill`, `stroke`, `filters`
- **Layout**: `layout`, `padding`, `margin`, `gap`
- **Media Control**: `src`, `loop`, `playbackRate`, `volume`
- **Curve Properties**: `start`, `end`, `startOffset`, `endOffset`
- **Text Styling**: `fontSize`, `fontFamily`, `fontWeight`, `fontStyle`, `lineHeight`, `letterSpacing`
- **Visual Effects**: `shadowBlur`, `shadowColor`, `shadowOffset`, `cache`, `cachePadding`

## Core Methods

**Playback Control**:
- `play()`: Begin audio playback
- `pause()`: Pause audio playback
- `getCurrentTime()`: Retrieve current playback position
- `getDuration()`: Get total audio length
- `setVolume(volume: number)`: Adjust audio volume
- `getVolume()`: Retrieve current volume

**Positioning & Transformation**:
- `localToWorld()`: Transform from local to world space
- `worldToLocal()`: Transform from world to global space
- `move(by: number)`: Reorder relative to siblings
- `reparent(newParent: Node)`: Change parent while maintaining position

**State Management**:
- `getState()`: Capture current signal values
- `applyState(state: NodeState)`: Apply stored state
- `save()`: Push state snapshot onto stack
- `restore()`: Pop previous state from stack
- `clone()`: Create node copy with optional property overrides

**Rendering**:
- `render(context: CanvasRenderingContext2D)`: Draw to canvas
- `toPromise()`: Await asynchronous resource loading

**Hierarchy**:
- `add(node: ComponentChildren)`: Append child nodes
- `insert(node: ComponentChildren, index: number)`: Insert at position
- `remove()`: Remove from parent
- `removeChildren()`: Clear all children

**Search & Traversal**:
- `findFirst(predicate)`: Locate first matching descendant
- `findAll(predicate)`: Find all matching descendants
- `findAncestor(predicate)`: Find closest matching parent

## Accessor Properties

Convenient getters for frequently-used dimensions:
- `x`, `y`: Individual position components
- `width`, `height`: Dimension components
- `columnGap`, `rowGap`: Flex spacing
