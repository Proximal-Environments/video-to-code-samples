# renderVideo() Function Signature & Settings

## Function Signature
```typescript
renderVideo(props: RenderVideoProps): string
```

## RenderVideoProps Parameters

| Field | Type | Description |
|-------|------|-------------|
| `projectFile` | `string` | Points towards your project file. This will probably be `./src/project.ts` |
| `variables?` | `Record<string, any>` | Parameters passed to parameterized videos |
| `settings?` | `RenderSettings` | Rendering configuration object |

## RenderSettings Object

| Field | Type | Description |
|-------|------|-------------|
| `outFile?` | `string` | The file name of the video output (must end with `.mp4`) |
| `outDir?` | `string` | Output directory path; defaults to `./output` |
| `range?` | `[number, number]` | Start and end seconds to render partial video |
| `workers?` | `number` | Number of parallel processes; default is 1 |
| `dimensions?` | `[number, number]` | Video resolution as `[width, height]` |
| `logProgress?` | `boolean` | Logs render progress to the console if set to `true` |
| `ffmpeg?` | `FfmpegSettings` | FFmpeg configuration options |
| `puppeteer?` | `BrowserLaunchArgumentOptions` | Puppeteer browser launch options |
| `viteBasePort?` | `number` | Base port for Vite servers; default is 9000 |
| `viteConfig?` | `InlineConfig` | Vite server configuration |
| `progressCallback?` | `(worker: number, progress: number) => void` | Progress reporting function |

## FfmpegSettings

| Field | Type | Description |
|-------|------|-------------|
| `ffmpegLogLevel?` | `'error' \| 'warning' \| 'info' \| 'verbose' \| 'debug' \| 'trace'` | FFmpeg logging verbosity; defaults to `error` |
| `ffmpegPath?` | `string` | Path to FFmpeg binary; uses bundled version if unspecified |

## Return Value
Returns a `string` containing the path to the rendered video file.
