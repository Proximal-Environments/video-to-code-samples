import {makeProject} from '@revideo/core';
import {Line, makeScene2D} from '@revideo/2d';
import {createRef, range} from '@revideo/core';

const W = 480;
const H = 360;
const FPS = 24;
const DUR = 20;
const ROWS = 3;
const COLS = 4;
const N = ROWS * COLS;
const COLORS = [
  '#ff3333', '#33cc33', '#3399ff', '#ffcc00',
  '#ff33ff', '#00cccc', '#ff8800', '#66ff66',
  '#cc33ff', '#33ffcc', '#ff6666', '#99ccff',
];
const SIZE = 35;
const M = 30;
const N_PTS = 32;

const ROW_SPEEDS = [2.5, 1.25, 0.25];

function clamp(v: number, lo: number, hi: number) {
  return Math.max(lo, Math.min(hi, v));
}

function morphShape(cx: number, cy: number, size: number, morph1: number, morph2: number): [number, number][] {
  const pts: [number, number][] = [];
  for (let i = 0; i < N_PTS; i++) {
    const angle = (i * 2 * Math.PI) / N_PTS;
    const ca = Math.cos(angle);
    const sa = Math.sin(angle);

    const circleX = cx + size * ca;
    const circleY = cy + size * sa;

    const squareX = cx + size * clamp(ca * 2, -1, 1);
    const squareY = cy + size * clamp(sa * 2, -1, 1);

    const diamondX = cx + size * ca * (Math.abs(ca) + Math.abs(sa));
    const diamondY = cy + size * sa * (Math.abs(ca) + Math.abs(sa));

    const x = circleX * (1 - morph1) + squareX * morph1 * (1 - morph2) + diamondX * morph2;
    const y = circleY * (1 - morph1) + squareY * morph1 * (1 - morph2) + diamondY * morph2;

    pts.push([clamp(x, M, W - M) - W / 2, clamp(y, M, H - M) - H / 2]);
  }
  return pts;
}

function computeMorph(progress: number, speed: number): [number, number] {
  let p = (progress * speed) % 2;
  if (p > 1) p = 2 - p;

  let b12: number, b23: number;
  if (p < 0.25) {
    b12 = 0; b23 = 0;
  } else if (p < 0.5) {
    b12 = (p - 0.25) / 0.25; b23 = 0;
  } else if (p < 0.75) {
    b12 = 1; b23 = 0;
  } else {
    b12 = 1; b23 = (p - 0.75) / 0.25;
  }
  return [b12, b23];
}

const scene = makeScene2D('scene', function* (view) {
  view.fill('#1a1a2e');

  const refs = range(N).map(() => createRef<Line>());

  for (let i = 0; i < N; i++) {
    view.add(
      <Line
        ref={refs[i]}
        closed={true}
        fill={COLORS[i]}
        points={[[0, 0]]}
      />,
    );
  }

  const dt = 1 / FPS;
  const rowY = [M + SIZE, H / 2, H - M - SIZE];

  for (let frame = 0; frame < DUR * FPS; frame++) {
    const t = frame * dt;
    const progress = t / DUR;

    for (let row = 0; row < ROWS; row++) {
      const [b12, b23] = computeMorph(progress, ROW_SPEEDS[row]);

      for (let col = 0; col < COLS; col++) {
        const idx = row * COLS + col;
        const cx = M + SIZE + (col * (W - 2 * M - 2 * SIZE)) / Math.max(1, COLS - 1);
        const cy = rowY[row];
        const pts = morphShape(cx, cy, SIZE, b12, b23);
        refs[idx]().points(pts);
      }
    }

    yield;
  }
});

export default makeProject({
  scenes: [scene],
  settings: {
    shared: {
      size: {x: W, y: H},
      background: '#1a1a2e',
      range: [0, DUR],
    },
    rendering: {
      fps: FPS,
    },
  },
});
