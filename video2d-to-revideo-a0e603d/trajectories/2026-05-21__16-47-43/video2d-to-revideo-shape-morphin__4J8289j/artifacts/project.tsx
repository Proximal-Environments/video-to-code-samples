import {makeProject, waitFor} from '@revideo/core';
import {Path, makeScene2D} from '@revideo/2d';

const WIDTH = 480;
const HEIGHT = 360;
const FPS = 24;
const DURATION = 481 / FPS;
const BACKGROUND = '#17182b';
const SHADOW_COLOR = 'rgba(7, 9, 18, 0.34)';
const SHADOW_BLUR = 8;
const SHADOW_OFFSET: [number, number] = [3, 4];
const SHAPE_SIZE = 70;
const SAMPLES = 160;

const columns = [-175.5, -59, 58, 174.5];
const rows = [-115, -0.5, 114.5];

const palette = [
  ['#fd3230', '#32ca33', '#3297fe', '#fdcb00'],
  ['#fd33fb', '#00ccc9', '#fd8800', '#65ff65'],
  ['#c932fc', '#32fdcc', '#fc6664', '#98cbfe'],
] as const;

type Keyframe = readonly [time: number, value: number];

const topExponent: readonly Keyframe[] = [
  [0.0, 2.0],
  [1.0, 2.0],
  [2.0, 3.8],
  [3.0, 12.0],
  [4.0, 180.0],
  [5.4, 180.0],
  [6.3, 120.0],
  [7.3, 40.0],
  [8.1, 24.0],
  [9.1, 36.0],
  [10.0, 180.0],
  [11.8, 180.0],
  [12.6, 18.0],
  [13.5, 4.4],
  [14.2, 2.0],
  [17.0, 2.0],
  [18.0, 4.0],
  [19.0, 14.0],
  [DURATION, 42.0],
] as const;

const topClover: readonly Keyframe[] = [
  [0.0, 0.0],
  [5.8, 0.0],
  [6.7, 0.03],
  [7.6, 0.06],
  [8.3, 0.07],
  [9.2, 0.04],
  [10.0, 0.0],
  [DURATION, 0.0],
] as const;

const middleExponent: readonly Keyframe[] = [
  [0.0, 2.0],
  [4.2, 2.0],
  [5.3, 3.4],
  [6.4, 10.0],
  [7.6, 180.0],
  [12.4, 180.0],
  [13.2, 42.0],
  [14.0, 30.0],
  [15.0, 22.0],
  [16.6, 22.0],
  [17.6, 28.0],
  [18.7, 24.0],
  [DURATION, 36.0],
] as const;

const middleClover: readonly Keyframe[] = [
  [0.0, 0.0],
  [12.7, 0.0],
  [13.5, 0.03],
  [14.5, 0.06],
  [15.1, 0.07],
  [16.6, 0.07],
  [17.6, 0.04],
  [18.6, 0.02],
  [DURATION, 0.0],
] as const;

function clamp01(value: number) {
  return Math.max(0, Math.min(1, value));
}

function easeInOutSine(value: number) {
  return 0.5 - 0.5 * Math.cos(Math.PI * clamp01(value));
}

function sampleTrack(time: number, keyframes: readonly Keyframe[]) {
  if (time <= keyframes[0][0]) {
    return keyframes[0][1];
  }

  for (let index = 1; index < keyframes.length; index += 1) {
    const [endTime, endValue] = keyframes[index];
    if (time <= endTime) {
      const [startTime, startValue] = keyframes[index - 1];
      const duration = Math.max(endTime - startTime, Number.EPSILON);
      const progress = easeInOutSine((time - startTime) / duration);
      return startValue + (endValue - startValue) * progress;
    }
  }

  return keyframes[keyframes.length - 1][1];
}

function shapePath(size: number, exponent: number, clover: number, samples = SAMPLES) {
  const half = size / 2;
  const points: Array<[number, number]> = [];

  for (let index = 0; index < samples; index += 1) {
    const angle = (index / samples) * Math.PI * 2;
    const cos = Math.cos(angle);
    const sin = Math.sin(angle);
    const power =
      Math.pow(Math.abs(cos), exponent) + Math.pow(Math.abs(sin), exponent);
    const superellipseRadius = half / Math.pow(Math.max(power, Number.EPSILON), 1 / exponent);
    const modulation = 1 - clover * Math.cos(angle * 4);
    const radius = superellipseRadius * modulation;
    points.push([radius * cos, radius * sin]);
  }

  let maxExtent = 0;
  for (const [x, y] of points) {
    maxExtent = Math.max(maxExtent, Math.abs(x), Math.abs(y));
  }

  const scale = half / Math.max(maxExtent, Number.EPSILON);
  const scaled = points.map(([x, y]) => [x * scale, y * scale] as [number, number]);

  return scaled
    .map(([x, y], index) => `${index === 0 ? 'M' : 'L'} ${x.toFixed(2)} ${y.toFixed(2)}`)
    .join(' ')
    .concat(' Z');
}

function rowShape(rowIndex: number, time: number) {
  if (rowIndex === 0) {
    return {
      exponent: sampleTrack(time, topExponent),
      clover: sampleTrack(time, topClover),
    };
  }

  if (rowIndex === 1) {
    return {
      exponent: sampleTrack(time, middleExponent),
      clover: sampleTrack(time, middleClover),
    };
  }

  return {
    exponent: 2.0,
    clover: 0.0,
  };
}

const scene = makeScene2D('scene', function* (view) {
  view.fill(BACKGROUND);

  for (let rowIndex = 0; rowIndex < rows.length; rowIndex += 1) {
    for (let columnIndex = 0; columnIndex < columns.length; columnIndex += 1) {
      view.add(
        <Path
          x={columns[columnIndex]}
          y={rows[rowIndex]}
          closed
          lineWidth={0}
          fill={palette[rowIndex][columnIndex]}
          shadowColor={SHADOW_COLOR}
          shadowBlur={SHADOW_BLUR}
          shadowOffset={SHADOW_OFFSET}
          data={() => {
            const time = view.globalTime();
            const shape = rowShape(rowIndex, time);
            return shapePath(SHAPE_SIZE, shape.exponent, shape.clover);
          }}
        />,
      );
    }
  }

  yield* waitFor(DURATION);
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
