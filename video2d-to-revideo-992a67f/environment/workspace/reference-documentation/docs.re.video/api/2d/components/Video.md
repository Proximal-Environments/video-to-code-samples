# Video Component Documentation

## Overview

The `Video` class extends `Media` and represents a video component for controlling video playback, rendering, and transformation.

## Constructor

```typescript
public override new Video(props: VideoProps): Video
```

## Key Properties

### Media Control
- **`decoder`**: Signal controlling which decoder to use (`'web'`, `'ffmpeg'`, `'slow'`, or `null`)
- **`playbackRate`**: Controls playback speed
- **`loop`**: Boolean signal for looping behavior
- **`alpha`**: Alpha value affecting the video itself (separate from opacity)
- **`smoothing`**: Boolean signal; when disabled, applies pixelated nearest-neighbor scaling

### Inherited Properties

All Media properties: src, size, position, rotation, scale, opacity, layout, effects.

## Methods

### Playback Control
```typescript
play(): void
pause(): void
isPlaying(): boolean
getCurrentTime(): number
getDuration(): number
setVolume(volume: number): void
getVolume(): number
```

### All standard node methods

Transform, state, hierarchy, rendering, search, clone, curve operations.

## Key Features

- **Decoder Support**: `'web'` for fastest MP4, `'ffmpeg'` for format flexibility, `'slow'` for comprehensive compatibility
- **Smoothing Control**: When disabled, video is scaled using nearest neighbor interpolation
- **Full 2D transform**: position, rotation, scale, skew with local and world-space helpers
- **Integrated layout**: Flexbox-style layout system
