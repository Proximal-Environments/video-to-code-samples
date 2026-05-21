import {makeProject} from '@revideo/core';
import {Circle, makeScene2D} from '@revideo/2d';
import {createRef, range} from '@revideo/core';

const W = 480;
const H = 360;
const FPS = 24;
const DUR = 15;
const N = 10;
const COLORS = [
  '#ffaa00',
  '#ff3333', '#3399ff', '#33cc33', '#ff33ff', '#00cccc',
  '#ffcc00', '#cc33ff', '#33ffcc', '#ff8866', '#9999ff',
];
const RADII = [50, 60, 70, 80, 95, 110, 120, 130, 140, 155];
const SPEEDS = [0.25, 0.5, 0.75, 0.75, 1.0, 1.25, 1.5, 1.75, 2.25, 2.75];
const SAT_SIZES = [20, 20, 22, 22, 24, 24, 22, 22, 20, 20];
const CENTER_R = 40;

function clamp(v: number, lo: number, hi: number) {
  return Math.max(lo, Math.min(hi, v));
}

const scene = makeScene2D('scene', function* (view) {
  view.fill('#1a1a2e');

  const centerRef = createRef<Circle>();
  view.add(
    <Circle
      ref={centerRef}
      width={CENTER_R * 2}
      height={CENTER_R * 2}
      fill={COLORS[0]}
      x={0}
      y={0}
    />,
  );

  const satRefs = range(N).map(() => createRef<Circle>());
  for (let i = 0; i < N; i++) {
    view.add(
      <Circle
        ref={satRefs[i]}
        width={SAT_SIZES[i] * 2}
        height={SAT_SIZES[i] * 2}
        fill={COLORS[i + 1]}
        x={0}
        y={0}
      />,
    );
  }

  const dt = 1 / FPS;
  const M = 30;

  for (let frame = 0; frame < DUR * FPS; frame++) {
    const t = frame * dt;
    const progress = t / DUR;

    let b12: number, b23: number;
    if (progress < 0.25) {
      b12 = 0; b23 = 0;
    } else if (progress < 0.5) {
      b12 = (progress - 0.25) / 0.25; b23 = 0;
    } else if (progress < 0.75) {
      b12 = 1; b23 = 0;
    } else {
      b12 = 1; b23 = (progress - 0.75) / 0.25;
    }

    for (let idx = 0; idx < N; idx++) {
      const r1 = RADII[idx];
      const r2 = RADII[idx] + 20;
      const r3 = RADII[idx] - 10;
      const orbitR = r1 * (1 - b12) + r2 * b12 * (1 - b23) + Math.max(20, r3) * b23;

      const dir1 = 1;
      const dir2 = 1;
      const dir3 = -1;
      const direction = dir1 * (1 - b12) + dir2 * b12 * (1 - b23) + dir3 * b23;
      const angle = direction * SPEEDS[idx] * t + (idx * 2 * Math.PI) / N;

      const sx = clamp(orbitR * Math.cos(angle), -W / 2 + M, W / 2 - M);
      const sy = clamp(orbitR * Math.sin(angle), -H / 2 + M, H / 2 - M);

      satRefs[idx]().position.x(sx);
      satRefs[idx]().position.y(sy);
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
