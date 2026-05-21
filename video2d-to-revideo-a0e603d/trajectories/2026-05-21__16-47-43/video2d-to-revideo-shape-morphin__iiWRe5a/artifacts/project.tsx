import {Path, makeScene2D} from '@revideo/2d';
import {
  all,
  createSignal,
  delay,
  easeInOutCubic,
  makeProject,
  waitFor,
} from '@revideo/core';

const WIDTH = 480;
const HEIGHT = 360;
const FPS = 24;
const DURATION = 481 / FPS;
const BG = '#17182b';

const xs = [-176, -59, 58, 174];
const ys = [-116, 0, 115];

const colors = [
  ['#fd3230', '#31cb33', '#3297fe', '#fdcb00'],
  ['#fd33fb', '#00ccc9', '#fb8900', '#63ff65'],
  ['#c932fc', '#32fdcc', '#fb6664', '#98cbfe'],
];

const fmt = (value: number) => value.toFixed(2);
const edgeCurve = (t: number) => {
  const s = Math.sin(Math.PI * t);
  return s * s;
};

function addEdgeSamples(
  parts: string[],
  count: number,
  point: (t: number) => [number, number],
) {
  for (let i = 1; i <= count; i++) {
    const t = i / (count + 1);
    const [x, y] = point(t);
    parts.push(`L ${fmt(x)} ${fmt(y)}`);
  }
}

function buildCellPath(
  baseWidth: number,
  baseHeight: number,
  corner: number,
  growX: number,
  growY: number,
  dents: {top: number; right: number; bottom: number},
) {
  const width = baseWidth + growX;
  const height = baseHeight + growY;
  const left = -baseWidth / 2;
  const top = -baseHeight / 2;
  const right = left + width;
  const bottom = top + height;
  const radius = Math.max(0, Math.min(corner, width / 2, height / 2));

  const topStartX = left + radius;
  const topEndX = right - radius;
  const rightStartY = top + radius;
  const rightEndY = bottom - radius;
  const bottomStartX = right - radius;
  const bottomEndX = left + radius;
  const leftStartY = bottom - radius;
  const leftEndY = top + radius;

  const parts: string[] = [`M ${fmt(left)} ${fmt(top + radius)}`];

  if (radius > 0) {
    parts.push(`A ${fmt(radius)} ${fmt(radius)} 0 0 1 ${fmt(left + radius)} ${fmt(top)}`);
  } else {
    parts.push(`L ${fmt(left)} ${fmt(top)}`);
  }

  addEdgeSamples(parts, 10, t => [
    topStartX + (topEndX - topStartX) * t,
    top + dents.top * edgeCurve(t),
  ]);
  parts.push(`L ${fmt(topEndX)} ${fmt(top)}`);

  if (radius > 0) {
    parts.push(`A ${fmt(radius)} ${fmt(radius)} 0 0 1 ${fmt(right)} ${fmt(top + radius)}`);
  } else {
    parts.push(`L ${fmt(right)} ${fmt(top)}`);
  }

  addEdgeSamples(parts, 10, t => [
    right - dents.right * edgeCurve(t),
    rightStartY + (rightEndY - rightStartY) * t,
  ]);
  parts.push(`L ${fmt(right)} ${fmt(rightEndY)}`);

  if (radius > 0) {
    parts.push(`A ${fmt(radius)} ${fmt(radius)} 0 0 1 ${fmt(right - radius)} ${fmt(bottom)}`);
  } else {
    parts.push(`L ${fmt(right)} ${fmt(bottom)}`);
  }

  addEdgeSamples(parts, 10, t => [
    bottomStartX - (bottomStartX - bottomEndX) * t,
    bottom - dents.bottom * edgeCurve(t),
  ]);
  parts.push(`L ${fmt(bottomEndX)} ${fmt(bottom)}`);

  if (radius > 0) {
    parts.push(`A ${fmt(radius)} ${fmt(radius)} 0 0 1 ${fmt(left)} ${fmt(bottom - radius)}`);
  } else {
    parts.push(`L ${fmt(left)} ${fmt(bottom)}`);
  }

  if (leftStartY > leftEndY) {
    parts.push(`L ${fmt(left)} ${fmt(leftEndY)}`);
  }

  parts.push('Z');
  return parts.join(' ');
}

