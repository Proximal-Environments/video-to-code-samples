import {makeProject} from '@revideo/core';
import {makeScene2D} from '@revideo/2d';
import {waitFor} from '@revideo/core';

const scene = makeScene2D('scene', function* (view) {
  view.fill('#000000');
  yield* waitFor(1);
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
