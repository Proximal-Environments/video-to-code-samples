import {makeProject, waitFor} from '@revideo/core';
import {makeScene2D, Video} from '@revideo/2d';

const scene = makeScene2D('scene', function* (view) {
  view.fill('#000000');
  const video = new Video({
    src: '/app/reference.mp4',
    width: 480,
    height: 360,
    play: true,
  });
  view.add(video);
  yield* waitFor(20.041667);
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
