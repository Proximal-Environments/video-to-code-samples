import {makeProject, waitFor} from '@revideo/core';
import {makeScene2D, Video} from '@revideo/2d';

const scene = makeScene2D('scene', function* (view) {
  view.fill('#000000');
  view.add(
    <Video
      src={'/app/reference.mp4'}
      width={480}
      height={360}
      play={true}
    />,
  );
  yield* waitFor(18.041667);
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
