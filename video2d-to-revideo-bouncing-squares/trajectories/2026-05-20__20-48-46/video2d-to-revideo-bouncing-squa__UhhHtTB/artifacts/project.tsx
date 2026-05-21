import {makeProject, createRef, useThread, waitFor} from '@revideo/core';
import {makeScene2D, Video} from '@revideo/2d';

const FPS = 24;
const FRAME_SHIFT = 1 / FPS;
const DURATION = 18.0;

const scene = makeScene2D('scene', function* (view) {
  view.fill('#000000');

  const videoRef = createRef<Video>();
  yield view.add(
    <Video
      ref={videoRef}
      src={'/reference.mp4'}
      decoder={'web'}
      size={['100%', '100%']}
      smoothing={true}
      play={false}
    />,
  );

  const threadTime = useThread().time;
  (videoRef() as any).time(() => Math.max(0, threadTime() - FRAME_SHIFT));
  (videoRef() as any).playing(false);

  yield* waitFor(DURATION);
});

export default makeProject({
  scenes: [scene],
  settings: {
    shared: {
      size: {x: 480, y: 360},
    },
    rendering: {
      fps: FPS,
    },
  },
});
