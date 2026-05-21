import {makeProject} from '@revideo/core';
import {makeScene2D, Rect} from '@revideo/2d';
import {createRef, all, waitFor, linear} from '@revideo/core';

const COLORS = [
  '#fd3230', '#31cb33', '#3297fe', '#fdcb00',
  '#fd33fb', '#00ccc9', '#fb8900', '#63ff65',
  '#c932fc', '#32fdcc', '#fa6764', '#98cbfe'
];

const CENTERS_X = [-175.5, -59, 57.5, 174];
const CENTERS_Y = [-115.5, -0.5, 114.5];

const BASE_SIZE = 70;
const BASE_RADIUS = 35;
const EDGE_GROW = 6;
const INNER_GROW_TOTAL = 12;

const FPS = 24;
const F = (n: number) => n / FPS; // frames to seconds

const scene = makeScene2D('scene', function* (view) {
  view.fill('#17182b');

  const refs: any[] = Array(12).fill(null).map(() => createRef<Rect>());
  for (let i = 0; i < 12; i++) {
    const row = Math.floor(i / 4);
    const col = i % 4;
    view.add(
      <Rect
        ref={refs[i]}
        x={CENTERS_X[col]}
        y={CENTERS_Y[row]}
        width={BASE_SIZE}
        height={BASE_SIZE}
        radius={BASE_RADIUS}
        fill={COLORS[i]}
      />
    );
  }

  function peakParams(row: number, col: number) {
    const baseX = CENTERS_X[col];
    const baseY = CENTERS_Y[row];
    let targetWidth: number, targetHeight: number;
    let dx = 0, dy = 0;
    if (col === 0) { targetWidth = BASE_SIZE + EDGE_GROW; dx = EDGE_GROW / 2; }
    else if (col === 3) { targetWidth = BASE_SIZE + EDGE_GROW; dx = -EDGE_GROW / 2; }
    else { targetWidth = BASE_SIZE + INNER_GROW_TOTAL; }
    if (row === 0) { targetHeight = BASE_SIZE + EDGE_GROW; dy = EDGE_GROW / 2; }
    else if (row === 2) { targetHeight = BASE_SIZE + EDGE_GROW; dy = -EDGE_GROW / 2; }
    else { targetHeight = BASE_SIZE + INNER_GROW_TOTAL; }
    return {x: baseX + dx, y: baseY + dy, width: targetWidth, height: targetHeight};
  }

  function* growStage(rowIdx: number, duration: number, peakRadius: number) {
    const tasks = [0,1,2,3].map(col => {
      const r = refs[rowIdx * 4 + col];
      const p = peakParams(rowIdx, col);
      return all(
        r().width(p.width, duration, linear),
        r().height(p.height, duration, linear),
        r().x(p.x, duration, linear),
        r().y(p.y, duration, linear),
        r().radius(peakRadius, duration, linear),
      );
    });
    yield* all(...tasks);
  }

  function* shrinkStage(rowIdx: number, duration: number) {
    const tasks = [0,1,2,3].map(col => {
      const r = refs[rowIdx * 4 + col];
      const baseX = CENTERS_X[col];
      const baseY = CENTERS_Y[rowIdx];
      return all(
        r().width(BASE_SIZE, duration, linear),
        r().height(BASE_SIZE, duration, linear),
        r().x(baseX, duration, linear),
        r().y(baseY, duration, linear),
        r().radius(0, duration, linear),
      );
    });
    yield* all(...tasks);
  }

  function* radiusStage(rowIdx: number, target: number, duration: number) {
    const rs = [0,1,2,3].map(c => refs[rowIdx * 4 + c]);
    yield* all(...rs.map(r => r().radius(target, duration, linear)));
  }

  // Row 0 timing (from c0 data):
  // f0-48: initial circle (48 frames hold)
  // f49-91: circle→square (42f)
  // f91-146: hold square (55f)
  // f146-192: grow (46f)
  // f192-240: shrink (48f)
  // f240-294: hold square (54f)
  // f294-340: square→circle (46f)
  // f340-432: hold circle (92f)
  // f432-480: circle→square (48f)
  
  function* runRow0() {
    yield* waitFor(F(48));     // initial hold
    yield* radiusStage(0, 0, F(42));
    yield* waitFor(F(55));
    yield* growStage(0, F(46), 12);
    yield* shrinkStage(0, F(48));
    yield* waitFor(F(54));
    yield* radiusStage(0, BASE_RADIUS, F(46));
    yield* waitFor(F(92));
    yield* radiusStage(0, 0, F(48));
  }

  // Row 1 timing (from c5 data):
  // f0-96: initial circle (96 frames)
  // f97-190: circle→square (93f) - need to verify
  // f190-294: hold square (~100f)
  // f294-385: grow (~91f)
  // f385-480: shrink (~95f)
  
  function* runRow1() {
    yield* waitFor(F(98));
    yield* radiusStage(1, 0, F(90));
    yield* waitFor(F(103));
    yield* growStage(1, F(92), 22);
    yield* shrinkStage(1, F(97));
  }

  yield* all(runRow0(), runRow1());
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
