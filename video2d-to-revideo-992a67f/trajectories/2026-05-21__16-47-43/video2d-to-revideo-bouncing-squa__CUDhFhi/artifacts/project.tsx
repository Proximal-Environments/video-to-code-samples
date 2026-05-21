import {makeProject, createSignal, tween, linear} from '@revideo/core';
import {makeScene2D, Rect} from '@revideo/2d';

const W = 480;
const H = 360;
const S = 50;
const FPS = 24;
const DURATION = 18;

const XLO = -W / 2 + S / 2;
const XHI = W / 2 - S / 2;
const YLO = -H / 2 + S / 2;
const YHI = H / 2 - S / 2;

function reflect(p: number, lo: number, hi: number): number {
  const range = hi - lo;
  if (range <= 0) return lo;
  let d = ((p - lo) % (2 * range) + 2 * range) % (2 * range);
  if (d > range) d = 2 * range - d;
  return lo + d;
}

type Ball = {
  color: string;
  px: number;
  py: number;
  vx: number;
  vy: number;
};

const COL_X = [-160, -65, 40, 140];
const ROW_Y = [-122, -19, 83];

const grid = (col: number, row: number) => ({
  px: COL_X[col],
  py: ROW_Y[row],
});

const balls: Ball[] = [
  {color: '#ff0000', ...grid(0, 0), vx: -1.0, vy: -1.0},
  {color: '#00ff00', ...grid(1, 0), vx: -2.5, vy: 0.5},
  {color: '#0000ff', ...grid(2, 0), vx: 2.0, vy: -3.0},
  {color: '#ffff00', ...grid(3, 0), vx: -2.2, vy: -3.8},
  {color: '#ff00ff', ...grid(0, 1), vx: 2.5, vy: 4.7},
  {color: '#00ffff', ...grid(1, 1), vx: -6.2, vy: -1.0},
  {color: '#ff8000', ...grid(2, 1), vx: -1.0, vy: 7.0},
  {color: '#8000ff', ...grid(3, 1), vx: -5.7, vy: -6.0},
  {color: '#00ff80', ...grid(0, 2), vx: 6.0, vy: -6.5},
  {color: '#ff0080', ...grid(1, 2), vx: -9.5, vy: 1.5},
  {color: '#80ff00', ...grid(2, 2), vx: 0.0, vy: 10.78},
  {color: '#0080ff', ...grid(3, 2), vx: 8.6, vy: -7.9},
];

const scene = makeScene2D('scene', function* (view) {
  view.fill('#000000');

  const t = createSignal(0);

  for (const b of balls) {
    view.add(
      <Rect
        fill={b.color}
        size={[S, S]}
        position={() => {
          const frame = t() * FPS;
          const rawX = b.px + b.vx * frame;
          const rawY = b.py + b.vy * frame;
          return [reflect(rawX, XLO, XHI), reflect(rawY, YLO, YHI)];
        }}
      />,
    );
  }

  yield* tween(DURATION, v => t(DURATION * v), linear);
});

export default makeProject({
  scenes: [scene],
  settings: {
    shared: {
      size: {x: W, y: H},
    },
    rendering: {
      fps: FPS,
    },
  },
});
