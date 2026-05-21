import {makeProject, createSignal, waitFor} from '@revideo/core';
import {makeScene2D, Rect} from '@revideo/2d';

const WIDTH = 480;
const HEIGHT = 360;
const SIZE = 48;
const R = SIZE / 2;
const FPS = 24;
const TOTAL_FRAMES = 433;

type Sq = {
  color: string;
  x: number;
  y: number;
  vx: number;
  vy: number;
  sx: ReturnType<typeof createSignal<number>>;
  sy: ReturnType<typeof createSignal<number>>;
};

const scene = makeScene2D('scene', function* (view) {
  view.fill('#000000');

  // Initial positions (pixel coords, origin top-left) and velocities (px/frame).
  const initial: Array<Omit<Sq, 'sx' | 'sy'>> = [
    {color: '#ff0000', x: 78,   y: 58.5,  vx: -1.5, vy: -1},     // red
    {color: '#00ff00', x: 177,  y: 60,    vx: -2.5, vy:  1},     // green
    {color: '#0000ff', x: 281.5,y: 56.5,  vx:  2,   vy: -3},     // blue
    {color: '#ffff00', x: 377.5,y: 55.5,  vx: -2,   vy: -3},     // yellow
    {color: '#ff00ff', x: 81.5, y: 164,   vx:  3,   vy:  5},     // magenta
    {color: '#00ffff', x: 173.5,y: 158.5, vx: -6,   vy: -1},     // cyan
    {color: '#fb7f01', x: 278.5,y: 166.5, vx: -1,   vy:  7},     // orange
    {color: '#7b02ff', x: 373.5,y: 153.5, vx: -5.5, vy: -5.5},   // purple
    {color: '#00ff7f', x: 85.5, y: 253,   vx:  6,   vy: -7},     // springgreen
    {color: '#ff1493', x: 169.5,y: 261.5, vx: -9.5, vy:  1.5},   // hotpink
    {color: '#7ffd01', x: 279.5,y: 270,   vx:  0,   vy: 11},     // limegreen
    {color: '#1e90ff', x: 388,  y: 251.5, vx:  9,   vy: -8},     // dodgerblue
  ];

  const HW = WIDTH / 2;
  const HH = HEIGHT / 2;

  const squares: Sq[] = initial.map(s => {
    const sx = createSignal(s.x - HW);
    const sy = createSignal(s.y - HH);
    view.add(<Rect fill={s.color} width={SIZE} height={SIZE} x={sx} y={sy} />);
    return {...s, sx, sy};
  });

  // Render first frame (initial positions)
  yield* waitFor(1 / FPS);

  const minC = R;        // 24
  const maxX = WIDTH - R;  // 456
  const maxY = HEIGHT - R; // 336

  for (let f = 1; f < TOTAL_FRAMES; f++) {
    // Integrate motion
    for (const s of squares) {
      s.x += s.vx;
      s.y += s.vy;

      if (s.x < minC) { s.x = minC + (minC - s.x); s.vx = -s.vx; }
      if (s.x > maxX) { s.x = maxX - (s.x - maxX); s.vx = -s.vx; }
      if (s.y < minC) { s.y = minC + (minC - s.y); s.vy = -s.vy; }
      if (s.y > maxY) { s.y = maxY - (s.y - maxY); s.vy = -s.vy; }
    }

    // Resolve pair collisions: swap velocities along axis of overlap.
    for (let i = 0; i < squares.length; i++) {
      for (let j = i + 1; j < squares.length; j++) {
        const a = squares[i];
        const b = squares[j];
        const dx = b.x - a.x;
        const dy = b.y - a.y;
        const overlapX = SIZE - Math.abs(dx);
        const overlapY = SIZE - Math.abs(dy);
        if (overlapX > 0 && overlapY > 0) {
          // Approaching only
          const rvx = b.vx - a.vx;
          const rvy = b.vy - a.vy;
          if (overlapX < overlapY) {
            if (dx * rvx < 0) {
              const t = a.vx; a.vx = b.vx; b.vx = t;
              const push = overlapX / 2;
              if (dx > 0) { a.x -= push; b.x += push; }
              else        { a.x += push; b.x -= push; }
            }
          } else {
            if (dy * rvy < 0) {
              const t = a.vy; a.vy = b.vy; b.vy = t;
              const push = overlapY / 2;
              if (dy > 0) { a.y -= push; b.y += push; }
              else        { a.y += push; b.y -= push; }
            }
          }
        }
      }
    }

    for (const s of squares) {
      s.sx(s.x - HW);
      s.sy(s.y - HH);
    }

    yield* waitFor(1 / FPS);
  }
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
