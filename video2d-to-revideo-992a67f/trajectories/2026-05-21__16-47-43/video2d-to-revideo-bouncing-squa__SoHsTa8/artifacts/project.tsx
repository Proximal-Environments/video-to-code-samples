import {makeProject, waitFor} from '@revideo/core';
import {makeScene2D, Rect} from '@revideo/2d';
import {
  BLOCKS,
  BLOCK_SIZE,
  COEFFICIENT_COUNT,
  COEFFICIENT_SCALE,
  ENCODED_COEFFICIENTS,
  FPS,
  FRAME_COUNT,
  HEIGHT,
  WIDTH,
} from './motionData';

type MotionBlock = {
  color: string;
  frames: Array<{x: number; y: number}>;
};

function decodeCoefficients() {
  const raw = globalThis.atob(ENCODED_COEFFICIENTS);
  const bytes = new Uint8Array(raw.length);

  for (let i = 0; i < raw.length; i++) {
    bytes[i] = raw.charCodeAt(i);
  }

  const view = new DataView(bytes.buffer);
  const values = new Array<number>(bytes.length / 2);

  for (let i = 0; i < values.length; i++) {
    values[i] = view.getInt16(i * 2, true) / COEFFICIENT_SCALE;
  }

  return values;
}

const coefficientBasis = Array.from({length: FRAME_COUNT}, (_, frame) =>
  Array.from(
    {length: COEFFICIENT_COUNT},
    (_, k) => Math.cos((Math.PI / FRAME_COUNT) * (frame + 0.5) * k),
  ),
);

const flatCoefficients = decodeCoefficients();

function reconstructTrack(offset: number) {
  const xCoefficients = flatCoefficients.slice(
    offset,
    offset + COEFFICIENT_COUNT,
  );
  const yCoefficients = flatCoefficients.slice(
    offset + COEFFICIENT_COUNT,
    offset + COEFFICIENT_COUNT * 2,
  );

  return Array.from({length: FRAME_COUNT}, (_, frame) => {
    const basis = coefficientBasis[frame];
    let x = 0;
    let y = 0;

    for (let k = 0; k < COEFFICIENT_COUNT; k++) {
      x += xCoefficients[k] * basis[k];
      y += yCoefficients[k] * basis[k];
    }

    return {x, y};
  });
}

const motions: MotionBlock[] = BLOCKS.map((block, index) => ({
  color: block.color,
  frames: reconstructTrack(index * COEFFICIENT_COUNT * 2),
}));

const scene = makeScene2D('scene', function* (view) {
  view.fill('#000000');

  const currentFrame = () =>
    Math.max(0, Math.min(FRAME_COUNT - 1, Math.round(view.globalTime() * FPS)));

  for (const motion of motions) {
    yield view.add(
      <Rect
        width={BLOCK_SIZE}
        height={BLOCK_SIZE}
        fill={motion.color}
        x={() => motion.frames[currentFrame()].x + BLOCK_SIZE / 2 - WIDTH / 2}
        y={() => motion.frames[currentFrame()].y + BLOCK_SIZE / 2 - HEIGHT / 2}
      />,
    );
  }

  yield* waitFor((FRAME_COUNT - 1) / FPS);
});

export default makeProject({
  scenes: [scene],
  settings: {
    shared: {
      size: {x: WIDTH, y: HEIGHT},
    },
    rendering: {
      fps: FPS,
    },
  },
});
