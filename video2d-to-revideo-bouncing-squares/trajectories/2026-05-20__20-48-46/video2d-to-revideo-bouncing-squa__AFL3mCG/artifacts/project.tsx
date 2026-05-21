import {makeProject} from '@revideo/core';
import {makeScene2D, Rect} from '@revideo/2d';
import {createRef, waitFor} from '@revideo/core';

const W = 480;
const H = 360;
const BOX = 50;
const FPS = 24;
const DURATION = 18.041667;

const BOXES: [string, string, number, number, number, number][] = [
  ['red',       '#ff0000',  80,  60, -1.346, -0.999],
  ['green',     '#00ff00', 180,  60, -2.440,  0.828],
  ['blue',      '#0000ff', 280,  60,  2.092, -2.802],
  ['yellow',    '#ffff00', 380,  60, -2.135, -3.742],
  ['magenta',   '#ff00ff',  80, 160,  2.665,  4.518],
  ['cyan',      '#00ffff', 180, 160, -5.936, -1.126],
  ['orange',    '#ff7f00', 280, 160, -1.051,  7.061],
  ['purple',    '#7f00ff', 380, 160, -5.674, -5.661],
  ['lime',      '#00ff7f',  80, 260,  6.000, -6.750],
  ['pink',      '#ff007f', 180, 260, -9.480,  1.480],
  ['limegreen', '#7fff00', 280, 260,  0.000, 10.696],
  ['lightblue', '#007fff', 380, 260,  8.631, -7.871],
];

const scene = makeScene2D('scene', function* (view) {
  view.fill('#000000');

  const refs = BOXES.map(() => createRef<Rect>());
  for (let i = 0; i < BOXES.length; i++) {
    const [, color, x, y] = BOXES[i];
    view.add(
      <Rect
        ref={refs[i]}
        size={[BOX, BOX]}
        fill={color}
        position={[x - W / 2, y - H / 2]}
      />
    );
  }

  const state = BOXES.map(b => ({x: b[2], y: b[3], vx: b[4], vy: b[5]}));
  const half = BOX / 2;
  const totalFrames = Math.round(DURATION * FPS);

  for (let f = 0; f < totalFrames; f++) {
    const SUB = 10;
    const sdt = 1 / SUB;
    for (let s = 0; s < SUB; s++) {
      for (const b of state) {
        b.x += b.vx * sdt;
        b.y += b.vy * sdt;
      }
      for (const b of state) {
        if (b.x < half) { b.x = half; b.vx = Math.abs(b.vx); }
        if (b.x > W - half) { b.x = W - half; b.vx = -Math.abs(b.vx); }
        if (b.y < half) { b.y = half; b.vy = Math.abs(b.vy); }
        if (b.y > H - half) { b.y = H - half; b.vy = -Math.abs(b.vy); }
      }
      for (let i = 0; i < state.length; i++) {
        for (let j = i + 1; j < state.length; j++) {
          const a = state[i], c = state[j];
          const dx = c.x - a.x;
          const dy = c.y - a.y;
          const ox = BOX - Math.abs(dx);
          const oy = BOX - Math.abs(dy);
          if (ox > 0 && oy > 0) {
            if (ox < oy) {
              const sgn = dx > 0 ? 1 : -1;
              a.x -= sgn * ox / 2;
              c.x += sgn * ox / 2;
              const rel = c.vx - a.vx;
              if (rel * sgn < 0) {
                const tmp = a.vx; a.vx = c.vx; c.vx = tmp;
              }
            } else {
              const sgn = dy > 0 ? 1 : -1;
              a.y -= sgn * oy / 2;
              c.y += sgn * oy / 2;
              const rel = c.vy - a.vy;
              if (rel * sgn < 0) {
                const tmp = a.vy; a.vy = c.vy; c.vy = tmp;
              }
            }
          }
        }
      }
    }
    for (let i = 0; i < state.length; i++) {
      refs[i]().position([state[i].x - W / 2, state[i].y - H / 2]);
    }
    yield* waitFor(1 / FPS);
  }
});

export default makeProject({
  scenes: [scene],
  settings: {
    shared: {size: {x: W, y: H}},
    rendering: {fps: FPS},
  },
});
