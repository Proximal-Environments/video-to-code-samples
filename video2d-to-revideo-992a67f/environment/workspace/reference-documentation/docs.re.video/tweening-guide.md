# Tweening

_Note: These docs were adopted from the original Motion Canvas docs_

Tweens are one of the fundamental building blocks of animation. They are a special type of generators that animate between two values over given time.

## `tween` function

The simplest way to create a tween is via the `tween` function:

```javascript
import {Circle, makeScene2D} from '@revideo/2d';
import {createRef, map, tween} from '@revideo/core';

export default makeScene2D(function* (view) {
  const circle = createRef<Circle>();
  view.add(
    <Circle
      ref={circle}
      x={-300}
      width={240}
      height={240}
      fill="#e13238"
    />,
  );
  yield* tween(2, value => {
    circle().position.x(map(-300, 300, value));
  });
});
```

In the example above, we animate the x coordinate of our circle from `-300` to `300` over a span of `2` seconds.

The `tween` function takes two parameters. The first one specifies the tween duration in seconds. The second is a callback function that will be called each frame the tween takes place. The `value` parameter it receives is a number ranging from `0` to `1`, informing us about the progress of the tween. We can use it to calculate the values that our tween animates. In the case of our circle, we use the `map` function to map the `value` range from `[0, 1]` to `[-300, 300]` and set it as the `x` coordinate.

### Timing functions

At the moment, our animation feels a bit unnatural. The speed with which the `value` parameter changes is constant, which in turn makes the circle move with constant speed. In real life, however, objects have inertia - they take time to speed up and slow down. We can simulate this behavior with timing functions.

A timing function takes a number in the range `[0, 1]` and returns another number in the same range but with a modified rate of change. Motion Canvas provides all the most popular timing functions but since it's a normal JavaScript function you can create your own.

Let's use the `easeInOutCubic` function to fix our animation:

```javascript
yield * tween(2, value => {
  circle().position.x(map(-300, 300, easeInOutCubic(value)));
});
```

Because using timing functions to map a range of values is a really common pattern, it's possible to skip `map` entirely and pass the range to the timing function itself:

```javascript
// This:
map(-300, 300, easeInOutCubic(value));
// Can be simplified to:
easeInOutCubic(value, -300, 300);
```

### Interpolation functions

So far, we've only animated a single, numeric value. The `map` function can be used to interpolate between two numbers but to animate more complex types we'll need to use interpolation functions. Consider the following example:

```javascript
yield * tween(2, value => {
  circle().fill(
    Color.lerp(
      new Color('#e6a700'),
      new Color('#e13238'),
      easeInOutCubic(value),
    ),
  );
});
```

`Color.lerp` is a static function that interpolates between two colors.

**tip:** All complex types in Motion Canvas provide a static method called `lerp` that interpolates between two instances of said type.

Aside from the default linear interpolation, some types offer more advanced functions such as the `Vector2.arcLerp`. It makes the object follow a curved path from point a to b:

```javascript
yield * tween(2, value => {
  circle().position(
    Vector2.arcLerp(
      new Vector2(-300, 200),
      new Vector2(300, -200),
      easeInOutCubic(value),
    ),
  );
});
```

### Tweening properties

The `tween` function is useful when we need to orchestrate complex animations. However, there's a better way of tweening individual properties. The following tween:

```javascript
yield * tween(2, value => {
  circle().color(
    Color.lerp(
      new Color('#e6a700'),
      new Color('#e13238'),
      easeInOutCubic(value),
    ),
  );
});
```

Can be written as:

```javascript
yield * circle().color('#e13238', 2);
```

Here, we use a `SignalTween` signature that looks similar to a setter, except it accepts the transition duration as its second argument.

We can chain multiple tweens together by calling the `to()` method on the returned object:

```javascript
yield * circle().color('#e13238', 2).to('#e6a700', 2);
```

By default, property tweens use `easeInOutCubic` as the timing function. We can override that by providing a third argument:

```javascript
yield * circle().color(
  '#e13238',
  2,
  easeOutQuad,
);
```

Similarly, we can pass a custom interpolation function as the fourth argument:

```javascript
yield * circle().position(
  new Vector2(300, -200),
  2,
  easeInOutCubic,
  Vector2.arcLerp,
);
```

## `spring` function

The `spring` function allows us to interpolate between two values using Hooke's law. We need to provide it with the description of our spring and the `from` and `to` values.

```javascript
import {Circle, makeScene2D} from '@revideo/2d';
import {PlopSpring, SmoothSpring, createRef, spring} from '@revideo/core';

export default makeScene2D(function* (view) {
  const circle = createRef<Circle>();
  view.add(
    <Circle
      ref={circle}
      x={-400}
      size={240}
      fill={'#e13238'}
    />,
  );
  yield* spring(PlopSpring, -400, 400, 1, value => {
    circle().position.x(value);
  });
  yield* spring(SmoothSpring, 400, -400, value => {
    circle().position.x(value);
  });
});
```

### Spring description

The first argument of the `spring` function expects an object that describes the physical properties of our spring:

```javascript
const MySpring = {
  mass: 0.04,
  stiffness: 10.0,
  damping: 0.7,
  initialVelocity: 8.0,
};
```

- `mass` - Describes the inertia of the spring.
- `stiffness` - The coefficient of the spring (k in Hooke's equation).
- `damping` - Causes the spring to lose energy and settle. Set to `0` for indefinite oscillation.
- `initialVelocity` - The initial velocity of the spring.

### Settle tolerance

The optional `settleTolerance` argument defines the minimal distance from the `to` value the spring should reach to be considered settled:

```javascript
yield * spring(PlopSpring, -400, 400, 1 /*...*/)
//                               here ^
```

## Saving and restoring states

All nodes provide a `save` method which allows us to save a snapshot of the node's current state. We can then use the `restore` method to restore the node to the previously saved state.

```javascript
circle().save();
yield * circle().position(new Vector2(300, -200), 2);
yield * circle().restore(1);
```

It is also possible to provide a custom timing function to the `restore` method:

```javascript
yield * circle().restore(1, linear);
```

Node states get stored on a stack. This makes it possible to save more than one state by invoking the `save` method multiple times. When calling `restore`, the node will be restored to the most recently saved state by popping the top entry in the state stack.

```javascript
import {Circle, makeScene2D} from '@revideo/2d';
import {all, createRef} from '@revideo/core';

export default makeScene2D(function* (view) {
  const circle = createRef<Circle>();
  view.add(
    <Circle
      ref={circle}
      size={150}
      position={[-300, -300]}
      fill={'#e13238'}
    />,
  );
  circle().save();
  yield* all(circle().position.x(0, 1), circle().scale(1.5, 1));
  circle().save();
  yield* all(circle().position.y(0, 1), circle().scale(0.5, 1));
  circle().save();
  yield* all(circle().position.x(300, 1), circle().scale(1, 1));
  yield* circle().restore(1);
  yield* circle().restore(1);
  yield* circle().restore(1);
});
```
