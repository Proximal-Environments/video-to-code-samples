import {makeProject} from '@revideo/core';
import {makeScene2D, Circle} from '@revideo/2d';
import {createSignal, linear} from '@revideo/core';

const scene = makeScene2D('scene', function* (view) {
  view.fill('#17182b');

  const CX = -1.95;
  const CY = -0.72;

  view.add(
    <Circle
      x={CX}
      y={CY}
      width={77}
      height={77}
      fill={'#fea800'}
    />
  );

  const t = createSignal(0);

  const tau = (tt: number) => {
    const tc = 11.25;
    if (tt < tc) return tt;
    const dt = tt - tc;
    return 11.2581 - 5.0217 * dt - 0.5246 * dt * dt;
  };

  const planets = [
    {color: '#3396fe', r: 69.73, T: 12.4588, phi0: 0.6025, size: 38},
    {color: '#31cb33', r: 79.75, T: 8.3784, phi0: 1.2540, size: 42},
    {color: '#fe33f9', r: 89.51, T: 8.3822, phi0: 1.8863, size: 42},
    {color: '#00cbcd', r: 104.61, T: 6.2850, phi0: 2.5164, size: 46},
    {color: '#fbcb00', r: 119.31, T: 5.0290, phi0: -3.1375, size: 45},
    {color: '#c832fc', r: 129.86, T: 4.1903, phi0: -2.5101, size: 42},
    {color: '#32fdcc', r: 139.81, T: 3.5890, phi0: -1.8869, size: 42},
    {color: '#fd8762', r: 149.26, T: 2.7916, phi0: -1.2594, size: 38},
    {color: '#9599fa', r: 161.87, T: 2.2846, phi0: -0.6295, size: 39},
  ];

  for (const p of planets) {
    const w = 2 * Math.PI / p.T;
    const phi0 = p.phi0;
    const r = p.r;
    view.add(
      <Circle
        x={() => CX + r * Math.cos(phi0 + w * tau(t()))}
        y={() => CY + r * Math.sin(phi0 + w * tau(t()))}
        width={p.size}
        height={p.size}
        fill={p.color}
      />
    );
  }

  yield* t(15.041667, 15.041667, linear);
});

export default makeProject({
  scenes: [scene],
  settings: {
    shared: {
      size: {x: 480, y: 360},
    },
    rendering: {
      fps: 24,
    },
  },
});
