# Revideo — Code Examples and API Patterns from GitHub README

## Project Initialization
```bash
npm init @revideo@latest
```

## Core Imports
```typescript
import {Audio, Img, Video, makeScene2D} from '@revideo/2d';
import {all, chain, createRef, waitFor} from '@revideo/core';
```

## Scene Creation Pattern
The framework uses a generator function approach with the `makeScene2D()` API:

```typescript
export default makeScene2D('scene', function* (view) {
  // Scene logic here
});
```

## Key API Usage Examples

**Ref Creation:**
```typescript
const logoRef = createRef<Img>();
```

**View Addition:**
```typescript
yield view.add(
  <>
    <Video src={'url'} size={['100%', '100%']} play={true} />
    <Audio src={'url'} play={true} time={17.0} />
  </>
);
```

**Animation Composition:**
```typescript
yield* chain(
  all(logoRef().scale(40, 2), logoRef().rotation(360, 2)),
  logoRef().scale(60, 1),
);
```

**Timing Control:**
```typescript
yield* waitFor(1); // Wait 1 second
```

## Headless Rendering
The documentation references a `renderVideo()` function call for programmatic rendering, enabling API deployments without UI interaction.

## Telemetry Control
```bash
DISABLE_TELEMETRY=true
```
