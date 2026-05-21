import {createSignal, makeProject} from '@revideo/core';
import {Circle, makeScene2D} from '@revideo/2d';

const W = 480;
const H = 360;
const FPS = 24;
const DURATION = 15.041667;
const FRAMES = 361;
const TAU = Math.PI * 2;

const orbit = (radius: number, cycles: number, phase: number, t: number) => {
  const a = phase + (TAU * cycles * t) / DURATION;
  return {
    x: radius * Math.cos(a),
    y: radius * Math.sin(a),
  };
};

const scene = makeScene2D('scene', function* (view) {
  view.fill('#17182b');
  const t = createSignal(0);
  view.add(
    <>
      <Circle x={0} y={0} width={79.8125} height={79.8125} fill={'#fda801'} />
      <Circle x={() => orbit(141.595517858, 5.390686345, -1.262417480, t()).x} y={() => orbit(141.595517858, 5.390686345, -1.262417480, t()).y} width={38.3750} height={38.3750} fill={'#fd8862'} />
      <Circle x={() => orbit(131.406900493, 4.194270606, -1.892424477, t()).x} y={() => orbit(131.406900493, 4.194270606, -1.892424477, t()).y} width={43.1250} height={43.1250} fill={'#36c8b9'} />
      <Circle x={() => orbit(121.557012246, 3.588534811, -2.510064869, t()).x} y={() => orbit(121.557012246, 3.588534811, -2.510064869, t()).y} width={43.2500} height={43.2500} fill={'#b13ddb'} />
      <Circle x={() => orbit(111.507401961, 2.994278106, 3.139279510, t()).x} y={() => orbit(111.507401961, 2.994278106, 3.139279510, t()).y} width={46.8750} height={46.8750} fill={'#f9af0e'} />
      <Circle x={() => orbit(96.396681233, 2.385623690, 2.525564615, t()).x} y={() => orbit(96.396681233, 2.385623690, 2.525564615, t()).y} width={46.3750} height={46.3750} fill={'#00cccb'} />
      <Circle x={() => orbit(70.093750000, 1.800000000, 1.251449561, t()).x} y={() => orbit(70.093750000, 1.800000000, 1.251449561, t()).y} width={43.5620} height={43.5620} fill={'#45b33a'} />
      <Circle x={() => orbit(50.558667389, 0.612316367, -0.015023279, t()).x} y={() => orbit(50.558667389, 0.612316367, -0.015023279, t()).y} width={39.3750} height={39.3750} fill={'#dd3a33'} />
      <Circle x={() => orbit(80.812500000, 1.789250000, 1.891830592, t()).x} y={() => orbit(80.812500000, 1.789250000, 1.891830592, t()).y} width={43.6250} height={43.6250} fill={'#e6419c'} />
    </>,
  );
  for (let i = 0; i < FRAMES; i++) {
    t(i / FPS);
    yield;
  }
});

export default makeProject({
  scenes: [scene],
  settings: {
    shared: {
      size: {x: W, y: H},
    },
    rendering: {
      fps: FPS,
    },
  },
});
