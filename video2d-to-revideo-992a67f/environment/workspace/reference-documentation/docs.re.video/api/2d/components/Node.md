# Node Class Documentation

## Overview

The `Node` class is a foundational component in Revideo's 2D animation library. It implements `PromisableNode` and serves as the base for hierarchical scene graph structures.

## Key Properties

**Transform Properties:**
- `position`: Location in parent's local space
- `rotation`: Degrees relative to parent
- `scale`: Scaling in parent's local space
- `skew`: Skewing transformation
- `absolutePosition`, `absoluteRotation`, `absoluteScale`: World space equivalents

**Visual Properties:**
- `opacity`: Range 0-1, clamped automatically
- `zIndex`: Rendering order control
- `filters`: Visual effect filtering
- `shaders`: Experimental shader configuration
- `composite`: Compositing behavior
- `compositeOperation`: Canvas composite mode

**Shadow & Effects:**
- `shadowColor`, `shadowBlur`, `shadowOffset`: Shadow rendering
- `cache`: Performance optimization toggle
- `cachePadding`: Cache area expansion control

## Critical Methods

**Hierarchy Management:**
- `add()`, `insert()`: Add/insert child nodes
- `remove()`, `removeChildren()`: Remove from tree
- `reparent()`: Change parent while maintaining visual position

**Querying:**
- `findFirst()`, `findAll()`, `findLast()`: Descendant search with predicates
- `findAncestor()`: Ancestor matching
- `hit()`: Position-based node detection
- `peekChildren()`: Safe children access without signal registration

**State Management:**
- `save()`/`restore()`: State stack operations
- `getState()`: Snapshot current values
- `applyState()`: Apply state with optional animation
- `clone()`, `reactiveClone()`, `snapshotClone()`: Node duplication variants

**Rendering:**
- `render()`: Canvas drawing
- `drawOverlay()`: Inspector overlay support

**Coordinate Transformation:**
- `localToWorld()`, `worldToLocal()`: Space conversion matrices
- `localToParent()`, `worldToParent()`: Relative transformations
- `compositeToWorld()`: Effect space mapping

**Z-Order Control:**
- `moveUp()`, `moveDown()`, `moveToTop()`, `moveToBottom()`
- `moveAbove()`, `moveBelow()`, `moveTo()`: Precise positioning
- `move()`: Relative adjustment

## Specialized Features

"Get the nth children cast to the specified type" via `childAs<T>()` with generic type support. The `peekChildren()` method provides safe debugging access without reactive side effects.
