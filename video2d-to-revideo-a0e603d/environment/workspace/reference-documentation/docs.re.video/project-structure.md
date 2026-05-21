# Project Structure | Revideo

## Overview

Revideo projects follow a standard TypeScript structure. The default initialization creates:

```
my-project/
├── package.json
├── package-lock.json
├── tsconfig.json
├── vite.config.ts
├── src/
│   ├── project.ts
│   ├── render.ts
│   ├── project.meta
│   └── scenes/
│       └── example.tsx
└── public/
    └── my-video.mp4
```

## Key Files

### `./src/scenes/example.tsx`

Scene files define video templates using `makeScene2D` with a generator function. They describe the visual content and animations for your video output.

### `./src/project.ts`

This configuration file serves two purposes:

1. Defines an array of scenes that compose the complete video
2. Accepts video variables passed to the visual editor during development

Multiple scenes play sequentially without inheriting nodes from previous scenes, improving performance for complex projects. For logical organization without performance concerns, use separate generator functions instead.

### `vite.config.ts`

Revideo uses Vite to serve the visual editor. The configuration applies the `motionCanvas` plugin to enable editor functionality and ffmpeg audio processing communication.

Customizable options include specifying alternate project files or output directories, plus standard Vite server settings like port configuration.

### `./src/render.ts`

This file executes video rendering via the `npm run render` command. The `renderVideo()` function accepts its own variables independent of those in `project.ts`.

### `/public` Directory

Local files placed here become accessible within scenes using relative paths like `'/my-video.mp4'`.
