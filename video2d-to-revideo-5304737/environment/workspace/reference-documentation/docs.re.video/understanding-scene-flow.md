# Scene Flow | Revideo

Revideo enables video creation through generator functions. This page explains how scenes work sequentially and clarifies the distinctions between `yield`, `yield*`, and calling functions directly.

## Scenes are defined sequentially

Generator functions operate as sequences of `yield` statements. Each call to the generator returns the next yielded value:

```javascript
function* example() {
  yield 1;
  yield 2;
  yield 3;
}
const generator = example();
console.log(generator.next().value); // 1
console.log(generator.next().value); // 2
console.log(generator.next().value); // 3
```

This approach allows developers to describe videos as "a sequence of concrete steps," making code readable from top to bottom. For example:

- A red circle appears at center
- The circle moves right 200 pixels in 2 seconds
- The circle disappears
- Nothing happens for 1 second

Code example:

```javascript
import ...
export default makeScene2D(function* (view) {
  const circleRef = createRef<Circle>();
  yield view.add(<Circle fill={'red'} size={100} ref={circleRef} />);
  yield* circleRef().position.x(200, 2);
  circleRef().remove();
  yield* waitFor(1);
});
```

For parallel animations, use flow generators like `all`.

## `yield` vs `yield*` vs no yield

### `yield view.add` vs `view.add`

Adding `yield` ensures Revideo awaits promises associated with operations, such as network requests or font loading. This is particularly important for image loading:

```javascript
yield view.add(
  <Img
    src={'https://revideo-example-assets.s3.amazonaws.com/revideo-logo-white.png'}
  />,
);
```

Text nodes also create promises as Revideo waits for the `document.fonts.ready` event. If you neglect `yield` before an async operation, Revideo warns: "Tried to access an asynchronous property before the node was ready."

### Will calling `yield` add an extra frame?

Not necessarily. According to the documentation, "a `yield` will only correspond to a frame when the yielded value is falsy." The rendering process awaits promises and only draws frames when yield values are empty.

### `yield` vs `yield*`

Use `yield` for single operations and `yield*` for generators producing multiple frames:

```javascript
yield view.add(<Img src={'img.png'} />); // single operation
yield* waitFor(1); // multiple frames
```
