# Animation Flow

*Note: These docs were adopted from the original Motion Canvas docs*

## Overview

Motion Canvas employs generator functions to define animations. A generator function can yield multiple values, pausing execution at each `yield` keyword until the caller requests the next value.

> "yield means: 'The current frame is ready, display it on the screen and come back to me later.'"

### Basic Generator Concept

Generators use the `yield` keyword to pause execution:

```javascript
function* example() {
  yield 1;
  yield 2;
  yield 3;
}
```

### Simple Animation Example

```javascript
export default makeScene2D(function* (view) {
  const circle = createRef<Circle>();
  view.add(<Circle ref={circle} width={100} height={100} />);
  circle().fill('red');
  yield;
  circle().fill('blue');
  yield;
  circle().fill('red');
  yield;
});
```

### Code Reusability with `yield*`

The `yield*` keyword delegates yielding to another generator, enabling code reuse:

```javascript
yield* flicker(circle());

function* flicker(circle: Circle): ThreadGenerator {
  circle.fill('red');
  yield;
  circle.fill('blue');
  yield;
  circle.fill('red');
  yield;
}
```

Tweens animate between values over time:

```javascript
yield * myCircle().fill('#e6a700', 1);
```

## Flow Generators

Flow generators combine multiple generators together:

### `all`
Runs all tasks concurrently and waits for completion.

### `any`
Runs all tasks concurrently but waits for only the first to finish.

### `chain`
Executes tasks sequentially, one after another.

### `delay`
Runs a generator or callback after a specified time delay in seconds.

### `sequence`
Starts tasks sequentially with constant delays between them, without waiting for previous tasks to complete.

### `loop`
Repeats a generator in a loop. Each iteration completes before the next begins.

## Looping Patterns

**Array.map with all:**
```javascript
yield * all(
  ...rects.map(rect =>
    rect.position.y(100, 1).to(-100, 2).to(0, 1),
  ),
);
```

**For loop with generator array:**
```javascript
const generators = [];
for (const rect of rects) {
  generators.push(rect.position.y(100, 1).to(-100, 2).to(0, 1));
}
yield * all(...generators);
```

**For loop with manual timing:**
```javascript
for (const rect of rects) {
  yield rect.position.y(100, 1).to(-100, 2).to(0, 1);
}
yield * waitFor(4);
```
