import {makeProject, waitFor, all, createRef, tween} from '@revideo/core';
import {makeScene2D, Rect} from '@revideo/2d';

const COLORS = [
  ['#fd3230', '#31cb33', '#3297fe', '#fdcb00'],
  ['#fd33fb', '#00ccc9', '#fb8900', '#63ff65'],
  ['#c932fc', '#32fdcc', '#fa6764', '#98cbfe'],
];

const BG = '#17182b';
const MAX_R = 35;
const W = 70;

const scene = makeScene2D('scene', function* (view) {
  view.fill(BG);

  const refs: any[][] = [[], [], []];
  const row0_topleft = [-210, -94, 23, 139];
  const row0_topy = -150;
  const row12_xs = [-176, -59, 58, 174];

  for (let c = 0; c < 4; c++) {
    const ref = createRef<Rect>();
    refs[0].push(ref);
    view.add(
      <Rect
        ref={ref}
        x={row0_topleft[c]}
        y={row0_topy}
        offset={[-1, -1]}
        width={W}
        height={W}
        fill={COLORS[0][c]}
        radius={MAX_R}
      />
    );
  }
  for (let c = 0; c < 4; c++) {
    const ref = createRef<Rect>();
    refs[1].push(ref);
    view.add(
      <Rect
        ref={ref}
        x={row12_xs[c]}
        y={0}
        width={W}
        height={W}
        fill={COLORS[1][c]}
        radius={MAX_R}
      />
    );
  }
  for (let c = 0; c < 4; c++) {
    const ref = createRef<Rect>();
    refs[2].push(ref);
    view.add(
      <Rect
        ref={ref}
        x={row12_xs[c]}
        y={114}
        width={W}
        height={W}
        fill={COLORS[2][c]}
        radius={MAX_R}
      />
    );
  }

  const tweenRadius = function* (row: any[], dur: number, from: number, to: number) {
    yield* tween(dur, (t) => {
      const r = from + (to - from) * t;
      for (let i = 0; i < 4; i++) row[i]().radius(r);
    });
  };

  // Tween that animates size AND radius linearly (radius proportional to (size-W)*ratio)
  const tweenSizeWithRadius = function* (row: any[], dur: number, sFrom: number, sTo: number, rFrom: number, rTo: number) {
    yield* tween(dur, (t) => {
      const s = sFrom + (sTo - sFrom) * t;
      const r = rFrom + (rTo - rFrom) * t;
      for (let i = 0; i < 4; i++) {
        row[i]().width(s);
        row[i]().height(s);
        row[i]().radius(r);
      }
    });
  };

  const tweenSize = function* (row: any[], dur: number, from: number, to: number) {
    yield* tween(dur, (t) => {
      const s = from + (to - from) * t;
      for (let i = 0; i < 4; i++) {
        row[i]().width(s);
        row[i]().height(s);
      }
    });
  };

  // Phase 1: idle
  yield* waitFor(52/24);
  // Phase 2: row 0 radius 35→0
  yield* tweenRadius(refs[0], 42/24, 35, 0);
  yield* waitFor(4/24);
  // Phase 4: row 1 radius starts (99-189 over 90 frames)
  yield* tweenRadius(refs[1], 56/24, 35, 35*(1-56/90));
  // Phase 5: row 1 radius continues + row 0 size up (155-185, 30f)
  yield* all(
    tweenRadius(refs[1], 30/24, 35*(1-56/90), 35*(1-86/90)),
    tweenSize(refs[0], 30/24, 70, 76),
  );
  // Phase 6: row 1 radius finishes (4f)
  yield* tweenRadius(refs[1], 4/24, 35*(1-86/90), 0);
  // Phase 7: row 0 plateau (15f)
  yield* waitFor(15/24);
  // Phase 8: row 0 size shrinks (30f)
  yield* tweenSize(refs[0], 30/24, 76, 70);
  // Phase 9: idle (58f)
  yield* waitFor(58/24);
  // Phase 10: row 0 radius 0→partway (2f)
  yield* tweenRadius(refs[0], 2/24, 0, 35*(2/41));
  // Phase 11: row 0 radius continues + row 1 size + radius up (39f)
  // At 39 of 90 frames: size_progress=39/90, expected size = 70 + 15*(39/90) = 76.5
  // Radius growth: 0 to 22*(39/90) = 9.5
  yield* all(
    tweenRadius(refs[0], 39/24, 35*(2/41), 35),
    tweenSizeWithRadius(refs[1], 39/24, 70, 70 + 15 * (39/90), 0, 22 * (39/90)),
  );
  // Phase 12: row 1 size + radius continue to peak (51f)
  yield* tweenSizeWithRadius(refs[1], 51/24, 70 + 15 * (39/90), 85, 22 * (39/90), 22);
  // Phase 13: row 1 plateau at peak (3f)
  yield* waitFor(3/24);
  // Phase 14: row 1 size + radius shrink (49 of 89 frames)
  yield* tweenSizeWithRadius(refs[1], 49/24, 85, 85 - 15*(49/89), 22, 22 - 22*(49/89));
  // Phase 15: row 1 finishes shrink + row 0 radius 35→partway (40f)
  yield* all(
    tweenSizeWithRadius(refs[1], 40/24, 85 - 15*(49/89), 70, 22 - 22*(49/89), 0),
    tweenRadius(refs[0], 40/24, 35, 35 - 35*(40/43)),
  );
  // Phase 16: row 0 finishes radius shrink (3f)
  yield* tweenRadius(refs[0], 3/24, 35 - 35*(40/43), 0);
  yield* waitFor(0.1);
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
