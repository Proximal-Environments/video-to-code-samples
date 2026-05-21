# Line Component - Complete API Documentation

## Overview

The `Line` class extends `Curve` and is designed for rendering lines and polygons defined by sets of points.

## Constructor

```typescript
public override new Line(props: LineProps): Line
```

## Key Properties

### Points
```typescript
readonly public points: SimpleSignal<null | SignalValue<Possible<Vector2>[]>>
```
The points defining the line. When set to `null`, uses child node positions.

### Radius
```typescript
readonly public radius: SimpleSignal<number>
```
Controls the corner radius of the line.

### Curve Properties (Inherited)
- `closed`: Whether curve endpoints connect
- `start`/`end`: Percentage clipping boundaries
- `startOffset`/`endOffset`: Pixel-based trimming
- `startArrow`/`endArrow`: Arrow display controls
- `arrowSize`: Arrow dimension control
- `lineWidth`, `lineCap`, `lineJoin`: Stroke styling
- `lineDash`, `lineDashOffset`: Dashed line patterns

### Transform Properties (Inherited)
- `position`, `rotation`, `scale`, `skew`: Local transforms
- `absolutePosition`, `absoluteRotation`, `absoluteScale`: World space equivalents
- `offset`: Origin point control

### Layout Properties (Inherited)
- `size`, `width`, `height`: Dimensions
- `margin`, `padding`: Spacing controls
- `layout`: Layout mode configuration

### Visual Properties (Inherited)
- `fill`, `stroke`: Canvas styles
- `opacity`: Transparency (0-1)
- `filters`: Visual effects
- `cache`, `cachePadding`: Performance optimization
- `shadowBlur`, `shadowColor`, `shadowOffset`: Shadow effects

## Core Methods

### Measurement
```typescript
public arcLength(): number
public baseArcLength(): number
public offsetArcLength(): number
public completion(): number
public distanceToPercentage(value: number): number
public percentageToDistance(value: number): number
public getPointAtPercentage(value: number): CurvePoint
```

### Geometry
```typescript
public parsedPoints(): Vector2[]
public profile(): CurveProfile
public getPath(): Path2D
```

### Rendering
```typescript
public render(context: CanvasRenderingContext2D): Promise<void>
public drawOverlay(context: CanvasRenderingContext2D, matrix: DOMMatrix): void
```

### State Management
```typescript
public getState(): NodeState
public applyState(state: NodeState): void
public applyState(state: NodeState, duration: number, timing?: TimingFunction): ThreadGenerator
public save(): void
public restore(): void
public restore(duration: number, timing?: TimingFunction): ThreadGenerator
```

### Transformation
```typescript
public localToParent(): DOMMatrix
public localToWorld(): DOMMatrix
public worldToLocal(): DOMMatrix
public worldToParent(): DOMMatrix
```

### Cloning
```typescript
public clone(customProps?: NodeState): Line
public reactiveClone(customProps?: NodeState): Line
public snapshotClone(customProps?: NodeState): Line
```

### Tree Operations
```typescript
public add(node: ComponentChildren): Line
public insert(node: ComponentChildren, index?: number): Line
public remove(): Line
public move(by?: number): Line
public moveAbove(node: Node, directlyAbove?: boolean): Line
public moveBelow(node: Node, directlyBelow?: boolean): Line
public moveToTop(): Line
public moveToBottom(): Line
```

### Child Management
```typescript
public peekChildren(): readonly Node[]
public childrenAs<T extends Node>(): T[]
public childAs<T extends Node>(index: number): null | T
public findFirst<T extends Node>(predicate: (node: Node) => node is T): null | T
public findAll<T extends Node>(predicate: (node: Node) => node is T): T[]
```

### Utilities
```typescript
public hit(position: Vector2): null | Node
public view(): View2D
public toPromise(): Promise<Line>
public absoluteOpacity(): number
```

## Example Usage

```typescript
import { makeScene2D } from '@revideo/2d';
import { Line } from '@revideo/2d/lib/components';

export default makeScene2D(function* (view) {
  view.add(
    <Line
      points={[
        [150, 50],
        [0, -50],
        [-150, 50],
      ]}
      stroke={'lightseagreen'}
      lineWidth={8}
      radius={40}
      startArrow
    />,
  );
});
```

## Inherited Type Definitions

The `Line` component inherits properties and methods from `Curve`, which extends `Node`. Key inherited signal types include `SimpleSignal<T>`, `Vector2Signal`, and `CanvasStyleSignal` for reactive property management.
