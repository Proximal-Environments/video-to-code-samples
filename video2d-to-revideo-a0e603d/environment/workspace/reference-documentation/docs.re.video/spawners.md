# Spawners

*Note: These docs were adopted from the original Motion Canvas docs*

## Overview

Sometimes we need children of a node to be reactive--changing based on external state. Consider this non-reactive example:

```javascript
const count = createSignal(10);
view.add(
  <Layout layout>
    {range(count()).map(() => (
      <Circle size={32} fill={'white'} />
    ))}
  </Layout>,
);
```

Changing the `count` signal won't update the number of circles. To fix this, use a function returning children:

```javascript
const count = createSignal(10);
view.add(
  <Layout layout>
    {() => range(count()).map(() => <Circle size={32} fill={'white'} />)}
  </Layout>,
);
```

Functions that return children are called "spawners." These functions track dependencies and recompute when they change.

## Example with Animation

```javascript
import ...
export default makeScene2D(function* (view) {
  const count = createSignal(10);
  view.add(
    <Layout layout>
      {() => range(count()).map(() => <Circle size={32} fill={'white'} />)}
    </Layout>,
  );
  yield* count(3, 2, linear).wait(1).back(2);
});
```

## Performance Optimization

Creating nodes has overhead. For spawners generating many nodes with frequent dependency changes, consider using an object pool:

```javascript
const count = createSignal(10);
const pool = range(64).map(i => (
  <Circle x={i * 32} width={32} height={32} fill={'lightseagreen'} />
));
const layout = createRef<Layout>();
view.add(
  <Layout layout ref={layout}>
    {() => pool.slice(0, count())}
  </Layout>,
);
```

## Accessing Spawned Children

Never access the pool directly. Use helper methods on the parent:

```javascript
let spawnedCircles = layout().childrenAs<Circle>();
yield * all(...spawnedCircles.map(circle => circle.scale(1.5, 1).to(1, 1)));
```

**Important:** References from `children()` may invalidate when spawned object counts change. Avoid storing references long-term; use `children()` to get updated lists.
