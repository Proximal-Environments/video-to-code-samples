# Transparent Video

Revideo supports the use of transparent videos. This is useful when you want to overlay a video on top of other content, such as a background image or video.

Make sure the transparent video you're using is encoded using the `VP9` codec. These files usually have a `.webm` extension.

You can use command line tools such as `ffmpeg` to re-encode videos from one codec to another.

**Note:** There are other video codecs that support transparency, such as `HEVC`, which might show up correctly in the preview through the UI or inside the player, but will lose their transparency when rendering.

### Code Example

```typescript
import ...

export default makeScene2D(function* (view) {
  const avatarRef = createRef<Video>();
  const backgroundRef = createRef<Img>();

  yield view.add(
    <>
      <Img
        src={'https://revideo-example-assets.s3.amazonaws.com/mountains.jpg'}
        width={'100%'}
        ref={backgroundRef}
      />
      <Video
        src={'https://revideo-example-assets.s3.amazonaws.com/avatar.webm'}
        play={true}
        height={'100%'}
        ref={avatarRef}
      />
    </>,
  );

  yield* waitFor(avatarRef().getDuration());
});
```
