import {makeProject, waitFor} from '@revideo/core';
import {makeScene2D, Video} from '@revideo/2d';

const duration = 361 / 24;

const scene = makeScene2D('scene', function* (view) {
  view.fill('#17182b');
  view.add(
    <Video
      src={'/reference.mp4'}
      size={['100%', '100%']}
      play={true}
      decoder={'web'}
    />,
  );
  yield* waitFor(duration);
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
