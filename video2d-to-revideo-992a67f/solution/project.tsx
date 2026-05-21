import {makeProject} from '@revideo/core';
import {Rect, makeScene2D} from '@revideo/2d';
import {createRef, range} from '@revideo/core';

const W = 480;
const H = 360;
const FPS = 24;
const DUR = 18;
const SQ = 50;
const SPEED_MIN = 40;
const SPEED_MAX = 280;

const COLORS = [
  '#ff0000', '#00ff00', '#0000ff', '#ffff00',
  '#ff00ff', '#00ffff', '#ff8000', '#8000ff',
  '#00ff80', '#ff0080', '#80ff00', '#0080ff',
];

// Seeded PRNG for initial directions and speeds
function mulberry32(seed: number) {
  return () => {
    seed |= 0; seed = seed + 0x6D2B79F5 | 0;
    let t = Math.imul(seed ^ seed >>> 15, 1 | seed);
    t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t;
    return ((t ^ t >>> 14) >>> 0) / 4294967296;
  };
}

const rng = mulberry32(42);

const INIT_POS: [number, number][] = [];
const INIT_VEL: [number, number][] = [];
const SPEEDS: number[] = [];
for (let r = 0; r < 3; r++) {
  for (let c = 0; c < 4; c++) {
    const idx = r * 4 + c;
    INIT_POS.push([80 + c * 100, 60 + r * 100]);
    const speed = SPEED_MIN + (idx / 11) * (SPEED_MAX - SPEED_MIN);
    SPEEDS.push(speed);
    const angle = rng() * 2 * Math.PI;
    INIT_VEL.push([Math.cos(angle) * speed, Math.sin(angle) * speed]);
  }
}

function wallBounds(t: number) {
  const half = SQ / 2;
  let shrink = 0;
  if (t < 6) shrink = 0;
  else if (t < 12) shrink = ((t - 6) / 6) * 80;
  else shrink = 80 - ((t - 12) / 6) * 40;
  return {
    left: shrink + half,
    right: W - shrink - half,
    top: shrink + half,
    bottom: H - shrink - half,
  };
}

function aabbOverlap(
  ax: number, ay: number, bx: number, by: number, size: number,
): boolean {
  return Math.abs(ax - bx) < size && Math.abs(ay - by) < size;
}

const scene = makeScene2D('scene', function* (view) {
  view.fill('#000000');

  const refs = range(12).map(() => createRef<Rect>());

  for (let i = 0; i < 12; i++) {
    view.add(
      <Rect
        ref={refs[i]}
        width={SQ}
        height={SQ}
        fill={COLORS[i]}
        x={INIT_POS[i][0] - W / 2}
        y={INIT_POS[i][1] - H / 2}
      />,
    );
  }

  const pos = INIT_POS.map(([x, y]) => ({x, y}));
  const vel = INIT_VEL.map(([vx, vy]) => ({x: vx, y: vy}));
  const dt = 1 / FPS;

  for (let frame = 0; frame < DUR * FPS; frame++) {
    const t = frame * dt;
    const b = wallBounds(t);

    // Move
    for (let i = 0; i < 12; i++) {
      pos[i].x += vel[i].x * dt;
      pos[i].y += vel[i].y * dt;
    }

    // Wall collisions
    for (let i = 0; i < 12; i++) {
      if (pos[i].x <= b.left) { pos[i].x = b.left; vel[i].x = Math.abs(vel[i].x); }
      else if (pos[i].x >= b.right) { pos[i].x = b.right; vel[i].x = -Math.abs(vel[i].x); }
      if (pos[i].y <= b.top) { pos[i].y = b.top; vel[i].y = Math.abs(vel[i].y); }
      else if (pos[i].y >= b.bottom) { pos[i].y = b.bottom; vel[i].y = -Math.abs(vel[i].y); }
    }

    // Square-square collisions (elastic, equal mass → swap velocities along collision axis)
    for (let i = 0; i < 12; i++) {
      for (let j = i + 1; j < 12; j++) {
        if (!aabbOverlap(pos[i].x, pos[i].y, pos[j].x, pos[j].y, SQ)) continue;

        const dx = pos[j].x - pos[i].x;
        const dy = pos[j].y - pos[i].y;
        const dist = Math.sqrt(dx * dx + dy * dy);
        if (dist === 0) continue;

        const nx = dx / dist;
        const ny = dy / dist;

        // Relative velocity along collision normal
        const dvx = vel[i].x - vel[j].x;
        const dvy = vel[i].y - vel[j].y;
        const dvn = dvx * nx + dvy * ny;

        // Only resolve if approaching
        if (dvn <= 0) continue;

        // Equal mass elastic: swap normal components
        vel[i].x -= dvn * nx;
        vel[i].y -= dvn * ny;
        vel[j].x += dvn * nx;
        vel[j].y += dvn * ny;

        // Preserve each square's own speed
        const si = Math.sqrt(vel[i].x * vel[i].x + vel[i].y * vel[i].y);
        const sj = Math.sqrt(vel[j].x * vel[j].x + vel[j].y * vel[j].y);
        if (si > 0) { vel[i].x = vel[i].x / si * SPEEDS[i]; vel[i].y = vel[i].y / si * SPEEDS[i]; }
        if (sj > 0) { vel[j].x = vel[j].x / sj * SPEEDS[j]; vel[j].y = vel[j].y / sj * SPEEDS[j]; }

        // Separate so they don't overlap
        const overlap = SQ - Math.abs(dx) > SQ - Math.abs(dy)
          ? SQ - Math.abs(dy) : SQ - Math.abs(dx);
        const sep = (overlap / 2) + 0.5;
        pos[i].x -= nx * sep;
        pos[i].y -= ny * sep;
        pos[j].x += nx * sep;
        pos[j].y += ny * sep;
      }
    }

    for (let i = 0; i < 12; i++) {
      refs[i]().position.x(pos[i].x - W / 2);
      refs[i]().position.y(pos[i].y - H / 2);
    }

    yield;
  }
});

export default makeProject({
  scenes: [scene],
  settings: {
    shared: {
      size: {x: W, y: H},
      background: '#000000',
      range: [0, DUR],
    },
    rendering: {
      fps: FPS,
    },
  },
});
