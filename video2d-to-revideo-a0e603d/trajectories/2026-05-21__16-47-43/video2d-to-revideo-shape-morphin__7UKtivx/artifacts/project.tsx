import {makeProject, createSignal, tween} from '@revideo/core';
import {makeScene2D, Rect} from '@revideo/2d';

const BG = '#17182b';
const COLORS = [
  ['#fd3230', '#31ca32', '#3296fd', '#fdca00'],
  ['#fd33fa', '#00ccc9', '#fb8800', '#63ff65'],
  ['#c931fc', '#32fdcc', '#fb6664', '#98cafd'],
];

const FIRST_X = -180;
const FIRST_Y = -115;
const COL_STEP = 117;
const ROW_STEP = 116;
const SHAPE = 70;
const DURATION = 20;
const CS_DEFORM = 2.0;
const CYCLE = 16;
const ROW_SCALES = [1, 0.5, 0];

function shapeP(t: number): number {
  if (t <= 0) return 0;
  const u = t - Math.floor(t / CYCLE) * CYCLE;
  if (u < 2) return 0;
  if (u < 4) return (u - 2) / 2;
  if (u < 6) return 1;
  if (u < 8) return 1 + (u - 6) / 2;
  if (u < 10) return 2 - (u - 8) / 2;
  if (u < 13) return 1;
  if (u < 14) return 1 - (u - 13);
  return 0;
}

const scene = makeScene2D('scene', function* (view) {
  view.fill(BG);

  const time = createSignal(0);

  for (let r = 0; r < 3; r++) {
    for (let c = 0; c < 4; c++) {
      const p = () => shapeP(time() * ROW_SCALES[r]);
      const radius = () => {
        const pv = p();
        if (pv <= 1) return (1 - pv) * (SHAPE / 2);
        return (pv - 1) * (SHAPE / 2);
      };
      const sharpness = () => {
        const pv = p();
        if (pv <= 1) return 0.55;
        return 0.55 + (pv - 1) * (CS_DEFORM - 0.55);
      };
      view.add(
        <Rect
          x={FIRST_X + c * COL_STEP}
          y={FIRST_Y + r * ROW_STEP}
          width={SHAPE}
          height={SHAPE}
          fill={COLORS[r][c]}
          radius={radius}
          smoothCorners
          cornerSharpness={sharpness}
        />,
      );
    }
  }

  yield* tween(DURATION, value => {
    time(value * DURATION);
  });
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
