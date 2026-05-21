# Revideo Types API Documentation

## Overview
This page documents the **types module** from `@revideo/core`, which provides "Complex types used in animations."

## Enumerations
- `Center`
- `Direction`
- `Origin`

## Classes
- `BBox`
- `Matrix2D`
- `Spacing`
- `Vector2`

## Interfaces
- `Type`
- `WebGLConvertible`

## Type Aliases

**CanvasColorSpace**: Union of `'srgb'` or `'display-p3'`

**CanvasOutputMimeType**: Union of `'image/png'`, `'image/jpeg'`, or `'image/webp'`

**Color**: Represents a color; same class as created by [`chroma.js`](https://gka.github.io/chroma.js/)

**ColorSignal**: Generic signal type parameterized by `T`

**PossibleBBox**: Union accepting `SerializedBBox`, numbers, `Vector2`, or `undefined`

**PossibleColor**: Union accepting `SerializedColor`, numbers, `Color`, or objects with color properties

**PossibleMatrix2D**: Union accepting `Matrix2D`, `DOMMatrix`, numbers, `PossibleVector2`, or `undefined`

**PossibleSpacing**: Union accepting `SerializedSpacing`, numbers, or `undefined`

**PossibleVector2**: Generic type (default `number`) accepting `SerializedVector2` or `undefined`

**RectSignal**: Compound signal with `'x'`, `'y'`, `'width'`, `'height'` properties

**SerializedBBox**: Object with `height`, `width`, `x`, `y` properties

**SerializedColor**: String type

**SerializedSpacing**: Object with `bottom`, `left`, `right`, `top` properties

**SerializedVector2**: Generic object with `x` and `y` properties

**SimpleVector2Signal**: Signal for `PossibleVector2` and `Vector2`

**SpacingSignal**: Compound signal for spacing components with `'top'`, `'right'`, `'bottom'`, `'left'` properties

**Vector2Signal**: Compound signal with `'x'` and `'y'` properties

## Variables

**Color**: Static color constructor function (ColorStatic)

**EPSILON**: Constant value of `0.000001`

## Functions

**flipOrigin**: Flips a `Direction` or `Origin` along an optional `Center` axis

**isType**: Type guard checking if value satisfies the `Type` interface

**originToOffset**: "Convert the given origin to a vector representing its offset"

**transformAngle**: Transforms an angle using a `DOMMatrix`

**transformScalar**: Transforms a scalar value using a `DOMMatrix`
