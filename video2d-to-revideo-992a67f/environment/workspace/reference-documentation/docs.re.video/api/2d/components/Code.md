# Code Component Documentation

## Overview

The `Code` component is an experimental node for displaying and animating code within Revideo animations. It extends the `Shape` class and provides syntax highlighting and selection capabilities.

## Constructor

```typescript
public override new Code(props: CodeProps): Code
```

## Core Properties

### `code`
```typescript
readonly public code: CodeSignal
```
The code to display.

### `highlighter`
```typescript
readonly public highlighter: SimpleSignal<null | CodeHighlighter<unknown>>
```
The code highlighter to use for this code node. Defaults to a shared LezerHighlighter.

### `selection`
```typescript
readonly public selection: Signal<PossibleCodeSelection, CodeSelection, SignalContext>
```
The currently selected code range.

### `drawHooks`
```typescript
readonly public drawHooks: SimpleSignal<DrawHooks>
```
Custom drawing logic for the code.

## Key Methods

### Selection Operations

- `findAllRanges(pattern: string | RegExp): CodeRange[]` - Find all code ranges matching a pattern
- `findFirstRange(pattern: string | RegExp): CodeRange` - Find the first matching code range
- `findLastRange(pattern: string | RegExp): CodeRange` - Find the last matching code range

### Bounding Box Operations

- `getPointBbox(point: CodePoint): BBox` - Return the bounding box of a character
- `getSelectionBbox(selection: PossibleCodeSelection): BBox[]` - Return bounding boxes of all characters in the selection

### Parsing

- `parsed(): string` - Get the currently displayed code as a string

### Signal Creation

- `createSignal(initial: PossibleCodeScope): CodeSignal` - Create a child code signal
- `static createSignal(initial: PossibleCodeScope, highlighter?): CodeSignal<void>` - Create a standalone code signal

## Inherited Properties

Transform, sizing, styling, layout, and effects from `Shape`.

## Example Usage

```typescript
import ...
export default makeScene2D(function* (view) {
  LezerHighlighter.registerParser(parser);
  const code = createRef<Code>();
  view.add(
    <Code
      ref={code}
      offset={-1}
      position={view.size().scale(-0.5).add(60)}
      fontFamily={'JetBrains Mono, monospace'}
      fontSize={36}
      code={`\
function hello() {
  console.log('Hello');
}`}
    />,
  );
  yield* code()
    .code(
      `\
function hello() {
  console.warn('Hello World');
}`,
      1,
    )
    .wait(0.5)
    .back(1)
    .wait(0.5);
});
```

**Status**: This is an experimental feature.
