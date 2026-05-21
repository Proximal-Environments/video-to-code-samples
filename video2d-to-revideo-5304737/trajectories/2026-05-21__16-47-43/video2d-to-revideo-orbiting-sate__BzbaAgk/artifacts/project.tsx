import {makeProject} from '@revideo/core';
import {makeScene2D, Circle} from '@revideo/2d';
import {createRef, waitFor} from '@revideo/core';

interface BallParams {
  color: string;
  radius: number;
  orbitR: number;
  startAngle: number; // degrees
  omega: number;      // deg/sec
}

// Measured directly from the reference: each circle is on a quasi-circular
// orbit around the canvas center with its own constant angular velocity.
// Starting angles are arranged in a 10-fold spiral (~36° apart); radii grow
// linearly with index.
const BALLS: BallParams[] = [
  { color: '#fd3132', radius: 19.5, orbitR: 49,  startAngle:  -1.8, omega:  15.3 },
  { color: '#3297fc', radius: 20.0, orbitR: 59,  startAngle:  35.8, omega:  29.1 },
  { color: '#2fcc31', radius: 21.0, orbitR: 70,  startAngle:  72.4, omega:  43.1 },
  { color: '#fe32fe', radius: 21.5, orbitR: 80,  startAngle: 108.5, omega:  43.0 },
  { color: '#00cccb', radius: 22.5, orbitR: 95,  startAngle: 144.5, omega:  57.0 },
  { color: '#fdcb00', radius: 22.5, orbitR:111,  startAngle: 180.3, omega:  71.2 },
  { color: '#c932fc', radius: 21.5, orbitR:121,  startAngle: 216.3, omega:  85.3 },
  { color: '#34e9bc', radius: 21.0, orbitR:131,  startAngle: 251.8, omega: 100.3 },
  { color: '#fd8862', radius: 20.0, orbitR:140,  startAngle: 287.7, omega: 129.2 },
  { color: '#9798fc', radius: 20.0, orbitR:155,  startAngle: 323.8, omega: 158.2 },
];

const BG = '#181a2c';
const ORANGE = '#fda801';
const ORANGE_R = 40;

const scene = makeScene2D('scene', function* (view) {
  view.fill(BG);

  view.add(
    <Circle
      x={0}
      y={0}
      width={ORANGE_R * 2}
      height={ORANGE_R * 2}
      fill={ORANGE}
    />
  );

  const refs = BALLS.map(() => createRef<Circle>());

  BALLS.forEach((b, i) => {
    const a = (b.startAngle * Math.PI) / 180;
    view.add(
      <Circle
        ref={refs[i]}
        x={Math.cos(a) * b.orbitR}
        y={Math.sin(a) * b.orbitR}
        width={b.radius * 2}
        height={b.radius * 2}
        fill={b.color}
      />
    );
  });

  const totalDuration = 15.0;
  const fps = 24;
  const totalFrames = Math.round(totalDuration * fps);
  const dt = 1 / fps;

  for (let f = 0; f < totalFrames; f++) {
    const t = f * dt;
    // Global radial breathing fit: a smoothstep ramp up to +20 (centered around
    // t=3..8), then a second smoothstep that pulls it down through zero to
    // about -11 by t=15. Matches the empirical envelope of the reference.
    const smooth = (x: number) => {
      const c = Math.max(0, Math.min(1, x));
      return c * c * (3 - 2 * c);
    };
    const pulse = 20 * smooth((t - 3) / 5) - 31 * smooth((t - 11) / 4);

    BALLS.forEach((b, i) => {
      const ang = ((b.startAngle + b.omega * t) * Math.PI) / 180;
      const r = b.orbitR + pulse;
      refs[i]().position([Math.cos(ang) * r, Math.sin(ang) * r]);
    });

    yield* waitFor(dt);
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
