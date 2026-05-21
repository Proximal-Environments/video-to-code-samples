# Media Component Documentation

## Overview

The `Media` class is an abstract component that extends `Asset` and serves as a base for audio and video playback components.

**Extended by:** `Audio`, `Video`

## Constructor

```typescript
public override new Media(props: MediaProps): Media
```

## Playback Control Properties

| Property | Type | Description |
|----------|------|-------------|
| `loop` | `SimpleSignal<boolean>` | Controls whether media repeats |
| `playbackRate` | `SimpleSignal<number>` | Controls playback speed |
| `playing` | `SimpleSignal<boolean>` | Current playback state |
| `time` | `SimpleSignal<number>` | Current playback time |
| `volume` | `SimpleSignal<number>` | Audio volume level |

## Inherited Properties

Transform, visual, layout, edge position, curve/shape, text, effects, and source properties from Asset/Shape/Layout/Node.

## Playback Control Methods

```typescript
play(): void
pause(): void
isPlaying(): boolean
getCurrentTime(): number
setCurrentTime(time: number): void
getDuration(): number
setPlaybackRate(rate: number): void
setVolume(volume: number): void
getVolume(): number
getUrl(): string
clampTime(time: number): number
```

## State, Hierarchy, Transform, Layout, Curve, Rendering, and Utility Methods

All standard node methods inherited from parent classes.
