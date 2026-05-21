import {makeProject} from '@revideo/core';
import {makeScene2D, Circle} from '@revideo/2d';
import {createSignal, linear} from '@revideo/core';

const scene = makeScene2D('scene', function* (view) {
  view.fill('#17182b');

  const fps = 24;
  const N = 361;
  const duration = (N - 1) / fps;

  const t = createSignal(0);

  type Ball = {color: string; R: number; theta0: number; omega: number};

  const D = Math.PI / 180;
  const ox = -2, oy = 0;

  // Common breathing
  const delta = 9.124;
  const wB = 1.0484 * D;
  const phaseB = 135.43 * D;

  // Time mapping (acceleration phase 2): tau = tSplit - a*dt - b*dt^2 - c*dt^3
  const tSplit = 269.96;
  const accelA = 4.9574;
  const accelB = 0.02370;
  const accelC = -0.0000135;
  function tau(tt: number): number {
    if (tt <= tSplit) return tt;
    const dt = tt - tSplit;
    return tSplit - accelA*dt - accelB*dt*dt - accelC*dt*dt*dt;
  }

  const balls: Ball[] = [
    {color: '#fd3131', R: 57.6971,  theta0: -0.5594 * D,   omega: 0.59427 * D},
    {color: '#3298fe', R: 68.2409,  theta0: 35.8581 * D,   omega: 1.19616 * D},
    {color: '#31cb31', R: 78.3646,  theta0: 72.0310 * D,   omega: 1.78919 * D},
    {color: '#fd32fd', R: 88.0999,  theta0: 108.0654 * D,  omega: 1.78979 * D},
    {color: '#00cccc', R: 103.3410, theta0: 144.0804 * D,  omega: 2.38704 * D},
    {color: '#fdcc00', R: 118.0447, theta0: -179.9066 * D, omega: 2.98380 * D},
    {color: '#c932fc', R: 128.3377, theta0: -143.9361 * D, omega: 3.57965 * D},
    {color: '#32fdcc', R: 138.4982, theta0: -107.9494 * D, omega: 4.17853 * D},
    {color: '#fd8764', R: 147.9901, theta0: -71.9788 * D,  omega: 5.37213 * D},
    {color: '#9898f8', R: 160.7262, theta0: -36.0015 * D,  omega: 6.56544 * D},
  ];

  view.add(<Circle size={78} fill={'#fda800'} x={ox} y={oy} />);

  for (const bb of balls) {
    view.add(
      <Circle
        size={40}
        fill={bb.color}
        x={() => {
          const tt = tau(t());
          const r = bb.R + delta * Math.cos(wB * tt + phaseB);
          return ox + r * Math.cos(bb.theta0 + bb.omega * tt);
        }}
        y={() => {
          const tt = tau(t());
          const r = bb.R + delta * Math.cos(wB * tt + phaseB);
          return oy + r * Math.sin(bb.theta0 + bb.omega * tt);
        }}
      />
    );
  }

  yield* t(N - 1, duration, linear);
});

export default makeProject({
  scenes: [scene],
  settings: {
    shared: {size: {x: 480, y: 360}},
    rendering: {fps: 24},
  },
});
