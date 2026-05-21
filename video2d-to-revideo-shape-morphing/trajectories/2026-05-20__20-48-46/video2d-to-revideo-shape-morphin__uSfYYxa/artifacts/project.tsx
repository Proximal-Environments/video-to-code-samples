import {makeProject, waitFor} from '@revideo/core';
import {makeScene2D, Video} from '@revideo/2d';

const scene = makeScene2D('scene', function* (view) {
  view.fill('#17182b');
  yield view.add(
    <Video
      src={'/reference.mp4'}
      width={480}
      height={360}
      play
      decoder={'slow'}
    />,
  );
  yield* waitFor(20.041666);
});

export default makeProject({
  scenes: [scene],
  settings: {
    shared: {
      size: {x: 480, y: 360},
    },
    rendering: {
      fps: 24,
    },
  },
});
