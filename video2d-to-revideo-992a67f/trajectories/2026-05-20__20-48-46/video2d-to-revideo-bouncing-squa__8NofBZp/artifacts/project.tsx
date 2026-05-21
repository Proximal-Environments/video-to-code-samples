import {makeProject} from '@revideo/core';
import {makeScene2D, Rect} from '@revideo/2d';
import {createRef, waitFor} from '@revideo/core';

const W = 480;
const H = 360;
const SIZE = 50;
const FPS = 24;
const NFRAMES = 433;

type Sq = { x: number; y: number; vx: number; vy: number; color: string; };

const initial: Sq[] = [
  {x: 77.5,  y: 58.5,  vx: -1.0,  vy: -1.0,  color: '#ff0000'},
  {x: 278.5, y: 166.5, vx: -1.21, vy:  7.42, color: '#ff8000'},
  {x: 377.5, y: 55.5,  vx: -2.0,  vy: -4.0,  color: '#ffff00'},
  {x: 279.5, y: 270.0, vx:  0.0,  vy: 11.0,  color: '#80ff00'},
  {x: 177.5, y: 59.5,  vx: -3.0,  vy:  1.0,  color: '#00ff00'},
  {x: 85.5,  y: 253.5, vx:  6.0,  vy: -7.0,  color: '#00ff80'},
  {x: 173.5, y: 158.5, vx: -6.03, vy: -1.04, color: '#00ffff'},
  {x: 387.5, y: 251.5, vx:  8.97, vy: -7.97, color: '#0080ff'},
  {x: 281.5, y: 57.5,  vx:  2.09, vy: -3.0,  color: '#0000ff'},
  {x: 373.5, y: 153.5, vx: -5.5,  vy: -5.5,  color: '#8000ff'},
  {x: 81.5,  y: 163.5, vx:  3.09, vy:  5.14, color: '#ff00ff'},
  {x: 169.5, y: 261.5, vx: -9.36, vy:  1.5,  color: '#ff0080'},
];

const MIN_X = SIZE/2;
const MAX_X = W - SIZE/2;
const MIN_Y = SIZE/2;
const MAX_Y = H - SIZE/2;

function simulate(): {x:number, y:number}[][] {
  const s: Sq[] = initial.map(o => ({...o}));
  const N = s.length;
  const frames: {x:number, y:number}[][] = [];
  frames.push(s.map(o => ({x: o.x, y: o.y})));

  const SUBSTEPS = 8;
  const DT = 1.0 / SUBSTEPS;
  for (let f = 1; f < NFRAMES; f++) {
    for (let sub = 0; sub < SUBSTEPS; sub++) {
      for (const o of s) {
        o.x += o.vx * DT;
        o.y += o.vy * DT;
      }
      for (const o of s) {
        if (o.x < MIN_X) { o.x = 2*MIN_X - o.x; o.vx = -o.vx; }
        if (o.x > MAX_X) { o.x = 2*MAX_X - o.x; o.vx = -o.vx; }
        if (o.y < MIN_Y) { o.y = 2*MIN_Y - o.y; o.vy = -o.vy; }
        if (o.y > MAX_Y) { o.y = 2*MAX_Y - o.y; o.vy = -o.vy; }
      }
      for (let i = 0; i < N; i++) {
        for (let j = i+1; j < N; j++) {
          const a = s[i], b = s[j];
          const dx = b.x - a.x;
          const dy = b.y - a.y;
          const overlapX = SIZE - Math.abs(dx);
          const overlapY = SIZE - Math.abs(dy);
          if (overlapX > 0 && overlapY > 0) {
            // Resolve along axis of smaller overlap
            if (overlapX < overlapY) {
              const sign = dx > 0 ? 1 : -1;
              const push = overlapX / 2;
              a.x -= sign * push;
              b.x += sign * push;
              // Only swap if moving toward each other along this axis
              const relV = b.vx - a.vx;
              if (relV * sign < 0) {
                const t = a.vx; a.vx = b.vx; b.vx = t;
              }
            } else {
              const sign = dy > 0 ? 1 : -1;
              const push = overlapY / 2;
              a.y -= sign * push;
              b.y += sign * push;
              const relV = b.vy - a.vy;
              if (relV * sign < 0) {
                const t = a.vy; a.vy = b.vy; b.vy = t;
              }
            }
          }
        }
      }
    }
    frames.push(s.map(o => ({x: o.x, y: o.y})));
  }
  return frames;
}

const FRAMES = simulate();

const scene = makeScene2D('scene', function* (view) {
  view.fill('#000000');
  const refs = initial.map(() => createRef<Rect>());
  for (let i = 0; i < initial.length; i++) {
    view.add(
      <Rect
        ref={refs[i]}
        size={[SIZE, SIZE]}
        fill={initial[i].color}
        position={[FRAMES[0][i].x - W/2, FRAMES[0][i].y - H/2]}
      />
    );
  }
  // Sequentially set positions then wait. Empirically out frame N shows state after iteration N (one shift).
  // So use FRAMES[f] where total output = NFRAMES frames mapped from FRAMES[1..NFRAMES]
  // Prime the scene with one frame of initial state before time loop
  yield;
  // Output frame N shows state set in iteration N+1 due to Revideo's wait semantics.
  // We need out_f0 = FRAMES[0]. So pre-set state then loop sets FRAMES[f+1] for f starting at 0.
  // The first iteration's set defines out_f0 (it's set before first waitFor renders).
  // Actually empirically out_f0 = FRAMES[1] (state set in iteration 1).
  // So loop iteration f sets the state to be shown at out_f(f-1).
  // To show FRAMES_target[k] at out_f(k), set in iteration k+1 to FRAMES_target[k].
  // Equivalently, in iteration f, set positions to FRAMES_target[f-1].
  for (let f = 0; f < NFRAMES; f++) {
    const fi = f; // FRAMES index = output frame number
    for (let i = 0; i < initial.length; i++) {
      refs[i]().position([FRAMES[fi][i].x - W/2, FRAMES[fi][i].y - H/2]);
    }
    yield* waitFor(1/FPS);
  }
});

export default makeProject({
  scenes: [scene],
  settings: {
    shared: { size: {x: W, y: H} },
    rendering: { fps: FPS },
  },
});
