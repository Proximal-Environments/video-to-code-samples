import {makeProject, createSignal} from '@revideo/core';
import {makeScene2D, Circle} from '@revideo/2d';

const DURATION = 15;
const W = 480;
const H = 360;

interface Orb {
  color: string;
  size: number;
  // starting position (at t=0)
  sx: number;
  sy: number;
  // amplitudes and angular speeds
  ax: number;
  ay: number;
  wx: number;
  wy: number;
  // phases (motion direction at t=0)
  px: number;
  py: number;
}

// position(t) = s + a * (sin(w*t + p) - sin(p))
// so position(0) = s exactly, and motion direction varies by phase.
function posX(o: Orb, t: number): number {
  return o.sx + o.ax * (Math.sin(o.wx * t + o.px) - Math.sin(o.px));
}
function posY(o: Orb, t: number): number {
  return o.sy + o.ay * (Math.sin(o.wy * t + o.py) - Math.sin(o.py));
}

// Big center circle - small wandering motion
const center: Orb = {
  color: '#F39C12',
  size: 70,
  sx: 5, sy: -5,
  ax: 30, ay: 22,
  wx: 0.5, wy: 0.65,
  px: 0.3, py: 1.1,
};

// 10 small circles arranged in a rough ring (matching reference frame 0)
const orbs: Orb[] = [
  // mint top
  {color: '#2ED9B5', size: 32, sx: -20, sy: -85, ax: 60, ay: 55, wx: 0.55, wy: 0.75, px: 0.6, py: 1.8},
  // coral top-right
  {color: '#FF8E72', size: 30, sx: 70, sy: -85, ax: 70, ay: 65, wx: 0.65, wy: 0.5, px: 2.1, py: 0.4},
  // lavender right
  {color: '#9B9CF0', size: 32, sx: 130, sy: -20, ax: 80, ay: 70, wx: 0.5, wy: 0.6, px: 3.2, py: 1.6},
  // magenta-purple upper-left
  {color: '#C530E0', size: 32, sx: -85, sy: -40, ax: 70, ay: 60, wx: 0.7, wy: 0.55, px: 1.3, py: 2.4},
  // yellow left
  {color: '#F1C40F', size: 30, sx: -100, sy: 15, ax: 80, ay: 55, wx: 0.6, wy: 0.7, px: 4.0, py: 0.9},
  // cyan/teal left-bottom
  {color: '#1ABC9C', size: 32, sx: -120, sy: 60, ax: 70, ay: 60, wx: 0.55, wy: 0.65, px: 2.5, py: 3.0},
  // magenta-pink bottom
  {color: '#E91E63', size: 30, sx: -25, sy: 95, ax: 60, ay: 55, wx: 0.75, wy: 0.5, px: 1.7, py: 1.9},
  // green bottom-center
  {color: '#27AE60', size: 28, sx: 25, sy: 95, ax: 55, ay: 60, wx: 0.6, wy: 0.8, px: 3.4, py: 0.6},
  // red right inner
  {color: '#E74C3C', size: 28, sx: 60, sy: 15, ax: 45, ay: 60, wx: 0.9, wy: 0.6, px: 2.0, py: 2.5},
  // blue right inner
  {color: '#3498DB', size: 28, sx: 60, sy: 55, ax: 50, ay: 55, wx: 0.7, wy: 0.65, px: 3.6, py: 1.3},
];

const scene = makeScene2D('scene', function* (view) {
  view.fill('#15182E');

  const t = createSignal(0);

  view.add(
    <Circle
      fill={center.color}
      size={center.size}
      x={() => posX(center, t())}
      y={() => posY(center, t())}
    />,
  );

  for (const o of orbs) {
    const orb = o;
    view.add(
      <Circle
        fill={orb.color}
        size={orb.size}
        x={() => posX(orb, t())}
        y={() => posY(orb, t())}
      />,
    );
  }

  yield* t(DURATION, DURATION);
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
