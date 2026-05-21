# Slow Rendering

The rendering speed of Revideo projects depends on the content of your video. Projects that contain no `<Video/>` elements generally render much faster than those that do, as processing videos is an expensive operation.

Here you can find some strategies that can help speed up rendering:

## Upgrade to >=v0.4.4

We regularly release new versions of Revideo that often come with performance improvements. To get the best rendering speeds possible, make sure to upgrade Revideo to >=v0.4.4.

## Use MP4 decoder

We use the Webcodecs API to extract frames from `<Video/>` elements during rendering. This, however, is currently only supported for mp4 files, and Revideo will use Ffmpeg-based decoder or naively seek set the `.currentTime` attribute on the HTMLVideoElement if it detects another file type.

If Revideo fails to detect a file type, you will receive the following warning:

> WARNING: Could not detect file type of video, will default to using mp4 decoder. If your video file is no mp4 file, this will lead to an error - to fix this, reencode your video as an mp4 file (better performance) or specify a different decoder.

If this occurs, you can set the decoder explicitly as a prop of your `<Video/>` tag:

```typescript
yield view.add(<Video src={'your_file'} decoder={'web'} />);
```

You should use the following decoder for different file types:

- `decoder={"web"}` for mp4
- `decoder={"ffmpeg"}` for .webm
- `decoder={"slow"}` for everything else

## Lower output resolution through `resolutionScale` in `project.meta`

You can scale down the quality of your render output by setting the `resolutionScale` parameter in the `rendering` section of `project.meta`. We have noticed that setting the scale to 0.5 made our renders twice as fast as with the default of 1.0.

## Use smaller assets

When using media such as `<Img/>` or `<Video/>` elements, processing large files takes Revideo longer than smaller ones. If you want to render a video with a resolution of 1920x1080, it would be overkill to insert a 4K video inside a `<Video/>` tag, as the resolution will be scaled down anyway. In this case, you can speed up renders by using a smaller file.

## Parallelize Rendering

You can parallelize your rendering workloads using the `workers` argument in `renderVideo()`. Note that this can get memory-intensive, as it spins up multiple ffmpeg workers in parallel - you might have to switch to more powerful hardware to support a lot of workers.

Alternatively, you can also parallelize render workloads using `renderPartialVideo()` and serverless function services such as Google Cloud Run or AWS Lambda.
