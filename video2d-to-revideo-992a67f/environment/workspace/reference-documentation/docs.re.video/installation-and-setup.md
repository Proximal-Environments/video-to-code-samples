# Revideo Quickstart - Complete Page Content

## Quickstart

Let's install revideo with a sample project. To use revideo, make sure that you have [Node.js](https://nodejs.org/) version 16 or greater.

> If you're on Linux, also make sure that you have nscd installed: `sudo apt-get install nscd`. You need this package for ffmpeg.

### Creating a new project

Run the following command to create a new revideo project (If this fails, check out the troubleshooting section):

```
npm init @revideo@latest
```

Now, select the **default project**, navigate to its folder and install all dependencies:

```
cd <project-path>
npm install
```

To preview your video in the editor, run:

```
npm start
```

The editor can now be accessed by visiting [http://localhost:9000/](http://localhost:9000/). Here you should see the video shown below.

```typescript
import {Audio, Img, Video, makeScene2D} from '@revideo/2d';
import {all, chain, createRef, waitFor} from '@revideo/core';

export default makeScene2D(function* (view) {
  const logoRef = createRef<Img>();
  yield view.add(
    <>
      <Video
        src={'https://revideo-example-assets.s3.amazonaws.com/stars.mp4'}
        play={true}
        size={['100%', '100%']}
      />
      <Audio
        src={'https://revideo-example-assets.s3.amazonaws.com/chill-beat.mp3'}
        play={true}
        time={17.0}
      />
    </>,
  );
  yield* waitFor(1);
  view.add(
    <Img
      width={'1%'}
      ref={logoRef}
      src={
        'https://revideo-example-assets.s3.amazonaws.com/revideo-logo-white.png'
      }
    />,
  );
  yield* chain(
    all(logoRef().scale(40, 2), logoRef().rotation(360, 2)),
    logoRef().scale(60, 1),
  );
});
```

## Rendering the Video

You can render your video by running:

```
npm run render
```

This will call the `./src/render.ts` script in your code:

```typescript
import {renderVideo} from '@revideo/renderer';

async function render() {
  console.log('Rendering video...');
  // This is the main function that renders the video
  const file = await renderVideo({
    projectFile: './src/project.ts',
    settings: {logProgress: true},
  });
  console.log(`Rendered video to ${file}`);
}

render();
```

For more information, check out the [renderVideo()](/api/renderer/renderVideo) API reference.

Alternatively, you can also render your video using the button in the editor that starts when you run `npm run start`.

### Rendering from the browser

To render videos from the editor, simply click the "Render" Button:

![Render Button](https://revideo-example-assets.s3.amazonaws.com/render-button.png)

## Understanding the Video Code

For now, we can ignore all files in our revideo project except for `src/scenes/example.tsx`, as this is where the visuals and audio of our video are defined. Let's walk through all the parts of the code that might confuse you, and provide explanations and references.

### Defining a generator function

Our animation is defined within a generator function that is passed to `makeScene2D` - this function describes the sequence of events happening in our video:

```typescript
import {Audio, Img, Video, makeScene2D} from '@revideo/2d';
import {all, chain, createRef, waitFor} from '@revideo/core';

export default makeScene2D(function* (view) {
// your animation flow here
```

Generator functions can return multiple values - when they are called, they will execute until they first encounter a `yield` statement, and return the yielded value. Revideo renders animations by continually calling the generator function, which will yield frames that we can export. It is not neccessary to understand how this works exactly, but if you are interested, you can read about the animation flow in revideo [here](/flow).

### Adding Video and Audio elements

At the start of our generator function, we add [Video](/api/2d/components/Video) and [Audio](/api/2d/components/Audio) tags to our `view`, which will display them on the canvas. Other components you could add include [Txt](/api/2d/components/Txt) or [Img](/api/2d/components/Img) tags, or basic shapes like [Rect](/api/2d/components/Rect) or [Circle](/api/2d/components/Circle). You can find the API for all components [here](/api/2d/components).

```typescript
yield view.add(
  <>
    <Video
      src={'https://revideo-example-assets.s3.amazonaws.com/stars.mp4'}
      play={true}
      size={['100%', '100%']}
    />
    <Audio
      src={'https://revideo-example-assets.s3.amazonaws.com/chill-beat.mp3'}
      play={true}
      time={17.0}
    />
  </>,
);
```

A few points about input arguments:

- In both cases, `src` refers to the file, which points to a remote url on the bucket. Alternatively, you can use local files by passing their path.
- Passing `size={["100%", "100%"]}` makes the video stretch to the full width and height of its canvas.
- Adding `play={true}` makes both media elements play immediately, instead of being in a paused state.

### Play media for one second

After adding our background video and audio, we execute

```typescript
yield * waitFor(1);
```

The function [waitFor](/api/core/flow/#waitFor) does - as the name suggests - nothing. It is particularly useful when waiting for media (like videos and audio) to play or when we want to have a still-standing image.

### Animating the revideo logo

Lastly, we let the revideo logo spin into our video:

```typescript
view.add(
  <Img
    width={'1%'}
    ref={logoRef}
    src={
      'https://revideo-example-assets.s3.amazonaws.com/revideo-logo-white.png'
    }
  />,
);
yield *
  chain(
    all(logoRef().scale(40, 2), logoRef().rotation(360, 2)),
    logoRef().scale(60, 1),
  );
```

A few things happen here: First, we add the revideo logo as an [Img](/api/2d/components/Img) to our canvas. We set its initial width to only 1% of the screen, as we want it to grow as the video plays. We also pass a [reference](/references) through `ref={logoRef}`, which we had initialized before. Like [React refs](https://react.dev/learn/referencing-values-with-refs), references allow us to access and modify the behavior of elements after they've been initialized.

In our code, we use a reference to the revideo logo to later animate it. Particularly, we run the following commands:

- `scale(x, s)`: scales the size of the logo to `x` times its original size, within `n` seconds.
- `rotation(d, s)`: rotates the image by `d` degrees within `s` seconds

The flow of these animations is determined by the keywords [chain](/flow/#chain) and [all](/flow/#all). The former instructs revideo to play its input animations after one another, while the latter instructs revideo to play them simultaneously. As a result, we first see the revideo logo rotating around 360 degrees while growing to 40x its original size. After this is done, the logo still grows to 60x its original size. You can learn more about the animation flow in revideo [here](/flow).

## Troubleshooting

**`npm init @revideo@latest` fails to execute.**

There was [a bug in npm](https://github.com/npm/cli/issues/5175) causing the above command to fail. It got fixed in version `8.15.1`. You can follow [this guide](https://docs.npmjs.com/try-the-latest-stable-version-of-npm) to update your npm. Alternatively, you can use the following command instead:

```
npm exec @revideo/create@latest
```

**`npm install` fails with `code ENOENT`**

If `npm install` fails with the following error:

```
npm ERR! code ENOENT
npm ERR! syscall open
npm ERR! path [path]\package.json
npm ERR! errno -4058
npm ERR! enoent ENOENT: no such file or directory, open '[path]\package.json'
npm ERR! enoent This is related to npm not being able to find a file.
npm ERR! enoent
```

Make sure that you're executing the command in the correct directory. When you finish bootstrapping the project with `npm init`, it will display three commands:

```
cd [path]
npm install
npm start
```

Did you run the `cd` command to switch to the directory containing your project?

**I moved the camera too far away and can't find the preview (The preview is is black)**

You can press `0` to refocus the camera on the preview.

**The animation ends abruptly or does not start at the beginning.**

Make sure the playback range selector in the timeline starts and ends where you expect it to, e.g., at the beginning and end of your animation. The range selector is a gray bar in the time axis of your timeline. When you move your mouse over it, six dots will appear allowing you to manipulate it.

**File watching does not work on Windows Subsystem for Linux (WSL) 2**

When running Vite on WSL2, file system watching does not work if a file is edited by Windows applications.

To fix this, move the project folder into the WSL2 file system and use WSL2 applications to edit files. Accessing the Windows file system from WSL2 is slow, so this will improve performance.

For more information view the [**Vite Docs**](https://vitejs.dev/config/server-options.html#server-watch).

---

Copyright © 2024 Revideo. Built with Docusaurus.
