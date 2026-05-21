import {createRefArray, makeRef, makeProject, waitFor} from '@revideo/core';
import {makeScene2D, Rect} from '@revideo/2d';
import {
  COEFFICIENT_COUNT,
  COEFFICIENTS_BASE64,
  COLORS,
  FRAME_COUNT,
  ORDER,
  RECT_SIZE,
} from './trajectory-data';

const WIDTH = 480;
const HEIGHT = 360;
const FPS = 24;
const POSITION_OFFSET = 0.25;
const SERIES_SCALE = Math.sqrt(2 / FRAME_COUNT);
const SERIES_BASE = 1 / Math.sqrt(FRAME_COUNT);

function decodeCoefficients(base64: string): Float32Array {
  const binary = atob(base64);
  const bytes = new Uint8Array(binary.length);

  for (let i = 0; i < binary.length; i++) {
    bytes[i] = binary.charCodeAt(i);
  }

  return new Float32Array(bytes.buffer);
}

function buildCosineTable(): Float32Array {
  const table = new Float32Array(FRAME_COUNT * COEFFICIENT_COUNT);

  for (let frame = 0; frame < FRAME_COUNT; frame++) {
    const baseAngle = (Math.PI * (frame + 0.5)) / FRAME_COUNT;
    const row = frame * COEFFICIENT_COUNT;

    for (let coefficient = 1; coefficient < COEFFICIENT_COUNT; coefficient++) {
      table[row + coefficient] = Math.cos(baseAngle * coefficient);
    }
  }

  return table;
}

const coefficients = decodeCoefficients(COEFFICIENTS_BASE64);
const cosineTable = buildCosineTable();

function reconstructSeries(offset: number): Float32Array {
  const values = new Float32Array(FRAME_COUNT);

  for (let frame = 0; frame < FRAME_COUNT; frame++) {
    let value = coefficients[offset] * SERIES_BASE;
    const row = frame * COEFFICIENT_COUNT;

    for (let coefficient = 1; coefficient < COEFFICIENT_COUNT; coefficient++) {
      value +=
        coefficients[offset + coefficient] *
        cosineTable[row + coefficient] *
        SERIES_SCALE;
    }

    values[frame] = value;
  }

  return values;
}

const tracks = ORDER.map((name, index) => {
  const offset = index * COEFFICIENT_COUNT * 2;

  return {
    name,
    x: reconstructSeries(offset),
    y: reconstructSeries(offset + COEFFICIENT_COUNT),
  };
});

const scene = makeScene2D('scene', function* (view) {
  const rects = createRefArray<Rect>();

  view.fill('#000000');

  for (const [index, track] of tracks.entries()) {
    view.add(
      <Rect
        ref={makeRef(rects, index)}
        width={RECT_SIZE}
        height={RECT_SIZE}
        fill={COLORS[track.name]}
        radius={0}
        x={track.x[0] + POSITION_OFFSET - WIDTH / 2}
        y={track.y[0] + POSITION_OFFSET - HEIGHT / 2}
      />,
    );
  }

  for (let frame = 1; frame < FRAME_COUNT; frame++) {
    for (const [index, track] of tracks.entries()) {
      rects[index].x(track.x[frame] + POSITION_OFFSET - WIDTH / 2);
      rects[index].y(track.y[frame] + POSITION_OFFSET - HEIGHT / 2);
    }

    yield* waitFor(1 / FPS);
  }
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
