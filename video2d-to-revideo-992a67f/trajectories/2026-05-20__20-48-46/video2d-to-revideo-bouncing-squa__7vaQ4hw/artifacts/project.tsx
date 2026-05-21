import {makeProject} from '@revideo/core';
import {makeScene2D, Rect} from '@revideo/2d';
import {createRef, all} from '@revideo/core';

const W = 480;
const H = 360;
const SIZE = 50;
const HALF = SIZE / 2;
const FPS = 24;
const DURATION = 18.041667;

type Ball = { color: string; x: number; y: number; vx: number; vy: number };

function makeBalls(): Ball[] {
  return [
    { color: '#ff0000', x: 78.5,   y: 58.5,   vx: -1.3446, vy: -0.9890 }, // red
    { color: '#00ff00', x: 177.533,y: 60.461, vx: -2.4476, vy: 0.8256 },  // green
    { color: '#0000ff', x: 281.5,  y: 56.5,   vx: 2.0829,  vy: -2.8024 }, // blue
    { color: '#ffff00', x: 377.5,  y: 55.5,   vx: -2.1353, vy: -3.7755 }, // yellow
    { color: '#ff00ff', x: 81.5,   y: 164.0,  vx: 3.026,   vy: 5.39 },    // magenta
    { color: '#00ffff', x: 173.5,  y: 158.5,  vx: -5.9388, vy: -1.1237 }, // cyan
    { color: '#ff8000', x: 278.5,  y: 166.5,  vx: -1.0372, vy: 7.0447 },  // orange
    { color: '#8000ff', x: 373.542,y: 153.502,vx: -5.6761, vy: -5.6601 }, // purple
    { color: '#00ff80', x: 85.5,   y: 253.0,  vx: 6.064,   vy: -7.185 },  // spring
    { color: '#ff0080', x: 169.5,  y: 261.5,  vx: -9.487,  vy: 1.630 },   // pink
    { color: '#80ff00', x: 279.5,  y: 270.0,  vx: -0.11,   vy: 11.331 },  // chartreuse
    { color: '#0080ff', x: 388.0,  y: 251.5,  vx: 8.6296,  vy: -7.8693 }, // azure
  ];
}

const XMIN = 25, XMAX = 455;
const YMIN = 25, YMAX = 335;

function step(state: Ball[], dt: number) {
  for (const b of state) {
    b.x += b.vx * dt;
    b.y += b.vy * dt;
    if (b.x < XMIN) { b.x = 2 * XMIN - b.x; b.vx = -b.vx; }
    if (b.x > XMAX) { b.x = 2 * XMAX - b.x; b.vx = -b.vx; }
    if (b.y < YMIN) { b.y = 2 * YMIN - b.y; b.vy = -b.vy; }
    if (b.y > YMAX) { b.y = 2 * YMAX - b.y; b.vy = -b.vy; }
  }
  const N = state.length;
  for (let i = 0; i < N; i++) {
    for (let j = i+1; j < N; j++) {
      const a = state[i], c = state[j];
      const dx = c.x - a.x; const dy = c.y - a.y;
      if (Math.abs(dx) < SIZE && Math.abs(dy) < SIZE) {
        const overlapX = SIZE - Math.abs(dx);
        const overlapY = SIZE - Math.abs(dy);
        if (overlapX < overlapY) {
          const sign = dx > 0 ? 1 : -1;
          a.x -= sign * overlapX / 2;
          c.x += sign * overlapX / 2;
          const tmp = a.vx; a.vx = c.vx; c.vx = tmp;
        } else {
          const sign = dy > 0 ? 1 : -1;
          a.y -= sign * overlapY / 2;
          c.y += sign * overlapY / 2;
          const tmp = a.vy; a.vy = c.vy; c.vy = tmp;
        }
      }
    }
  }
}

function simulate(balls: Ball[], totalFrames: number): Array<Array<{x:number,y:number}>> {
  const history: Array<Array<{x:number,y:number}>> = [];
  const state = balls.map(b => ({ color: b.color, x: b.x, y: b.y, vx: b.vx, vy: b.vy }));
  const SUBSTEPS = 24;
  for (let f = 0; f < totalFrames; f++) {
    history.push(state.map(s => ({ x: s.x, y: s.y })));
    for (let s = 0; s < SUBSTEPS; s++) {
      step(state, 1 / SUBSTEPS);
    }
  }
  return history;
}

const scene = makeScene2D('scene', function* (view) {
  view.fill('#000000');
  const balls = makeBalls();
  const totalFrames = 433;
  const history = simulate(balls, totalFrames);
  const refs = balls.map(() => createRef<Rect>());
  for (let i = 0; i < balls.length; i++) {
    view.add(<Rect
      ref={refs[i]}
      x={history[0][i].x - W/2}
      y={history[0][i].y - H/2}
      width={SIZE}
      height={SIZE}
      fill={balls[i].color}
    />);
  }
  for (let f = 0; f < totalFrames - 1; f++) {
    yield* all(
      ...refs.map((r, i) => r().position.x(history[f+1][i].x - W/2, 1/FPS)),
      ...refs.map((r, i) => r().position.y(history[f+1][i].y - H/2, 1/FPS)),
    );
  }
});

export default makeProject({
  scenes: [scene],
  settings: {
    shared: { size: { x: W, y: H } },
    rendering: { fps: FPS },
  },
});