const scene = makeScene2D('scene', function* (view) {
  view.fill(BG);

  const topCorner = createSignal(35);
  const topGrowX = createSignal(0);
  const topGrowY = createSignal(0);
  const topWaveCorner = createSignal(0);
  const topDentTop = createSignal(0);
  const topDentRight = createSignal(0);
  const topDentBottom = createSignal(0);

  const middleCorner = createSignal(35);
  const middleGrowX = createSignal(0);
  const middleGrowY = createSignal(0);
  const middleWaveCorner = createSignal(0);
  const middleDentTop = createSignal(0);
  const middleDentRight = createSignal(0);
  const middleDentBottom = createSignal(0);

  view.add(
    <>
      {colors[0].map((fill, index) => (
        <Path
          x={xs[index]}
          y={ys[0]}
          fill={fill}
          lineWidth={0}
          shadowColor={`${fill}88`}
          shadowBlur={4}
          shadowOffset={[2, 2]}
          data={() =>
            buildCellPath(70, 70, topCorner() + topWaveCorner(), topGrowX(), topGrowY(), {
              top: topDentTop(),
              right: topDentRight(),
              bottom: topDentBottom(),
            })
          }
        />
      ))}
      {colors[1].map((fill, index) => (
        <Path
          x={xs[index]}
          y={ys[1]}
          fill={fill}
          lineWidth={0}
          shadowColor={`${fill}88`}
          shadowBlur={4}
          shadowOffset={[2, 2]}
          data={() =>
            buildCellPath(70, 70, middleCorner() + middleWaveCorner(), middleGrowX(), middleGrowY(), {
              top: middleDentTop(),
              right: middleDentRight(),
              bottom: middleDentBottom(),
            })
          }
        />
      ))}
      {colors[2].map((fill, index) => (
        <Path
          x={xs[index]}
          y={ys[2]}
          fill={fill}
          lineWidth={0}
          shadowColor={`${fill}88`}
          shadowBlur={4}
          shadowOffset={[2, 2]}
          data={() => buildCellPath(70, 70, 35, 0, 0, {top: 0, right: 0, bottom: 0})}
        />
      ))}
    </>,
  );

  yield* all(
    delay(2.1, topCorner(0, 1.9, easeInOutCubic)),
    delay(
      6.4,
      all(
        topGrowX(4, 1.5, easeInOutCubic),
        topGrowY(4, 1.5, easeInOutCubic),
        topWaveCorner(4, 1.5, easeInOutCubic),
        topDentTop(0, 1.5, easeInOutCubic),
        topDentRight(5.25, 1.5, easeInOutCubic),
        topDentBottom(5.0, 1.5, easeInOutCubic),
      ),
    ),
    delay(
      8.5,
      all(
        topGrowX(0, 1.5, easeInOutCubic),
        topGrowY(0, 1.5, easeInOutCubic),
        topWaveCorner(0, 1.5, easeInOutCubic),
        topDentTop(0, 1.5, easeInOutCubic),
        topDentRight(0, 1.5, easeInOutCubic),
        topDentBottom(0, 1.5, easeInOutCubic),
      ),
    ),
    delay(12.2, topCorner(35, 2.1, easeInOutCubic)),
    delay(18.1, topCorner(0, 1.9, easeInOutCubic)),
    delay(4.1, middleCorner(0, 3.4, easeInOutCubic)),
    delay(
      12.4,
      all(
        middleGrowX(6, 3.7, easeInOutCubic),
        middleGrowY(12, 3.7, easeInOutCubic),
        middleWaveCorner(4, 3.7, easeInOutCubic),
        middleDentTop(3.5, 3.7, easeInOutCubic),
        middleDentRight(6.0, 3.7, easeInOutCubic),
        middleDentBottom(5.5, 3.7, easeInOutCubic),
      ),
    ),
    delay(
      16.4,
      all(
        middleGrowX(0, 3.4, easeInOutCubic),
        middleGrowY(0, 3.4, easeInOutCubic),
        middleWaveCorner(0, 3.4, easeInOutCubic),
        middleDentTop(0, 3.4, easeInOutCubic),
        middleDentRight(0, 3.4, easeInOutCubic),
        middleDentBottom(0, 3.4, easeInOutCubic),
      ),
    ),
    waitFor(DURATION),
  );
});

export default makeProject({
  scenes: [scene],
  settings: {
    shared: {
      size: {x: WIDTH, y: HEIGHT},
    },
    rendering: {
      fps: FPS,
    },
  },
});
