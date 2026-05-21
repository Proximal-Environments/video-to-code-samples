# Logical Separation of Scene Components

A frequent question from Revideo users concerns organizing scene code to "achieve good logical separation and make things readable."

### Custom Generator Functions

Revideo allows defining scene code as a generator function wrapped in `makeScene2D`. Here's a minimal example displaying an image for five seconds:

```typescript
import {Img, makeScene2D, View2D} from '@revideo/2d';
import {waitFor} from '@revideo/core';

export default makeScene2D(function* (view) {
  yield view.add(
    <Img
      width={'30%'}
      ref={logoRef}
      src={
        'https://revideo-example-assets.s3.amazonaws.com/revideo-logo-white.png'
      }
    />,
  );
  yield* waitFor(5);
});
```

To add text to this scene:

```typescript
import {Img, Txt, makeScene2D} from '@revideo/2d';
import {waitFor} from '@revideo/core';

export default makeScene2D(function* (view) {
  yield view.add(
    <Img
      width={'30%'}
      ref={logoRef}
      src={
        'https://revideo-example-assets.s3.amazonaws.com/revideo-logo-white.png'
      }
    />,
  );
  yield view.add(<Txt fill="red" y={300} text={'Hello World!'} />);
  yield* waitFor(5);
});
```

Rather than embedding text addition in your main function, create a separate generator function called within the primary generator:

```typescript
import {Img, Txt, makeScene2D} from '@revideo/2d';
import {waitFor} from '@revideo/core';

export default makeScene2D(function* (view) {
  yield view.add(
    <Img
      width={'30%'}
      ref={logoRef}
      src={
        'https://revideo-example-assets.s3.amazonaws.com/revideo-logo-white.png'
      }
    />,
  );
  yield addText(view, 'Hello World!');
  yield* waitFor(5);
});

function* addText(view: View2D, displayText: string) {
  yield view.add(<Txt fill="red" y={300} text={displayText} />);
  yield* waitFor(5);
}
```

#### Calling generator functions with `yield` and `yield*`

Understanding the distinction between `yield` and `yield*` matters when using multiple generator functions.

Using `yield` calls your generator function but doesn't wait for completion before executing remaining code:

```typescript
yield displaySubtitles();
// rest of your scene code, will get displayed at the same time as subtitles
```

Conversely, `yield*` makes the main generator function wait for `displaySubtitles()` completion before showing remaining animations:

```typescript
yield* displaySubtitles(); // wait for displaySubtitles to finish
// rest of your scene code, will get displayed after subtitles
```

To display two generator functions simultaneously, call both subsequently with `yield`:

```typescript
yield displaySubtitles();
yield displayImages();
```

Alternatively, use the `all` function:

```typescript
yield* all(displaySubtitles(), displayImages());
```

For displaying functions sequentially, call them subsequently with `yield*` or use `chain`:

```typescript
yield* displaySubtitles();
yield* displayImages();
```

This is equivalent to:

```typescript
yield* chain(displaySubtitles(), displayImages());
```

### Custom Components

You can build custom components for Revideo projects. The Motion Canvas guide provides comprehensive guidance on this topic.

**Note:** Most custom component implementations won't require a custom `draw()` function. When implementing one, note that "draw() functions in Revideo need to be implemented as async functions, while they are synchronous in Motion Canvas."
