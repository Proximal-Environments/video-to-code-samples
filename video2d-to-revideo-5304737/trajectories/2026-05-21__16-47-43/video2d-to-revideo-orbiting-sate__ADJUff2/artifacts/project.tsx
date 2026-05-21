import {createSignal, makeProject} from '@revideo/core';
import {Circle, makeScene2D} from '@revideo/2d';

const FRAME_COUNT = 361;
const FPS = 24;
const DURATION = (FRAME_COUNT - 2) / FPS;
const MOTION_DURATION = 15;
const BACKGROUND = '#17182b';

type Orbiter = {
  color: string;
  diameter: number;
  radius: number;
  phase: number;
  turns: number;
};

const orbiters: Orbiter[] = [
  {color: '#fc8862', diameter: 40, radius: 141, phase: -1.260, turns: 5.4},
  {color: '#fdcb00', diameter: 46, radius: 110, phase: -3.133, turns: 3.0},
  {color: '#00cccb', diameter: 48, radius: 95, phase: 2.513, turns: 2.4},
  {color: '#fe32fe', diameter: 44, radius: 79, phase: 1.904, turns: 1.8},
  {color: '#2fcc31', diameter: 44, radius: 68, phase: 1.259, turns: 1.8},
  {color: '#32fdcc', diameter: 42, radius: 131, phase: -1.890, turns: 4.2},
  {color: '#9698fb', diameter: 40, radius: 155, phase: -0.634, turns: 6.6},
  {color: '#c932fc', diameter: 42, radius: 121, phase: -2.515, turns: 3.6},
  {color: '#3296fb', diameter: 42, radius: 59, phase: 0.640, turns: 1.2},
  {color: '#fd3232', diameter: 40, radius: 50, phase: 0.020, turns: 0.6},
];

function orbitX(
  time: () => number,
  radius: number,
  phase: number,
  turns: number,
) {
  return () => {
    const angle = phase + (2 * Math.PI * turns * time()) / MOTION_DURATION;
    return radius * Math.cos(angle);
  };
}

function orbitY(
  time: () => number,
  radius: number,
  phase: number,
  turns: number,
) {
  return () => {
    const angle = phase + (2 * Math.PI * turns * time()) / MOTION_DURATION;
    return radius * Math.sin(angle);
  };
}

const scene = makeScene2D('scene', function* (view) {
  const time = createSignal(0);
  view.fill(BACKGROUND);
  yield view.add(
    <>
      <Circle size={68} fill={'#fda801'} />
      {orbiters.map(({color, diameter, radius, phase, turns}) => (
        <Circle
          width={diameter}
          height={diameter}
          x={orbitX(time, radius, phase, turns)}
          y={orbitY(time, radius, phase, turns)}
          fill={color}
        />
      ))}
    </>,
  );
  yield* time(MOTION_DURATION, DURATION);
});

export default makeProject({
  scenes: [scene],
  settings: {
    shared: {
      size: {x: 480, y: 360},
    },
    rendering: {
      fps: FPS,
    },
  },
});
