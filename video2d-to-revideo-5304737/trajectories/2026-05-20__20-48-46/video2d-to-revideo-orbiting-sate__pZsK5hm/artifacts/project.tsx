import {makeProject, tween, createRef} from '@revideo/core';
import {makeScene2D, Circle} from '@revideo/2d';

function ballPos(f: number): [number, number] {
  let angleDeg: number, radius: number;
  if (f <= 270) {
    angleDeg = 180 + 2.985 * f;
    if (f <= 90) {
      radius = 109;
    } else if (f <= 180) {
      radius = 109 + 21 * ((f - 90) / 90);
    } else {
      radius = 130;
    }
  } else {
    const df = f - 270;
    const startAngle = -94.05;
    angleDeg = startAngle - 14.92 * df - 0.0663 * df * df;
    radius = 130 - 30 * (df / 90);
  }
  const rad = (angleDeg * Math.PI) / 180;
  return [radius * Math.cos(rad), radius * Math.sin(rad)];
}

function trailPos(f: number): [number, number] {
  const angleDeg = -71.6 + 5.35 * f;
  const radius = 139 + (165 - 139) * Math.min(f / 240, 1);
  const rad = (angleDeg * Math.PI) / 180;
  return [radius * Math.cos(rad), radius * Math.sin(rad)];
}

function trailOpacity(f: number): number {
  if (f < 240) return 1;
  if (f < 270) return (270 - f) / 30;
  return 0;
}

const scene = makeScene2D('scene', function* (view) {
  view.fill('#17182B');

  view.add(
    <Circle x={0} y={0} width={80} height={80} fill={'#FDA900'} />,
  );

  const ball = createRef<Circle>();
  const bp0 = ballPos(0);
  view.add(
    <Circle
      ref={ball}
      x={bp0[0]}
      y={bp0[1]}
      width={48}
      height={48}
      fill={'#FDA900'}
    />,
  );

  const trail = createRef<Circle>();
  const tp0 = trailPos(0);
  view.add(
    <Circle
      ref={trail}
      x={tp0[0]}
      y={tp0[1]}
      width={24}
      height={24}
      fill={'#FDA900'}
    />,
  );

  const DURATION = 15;
  yield* tween(DURATION, (t) => {
    const f = t * DURATION * 24;
    const [x, y] = ballPos(f);
    ball().position([x, y]);
    const [tx, ty] = trailPos(f);
    trail().position([tx, ty]);
    trail().opacity(trailOpacity(f));
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
