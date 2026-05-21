# Rendering Videos | Revideo

## Overview

Revideo provides multiple methods for rendering videos, including browser-based rendering through the editor interface and programmatic rendering via function calls.

## Rendering Methods

### Function-Based Rendering

The `renderVideo()` function enables programmatic video rendering:

```javascript
import {renderVideo} from '@revideo/renderer';

async function render() {
  console.log('Rendering video...');
  const file = await renderVideo({
    projectFile: './src/project.ts',
    settings: {logProgress: true},
  });
  console.log(`Rendered video to ${file}`);
}

render();
```

### Browser-Based Rendering

Users can render videos directly from the editor by clicking the "Render Button" after launching with `npm start`.

## How Rendering Works

The rendering architecture splits responsibilities between browser and backend processes:

- **Browser component**: "loops through all frames in the defined video, draws the defined frames onto an HTML Canvas"
- **Backend component**: Uses FFmpeg to handle audio extraction and processing from `<Video/>` and `<Audio/>` elements

The process generates a muted MP4 file in the browser, then merges extracted audio with the video output.

## Performance

Rendering speeds have improved significantly since version 0.4.6, typically exceeding real-time performance. A dedicated guide addresses factors affecting rendering speed and optimization strategies.

## Parallelized Rendering

For faster rendering of lengthy videos, Revideo supports parallel processing through:

- Single-process parallelization using the `settings.worker` argument
- Serverless function deployment (AWS Lambda recommended) using `renderPartialVideo()`, `concatenateMedia()`, and `mergeAudioWithVideo()` functions

Example implementations are available for AWS Lambda and Google Cloud Functions.
