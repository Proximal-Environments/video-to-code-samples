import {createSignal, makeProject} from '@revideo/core';
import {makeScene2D, Rect} from '@revideo/2d';

const W = 480;
const H = 360;
const BG = '#17182b';
const DURATION = 20;

const cols = [-168, -56, 56, 168];
const rows = [-108, 0, 108];

const topColors = ['#fb3232', '#31cb32', '#3298f9', '#feca01'];
const midColors = ['#fb34fb', '#00cccb', '#f98903', '#64ff63'];
const botColors = ['#ca32fc', '#32fdcc', '#e25e5f', '#7da4d0'];

const topTimes = [0, 4.5, 8, 16, 20];
const topW = [
  [66, 68, 66, 72],
  [70, 72, 72, 74],
  [74, 76, 76, 78],
  [66, 68, 66, 72],
  [70, 72, 74, 74],
];
const topH = [
  [72, 72, 72, 72],
  [74, 76, 76, 78],
  [72, 72, 72, 74],
  [72, 72, 72, 72],
  [72, 74, 74, 76],
];
const topR = [
  [30, 30, 30, 30],
  [24, 24, 24, 24],
  [12, 12, 12, 12],
  [30, 30, 30, 30],
  [20, 20, 20, 20],
];
const topGlow = [
  [0.10, 0.10, 0.10, 0.10],
  [0.18, 0.18, 0.18, 0.18],
  [0.32, 0.32, 0.32, 0.32],
  [0.10, 0.10, 0.10, 0.10],
  [0.16, 0.16, 0.16, 0.16],
];

const midTimes = [0, 8, 16, 20];
const midW = [
  [68, 70, 70, 68],
  [70, 72, 72, 70],
  [74, 78, 78, 74],
  [68, 72, 74, 76],
];
const midH = [
  [68, 68, 68, 68],
  [70, 70, 70, 70],
  [78, 78, 78, 80],
  [68, 68, 68, 68],
];
const midR = [
  [34, 34, 34, 34],
  [28, 28, 28, 28],
  [12, 12, 12, 12],
  [24, 24, 24, 24],
];
const midGlow = [
  [0.08, 0.08, 0.08, 0.08],
  [0.14, 0.14, 0.14, 0.14],
  [0.24, 0.24, 0.24, 0.24],
  [0.12, 0.12, 0.12, 0.12],
];

const botW = [62, 62, 62, 62];
const botH = [62, 62, 62, 62];
const botR = [22, 22, 22, 22];
const botGlow = [0.32, 0.32, 0.32, 0.32];

const mix = (a: number, b: number, t: number) => a + (b - a) * t;
const clamp = (v: number, a = 0, b = 1) => Math.max(a, Math.min(b, v));
const smooth = (t: number) => t * t * (3 - 2 * t);

function key(t: number, times: number[], values: number[]) {
  if (t <= times[0]) return values[0];
  for (let i = 0; i < times.length - 1; i++) {
    if (t <= times[i + 1]) {
      const p = smooth(clamp((t - times[i]) / (times[i + 1] - times[i])));
      return mix(values[i], values[i + 1], p);
    }
  }
  return values[values.length - 1];
}

function keyCell(t: number, times: number[], frames: number[][], c: number) {
  return key(t, times, frames.map(frame => frame[c]));
}

const scene = makeScene2D('scene', function* (view) {
  view.fill(BG);
  const time = createSignal(0);

  for (let c = 0; c < 4; c++) {
    view.add(
      <Rect
        x={cols[c]}
        y={rows[0]}
        width={() => keyCell(time(), topTimes, topW, c) + 8}
        height={() => keyCell(time(), topTimes, topH, c) + 8}
        radius={() => keyCell(time(), topTimes, topR, c) + 3}
        fill={topColors[c]}
        opacity={() => keyCell(time(), topTimes, topGlow, c)}
      />,
    );
    view.add(
      <Rect
        x={cols[c]}
        y={rows[0]}
        width={() => keyCell(time(), topTimes, topW, c)}
        height={() => keyCell(time(), topTimes, topH, c)}
        radius={() => keyCell(time(), topTimes, topR, c)}
        fill={topColors[c]}
      />,
    );

    view.add(
      <Rect
        x={cols[c]}
        y={rows[1]}
        width={() => keyCell(time(), midTimes, midW, c) + 8}
        height={() => keyCell(time(), midTimes, midH, c) + 8}
        radius={() => keyCell(time(), midTimes, midR, c) + 3}
        fill={midColors[c]}
        opacity={() => keyCell(time(), midTimes, midGlow, c)}
      />,
    );
    view.add(
      <Rect
        x={cols[c]}
        y={rows[1]}
        width={() => keyCell(time(), midTimes, midW, c)}
        height={() => keyCell(time(), midTimes, midH, c)}
        radius={() => keyCell(time(), midTimes, midR, c)}
        fill={midColors[c]}
      />,
    );

    view.add(
      <Rect
        x={cols[c]}
        y={rows[2]}
        width={botW[c] + 8}
        height={botH[c] + 8}
        radius={botR[c] + 3}
        rotation={45}
        fill={botColors[c]}
        opacity={botGlow[c]}
      />,
    );
    view.add(
      <Rect
        x={cols[c]}
        y={rows[2]}
        width={botW[c]}
        height={botH[c]}
        radius={botR[c]}
        rotation={45}
        fill={botColors[c]}
      />,
    );
  }

  yield* time(DURATION, DURATION);
});

export default makeProject({
  scenes: [scene],
  settings: {
    shared: {
      size: {x: W, y: H},
    },
    rendering: {
      fps: 24,
    },
  },
});
