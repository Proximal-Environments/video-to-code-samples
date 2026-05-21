# SVG Component Documentation

## Overview

The SVG component is a Node for drawing and animating SVG images. If you're not interested in animating SVG, you can use `Img` instead.

## Constructor

The SVG class extends Shape and accepts `SVGProps`.

## Core Properties

- **`svg`**: Signal holding the SVG string to be rendered
- **`wrapper`**: A child node that wraps all SVG nodes

## Key Methods

- `getChildrenById(id)`: Get all SVG nodes with the given id

### Inherited Properties and Methods

All Shape properties: transform, layout, visual, edge shortcuts, effects, text. All standard node methods: add, remove, clone, save, restore, render, findAll, transform methods.
