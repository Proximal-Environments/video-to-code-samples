import {makeProject, createSignal, linear} from '@revideo/core';
import {makeScene2D, Circle} from '@revideo/2d';

const scene = makeScene2D('scene', function* (view) {
  view.fill('#17182B');

  const cx = -2;
  const cy = 0;

  const t = createSignal(0);

  view.add(<Circle x={cx} y={cy} size={76} fill="#FDA900" />);

  const sats = [
    {color: '#F23037', r: 51,  w: 0.010},
    {color: '#2C87EA', r: 63,  w: 0.020},
    {color: '#2CC143', r: 72,  w: 0.031},
    {color: '#EC31EC', r: 80,  w: 0.032},
    {color: '#03C0BF', r: 94,  w: 0.042},
    {color: '#EEC005', r: 110, w: 0.052},
    {color: '#BC30EB', r: 120, w: 0.062},
    {color: '#32F0C3', r: 130, w: 0.073},
    {color: '#EC8060', r: 141, w: 0.093},
    {color: '#9190EF', r: 156, w: 0.113},
  ];

  const fps = 24;

  sats.forEach((s, i) => {
    const phase = (i * 2 * Math.PI) / 10;
    const omega = s.w * fps;
    view.add(
      <Circle
        x={() => cx + s.r * Math.cos(phase + omega * t())}
        y={() => cy + s.r * Math.sin(phase + omega * t())}
        size={40}
        fill={s.color}
      />,
    );
  });

  yield* t(15, 15, linear);
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
