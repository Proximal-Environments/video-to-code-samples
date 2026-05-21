# Parameterized Videos

To render videos with dynamic inputs or to build video apps, you can use video parameters. Consider this example video:

```typescript
import ...
export default makeScene2D(function* (view) {
  const textRef = createRef<Txt>();
  const name = 'new user';
  view.add(
    <Txt fontSize={1} textWrap={true} ref={textRef} fill={'blue'}>
      Hello {name}!
    </Txt>,
  );
  yield* textRef().scale(30, 2);
});
```

Instead of using the generic `"new user"` string, we might want to use a real name - we can do this using a project variable:

```typescript
import {Txt, makeScene2D} from '@revideo/2d';
import {useScene, createRef} from '@revideo/core';
export default makeScene2D(function* (view) {
  const textRef = createRef<Txt>();
  const name = useScene().variables.get('username', 'new user');
  view.add(
    <Txt fontSize={1} textWrap={true} ref={textRef} fill={'blue'}>
      Hello {name()}!
    </Txt>,
  );
  yield* textRef().scale(30, 2);
});
```

The first argument of `.get()` refers to the name of the variable we want to use, and the second assigns a default value if no variable is provided.

### Passing Parameters to `renderVideo()`

You can pass variables to `renderVideo()` as follows:

```typescript
import {renderVideo} from '@revideo/renderer';
renderVideo({
  projectFile: './src/project.ts',
  variables: {username: 'Mike'},
});
```

### Passing Parameters to visual editor

To use variables in the visual editor, you can pass them to `makeProject` in `src/project.ts`.

```typescript
import {makeProject} from '@revideo/core';
import example from './scenes/example?scene';
export default makeProject({
  scenes: [example],
  variables: {username: 'Mike'},
});
```

### Complex Parameters

Parameters allow you to customize videos extensively. For instance, you can also pass file names as parameters, which can in turn point to audio or images generated from AI services like text-to-speech software or image generators.
