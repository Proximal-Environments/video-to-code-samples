# Rive Component Documentation

## Overview

The `Rive` class extends `Asset` and provides functionality for rendering Rive animations within Revideo projects.

## Constructor

```typescript
public override new Rive(props: RiveProps): Rive
```

## Core Properties

### Animation Control

- **`animationId`**: Signal controlling which animation plays (string or number identifier)
- **`artboardId`**: Signal specifying the artboard to display (string or number identifier)

### Source

- **`src`**: Signal for the source file path of the Rive asset

### Inherited Properties

All Asset properties: transform, layout, visual, styling, spatial helpers.

## Methods

All standard node methods: add, remove, save, restore, clone, render, findAll, transform methods, etc.
