import {makeProject, createRef, useTime} from '@revideo/core';
import {makeScene2D, Rect} from '@revideo/2d';

const W = 480;
const H = 360;
const FPS = 24;
const DURATION = 18;
const SIZE = 50;
const HALF = SIZE / 2;

interface Square {
  color: string;
  x: number;
  y: number;
  vx: number;
  vy: number;
}

const INIT: Square[] = [
  {color: '#ff0000', x: 80, y: 60, vx: -1.5, vy: -1.0},
  {color: '#00ff00', x: 180, y: 60, vx: -2.0, vy: 0.5},
  {color: '#0000ff', x: 280, y: 60, vx: 2.0, vy: -8 / 3},
  {color: '#ffff00', x: 380, y: 60, vx: -2.0, vy: -4.0},
  {color: '#ff00ff', x: 80, y: 160, vx: 2.0, vy: 4.5},
  {color: '#00ffff', x: 180, y: 160, vx: -6.0, vy: -1.0},
  {color: '#ff8000', x: 280, y: 160, vx: -1.0, vy: 7.0},
  {color: '#8000ff', x: 380, y: 160, vx: -6.0, vy: -6.0},
  {color: '#00ff80', x: 80, y: 260, vx: 6.0, vy: -6.5},
  {color: '#ff0080', x: 180, y: 260, vx: -10.0, vy: 2.0},
  {color: '#80ff00', x: 280, y: 260, vx: 0.0, vy: 32 / 3},
  {color: '#0080ff', x: 380, y: 260, vx: 8.0, vy: -8.0},
];

function bounceWalls(s: Square) {
  if (s.x < HALF) {
    s.x = 2 * HALF - s.x;
    s.vx = -s.vx;
  }
  if (s.x > W - HALF) {
    s.x = 2 * (W - HALF) - s.x;
    s.vx = -s.vx;
  }
  if (s.y < HALF) {
    s.y = 2 * HALF - s.y;
    s.vy = -s.vy;
  }
  if (s.y > H - HALF) {
    s.y = 2 * (H - HALF) - s.y;
    s.vy = -s.vy;
  }
}

function resolveCollision(a: Square, b: Square) {
  const dx = b.x - a.x;
  const dy = b.y - a.y;
  const adx = Math.abs(dx);
  const ady = Math.abs(dy);
  if (adx >= SIZE || ady >= SIZE) return;
  const overlapX = SIZE - adx;
  const overlapY = SIZE - ady;
  if (overlapX < overlapY) {
    const sign = dx >= 0 ? 1 : -1;
    a.x -= (sign * overlapX) / 2;
    b.x += (sign * overlapX) / 2;
    const rel = b.vx - a.vx;
    if (sign * rel < 0) {
      const tmp = a.vx;
      a.vx = b.vx;
      b.vx = tmp;
    }
  } else {
    const sign = dy >= 0 ? 1 : -1;
    a.y -= (sign * overlapY) / 2;
    b.y += (sign * overlapY) / 2;
    const rel = b.vy - a.vy;
    if (sign * rel < 0) {
      const tmp = a.vy;
      a.vy = b.vy;
      b.vy = tmp;
    }
  }
}

function simulate(nFrames: number): Array<Array<[number, number]>> {
  const sim: Square[] = INIT.map(s => ({...s}));
  const states: Array<Array<[number, number]>> = [];
  for (let f = 0; f < nFrames; f++) {
    for (const s of sim) {
      s.x += s.vx;
      s.y += s.vy;
      bounceWalls(s);
    }
    for (let i = 0; i < sim.length; i++) {
      for (let j = i + 1; j < sim.length; j++) {
        resolveCollision(sim[i], sim[j]);
      }
    }
    states.push(sim.map(s => [s.x, s.y] as [number, number]));
  }
  return states;
}

const STATES = simulate(FPS * DURATION + 2);

const scene = makeScene2D('scene', function* (view) {
  view.fill('#000000');

  const refs = INIT.map(() => createRef<Rect>());
  INIT.forEach((square, i) => {
    view.add(
      <Rect
        ref={refs[i]}
        fill={square.color}
        size={SIZE}
        position={[square.x - W / 2, square.y - H / 2]}
      />,
    );
  });

  const MAX_ITERS = 800;
  for (let iter = 0; iter < MAX_ITERS; iter++) {
    const t = useTime();
    const f = Math.round(t * FPS);
    if (f >= STATES.length) break;
    const frameState = STATES[f];
    for (let i = 0; i < refs.length; i++) {
      const [x, y] = frameState[i];
      refs[i]().position([x - W / 2, y - H / 2]);
    }
    yield null;
  }
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
