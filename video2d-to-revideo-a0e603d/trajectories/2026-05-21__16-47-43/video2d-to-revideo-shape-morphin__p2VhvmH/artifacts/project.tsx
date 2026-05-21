import {makeProject, createSignal, waitFor} from '@revideo/core';
import {makeScene2D, Path} from '@revideo/2d';

// Morph through circle (M=0) -> square (M=1) -> star (M=2).
// Blend three polar shape functions linearly in radius:
//   circle: r = R
//   square: r = R / (|cos|^n + |sin|^n)^(1/n) with n=15 (rounded-corner square via superellipse)
//   star:   r = R + 15 * |sin(2*theta)|^1.5 (clover with lobes at corners, concave sides)
function generateShapePath(R: number, M: number): string {
  const n = 15;
  const N = 192;
  let d = '';
  for (let i = 0; i <= N; i++) {
    const theta = (i / N) * 2 * Math.PI;
    const cosA = Math.abs(Math.cos(theta));
    const sinA = Math.abs(Math.sin(theta));
    const rCircle = R;
    const rSquare =
      R / Math.pow(Math.pow(cosA, n) + Math.pow(sinA, n), 1 / n);
    const rStar = R + 15 * Math.pow(Math.abs(Math.sin(2 * theta)), 1.5);

    let r: number;
    if (M <= 1) {
      r = rCircle + (rSquare - rCircle) * M;
    } else {
      r = rSquare + (rStar - rSquare) * (M - 1);
    }

    const x = r * Math.cos(theta);
    const y = r * Math.sin(theta);
    d += (i === 0 ? 'M' : 'L') + x.toFixed(3) + ',' + y.toFixed(3) + ' ';
  }
  d += 'Z';
  return d;
}

// Smoothly interpolate M for a row based on (time, M) keyframes using cosine easing.
function interpolateKeyframes(keyframes: [number, number][], t: number): number {
  if (t <= keyframes[0][0]) return keyframes[0][1];
  const last = keyframes[keyframes.length - 1];
  if (t >= last[0]) return last[1];
  for (let i = 0; i < keyframes.length - 1; i++) {
    const [t0, m0] = keyframes[i];
    const [t1, m1] = keyframes[i + 1];
    if (t >= t0 && t < t1) {
      const p = (t - t0) / (t1 - t0);
      const eased = 0.5 * (1 - Math.cos(Math.PI * p));
      return m0 + (m1 - m0) * eased;
    }
  }
  return last[1];
}

// Keyframes use adjacent duplicates to create "hold" plateaus between transitions.
// Star (M=2) has a noticeably shorter hold than circle/square.
const rowKeyframes: [number, number][][] = [
  // Top row: full cycle through circle -> square -> star -> square -> circle -> square
  [
    [0, 0], [2, 0], [3.5, 1], [6.5, 1], [7.5, 2], [8.5, 2],
    [10, 1], [12, 1], [14, 0], [17, 0], [20, 1],
  ],
  // Middle row: slower; circle -> square -> star -> square in 20s
  [
    [0, 0], [3.5, 0], [7, 1], [12.5, 1], [14, 2], [18, 2], [19, 1], [20, 1],
  ],
  // Bottom row: held at circle (M=0)
  [[0, 0]],
];

const colors = [
  ['#FD3230', '#2DCA33', '#3397FC', '#FDCB00'],
  ['#FD33FB', '#00CCCA', '#FB8800', '#63FF65'],
  ['#C932FC', '#32FDCC', '#FA6664', '#98CBFE'],
];

const scene = makeScene2D('scene', function* (view) {
  view.fill('#171830');

  const colCenters = [-176, -59, 58, 174];
  const rowCenters = [-115, -1, 114];
  const R = 35.5;

  const time = createSignal(0);

  for (let r = 0; r < 3; r++) {
    for (let c = 0; c < 4; c++) {
      const kf = rowKeyframes[r];
      view.add(
        <Path
          x={colCenters[c]}
          y={rowCenters[r]}
          fill={colors[r][c]}
          data={() => {
            const t = time();
            const M = interpolateKeyframes(kf, t);
            return generateShapePath(R, M);
          }}
        />,
      );
    }
  }

  const fps = 24;
  const totalFrames = 481;
  for (let f = 0; f < totalFrames; f++) {
    time(f / fps);
    yield* waitFor(1 / fps);
  }
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
