import {makeProject, createRef, all, waitFor} from '@revideo/core';
import {makeScene2D, Rect} from '@revideo/2d';

const scene = makeScene2D('scene', function* (view) {
  view.fill('#191a2d');

  const cx = [-176, -59, 58, 175];
  const cy = [-116, 0, 115];

  const colors = [
    ['#ff3030', '#33d033', '#3399ff', '#ffcc00'],
    ['#ff33ff', '#00d0cd', '#ff8a00', '#66ff66'],
    ['#cc33ff', '#33ffcc', '#ff6666', '#99ccff'],
  ];

  const peakSize = 82;
  const peakRadius = 22;
  const plateauSize = 70;
  const plateauRadius = 5;
  const baseSize = 70;
  const baseRadius = 35;

  const refs: any[][] = [[], [], []];
  for (let r = 0; r < 3; r++) {
    for (let c = 0; c < 4; c++) {
      const ref = createRef<Rect>();
      view.add(
        <Rect
          ref={ref}
          x={cx[c]}
          y={cy[r]}
          width={baseSize}
          height={baseSize}
          radius={baseRadius}
          fill={colors[r][c]}
        />,
      );
      refs[r].push(ref);
    }
  }

  function* animateRow(row: number) {
    const rs = refs[row];
    const phase = row === 0 ? 2 : 4;
    if (row === 2) return;

    yield* waitFor(phase);
    yield* all(...rs.map(r => r().radius(plateauRadius, phase)));
    yield* waitFor(phase);
    yield* all(
      ...rs.map(r => r().size(peakSize, phase)),
      ...rs.map(r => r().radius(peakRadius, phase)),
    );
    yield* all(
      ...rs.map(r => r().size(plateauSize, phase)),
      ...rs.map(r => r().radius(plateauRadius, phase)),
    );
    if (row === 0) {
      yield* waitFor(phase);
      yield* all(...rs.map(r => r().radius(baseRadius, phase)));
      yield* waitFor(phase * 2);
      yield* all(...rs.map(r => r().radius(plateauRadius, phase)));
    }
  }

  yield* all(animateRow(0), animateRow(1), animateRow(2));
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
