import {makeProject, createSignal, linear} from '@revideo/core';
import {makeScene2D, Path} from '@revideo/2d';

const W = 480;
const H = 360;
const R = 35;
const N = 144;

const COLS = [-175.5, -58.5, 58.5, 175.5];
const ROWS = [-115.5, -0.5, 114.5];

const COLORS = [
  ['#FD3230', '#32CA33', '#3297FE', '#FDCB00'],
  ['#FD33FB', '#00CCC9', '#FB8900', '#63FF65'],
  ['#C932FC', '#32FDCC', '#FC6664', '#98CBFE'],
];

const ROW_RATES = [1.0, 0.5, 0.0];

const N_MAX = 100;

function pattern(tau: number): number {
  let t = tau % 16;
  if (t < 0) t += 16;
  if (t < 2) return 0;
  if (t < 4) return (t - 2) / 2;
  if (t < 6) return 1;
  if (t < 7.5) return 1 + (t - 6) / 1.5;
  if (t < 8) return 2;
  if (t < 9.5) return 2 - (t - 8) / 1.5;
  if (t < 12) return 1;
  if (t < 14) return 1 - (t - 12) / 2;
  return 0;
}

function shapeR(theta: number, s: number): number {
  const sClamped = Math.max(0, Math.min(2, s));
  const sBase = Math.min(1, sClamped);
  const n = 2 * Math.exp(3.56 * sBase * sBase);
  const cosT = Math.abs(Math.cos(theta));
  const sinT = Math.abs(Math.sin(theta));
  const cn = Math.pow(cosT, n);
  const sn = Math.pow(sinT, n);
  const base = R / Math.pow(cn + sn, 1 / n);
  const bulgeAmp = 6.5 * Math.max(0, sClamped - 1);
  const bulge = bulgeAmp * Math.abs(Math.sin(4 * theta));
  return base + bulge;
}

function shapePath(s: number): string {
  let d = '';
  for (let i = 0; i < N; i++) {
    const theta = (i * 2 * Math.PI) / N;
    const r = shapeR(theta, s);
    const x = r * Math.cos(theta);
    const y = r * Math.sin(theta);
    d += (i === 0 ? 'M' : 'L') + x.toFixed(2) + ',' + y.toFixed(2) + ' ';
  }
  return d + 'Z';
}

const scene = makeScene2D('scene', function* (view) {
  view.fill('#17182B');

  const time = createSignal(0);

  for (let r = 0; r < 3; r++) {
    for (let c = 0; c < 4; c++) {
      const rate = ROW_RATES[r];
      const dataSignal = createSignal(() => {
        const s = pattern(time() * rate);
        return shapePath(s);
      });

      view.add(
        <Path
          x={COLS[c]}
          y={ROWS[r]}
          fill={COLORS[r][c]}
          data={dataSignal}
        />,
      );
    }
  }

  yield* time(20, 20, linear);
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
