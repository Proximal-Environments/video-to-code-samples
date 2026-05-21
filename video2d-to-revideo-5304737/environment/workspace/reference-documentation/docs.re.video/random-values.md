# Random values

*Note: These docs were adopted from the original [Motion Canvas](https://motioncanvas.io/docs/) docs*

Randomly generated values can introduce variety and unpredictability into animations. In Motion Canvas, use the [`useRandom()`](/api/core/utils#useRandom) function to access a random number generator (RNG) for the current scene:

```javascript
import {useRandom} from '@revideo/core';

const random = useRandom();
const integer = random.nextInt(0, 10);
```

The `nextInt()` method returns an integer between 0 and 10 (exclusive). Refer to the [`Random` api](/api/core/scenes/Random) for all available methods.

## Reproducibility

Unlike `Math.random()`, `useRandom()` is completely reproducible. Each animation playback generates identical values. The seed for number generation is stored in each scene's meta file.

You can supply your own seed to discover a sequence that fits your needs:

```javascript
const random = useRandom(123);
```

## Example: Sound Wave Animation

This example demonstrates creating a sound-wave effect using randomized rectangle heights:

```javascript
import {Layout, Rect, makeScene2D} from '@revideo/2d';
import {all, loop, makeRef, range, sequence, useRandom} from '@revideo/core';

export default makeScene2D(function* (view) {
  const random = useRandom();
  const rects: Rect[] = [];
  
  view.add(
    <Layout layout gap={10} alignItems="center">
      {range(40).map(i => (
        <Rect
          ref={makeRef(rects, i)}
          radius={5}
          width={10}
          height={10}
          fill={'#e13238'}
        />
      ))}
    </Layout>,
  );
  
  yield* loop(3, () =>
    sequence(
      0.04,
      ...rects.map(rect =>
        all(
          rect.size.y(random.nextInt(100, 200), 0.5).to(10, 0.5),
          rect.fill('#e6a700', 0.5).to('#e13238', 0.5),
        ),
      ),
    ),
  );
});
```
