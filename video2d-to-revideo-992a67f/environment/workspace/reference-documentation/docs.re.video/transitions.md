# Transitions

*Note: These docs were adopted from the original [Motion Canvas](https://motioncanvas.io/docs/) docs*

Transitions allow you to customize the way scenes transition from one into another. A transition is an animation performed at the beginning of the scene. It can modify the context of both the current and the previous scene.

## Before we start

Make sure your project contains at least two scenes. In this example, we've prepared `firstScene.tsx` and `secondScene.tsx`, and configured our project to display one after the other. We'll be setting up our transitions in the second scene.

Make sure to put something different in both scenes to easier see the transitions.

```
my-animation/
└─ src/
   ├─ scenes/
   │  ├─ firstScene.tsx
   │  └─ secondScene.tsx
   └─ project.ts
```

## Pre-made transitions

Motion Canvas comes with a set of common transitions in a form of easy-to-use generators. To use them, `yield*` the transition generator at the beginning of the new scene:

### Example: secondScene.tsx

```typescript
export default makeScene2D(function* (view) {
  // set up the scene:
  view.add(/* your nodes here */);

  // perform a slide transition to the left:
  yield* slideTransition(Direction.Left);

  // proceed with the animation
  yield* waitFor(3);
});
```

**Caution:** Make sure to add nodes to the view before yielding the transition generator. Otherwise, your scene will remain empty until the transition ends.

### `slideTransition`

```
public slideTransition(direction: Direction, duration?: number): ThreadGenerator
public slideTransition(origin: Origin, duration?: number): ThreadGenerator
```

Perform a transition that slides the scene in the given direction.

**Parameters:**
- `direction: Direction` -- The direction in which to slide.
- `duration?: number` -- The duration of the transition.

### `zoomInTransition`

```
public zoomInTransition(area: BBox, duration: number = 0.6): ThreadGenerator
```

Perform a transition that zooms in on a given area of the scene.

**Parameters:**
- `area: BBox` -- The area on which to zoom in.
- `duration: number = 0.6` -- The duration of the transition.

### `zoomOutTransition`

```
public zoomOutTransition(area: BBox, duration: number = 0.6): ThreadGenerator
```

Perform a transition that zooms out from a given area of the scene.

**Parameters:**
- `area: BBox` -- The area from which to zoom out.
- `duration: number = 0.6` -- The duration of the transition.

### `fadeTransition`

```
public fadeTransition(duration: number = 0.6): ThreadGenerator
```

Perform a transition that fades between the scenes.

**Parameters:**
- `duration: number = 0.6` -- The duration of the transition.

## Custom transitions

You can use the `useTransition` function to implement custom transitions. It allows you to specify two callbacks that will modify the contexts of the current and previous scene respectively. The value it returns is a callback that you need to call once you finish the transition.

The transition template looks as follows:

```typescript
// set up the transition
const endTransition = useTransition(
  currentContext => {
    // modify the context of the current scene
  },
  previousContext => {
    // modify the context of the previous scene
  },
);

// perform animations

// finish the transition
endTransition();
```

Here's how you could implement a simple slide transition:

```typescript
export function* slideTransition(
  direction: Direction = Direction.Top,
  duration = 0.6,
): ThreadGenerator {
  const size = useScene().getSize();
  const position = size.getOriginOffset(direction).scale(2);
  const previousPosition = Vector2.createSignal();
  const currentPosition = Vector2.createSignal(position);

  // set up the transition
  const endTransition = useTransition(
    // modify the context of the current scene
    ctx => ctx.translate(currentPosition.x(), currentPosition.y()),
    // modify the context of the previous scene
    ctx => ctx.translate(previousPosition.x(), previousPosition.y()),
  );

  // perform animations
  yield* all(
    previousPosition(position.scale(-1), duration),
    currentPosition(Vector2.zero, duration),
  );

  // finish the transition
  endTransition();
}
```

## Animate when transitioning

By default, Motion Canvas will transition to the next scene once the generator of the current scene has reached the end. In this case, the scene will freeze for the duration of the transition. You can use the `finishScene` function to trigger the transition early, allowing the animation to continue while transitioning:

```typescript
export default makeScene2D(function* (view) {
  yield* animationOne();

  // trigger the transition early:
  finishScene();

  // continue animating:
  yield* animationTwo();
});
```
