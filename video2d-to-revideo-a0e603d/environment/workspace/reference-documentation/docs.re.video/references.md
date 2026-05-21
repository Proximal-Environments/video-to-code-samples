# References

_Note: These docs were adopted from the original Motion Canvas docs_

Usually, when creating a node, we want to store a reference to it, so we can animate it later. One way to do that is by assigning it to a variable first, and then adding it to the scene:

```
const circle = <Circle />;
view.add(circle);
// we can now animate our circle:
yield * circle.scale(2, 0.3);
```

> If you're used to libraries such as React, the above example may seem strange. In Motion Canvas, the JSX components immediately create and return an instance of the given class.

But this approach doesn't scale well. The more nodes we add, the harder it gets to see the overall structure of our scene. Consider the following example:

```
const rectA = <Rect />;
const rectB = <Rect />;
const circle = <Circle>{rectA}</Circle>;
view.add(
  <Layout>
    {circle}
    {rectB}
  </Layout>,
);
```

And now compare it to a version that doesn't store any references:

```
view.add(
  <Layout>
    <Circle>
      <Rect />
    </Circle>
    <Rect />
  </Layout>,
);
```

## `ref` property

Each node in Motion Canvas has a property called `ref` that allows you to create a reference to said node. It accepts a callback that will be invoked right after the node has been created, with the first argument being the newly created instance.

With this in mind, we can rewrite the initial example as:

```
let circle: Circle;
view.add(
  <Circle
    ref={instance => {
      circle = instance;
    }}
  />,
);
yield * circle.scale(2, 0.3);
```

Using the `ref` property in this way is not really practical, and we wouldn't recommend it. But it's crucial to understand how it works because all the upcoming methods use this property as a base.

## `createRef()` function

The preferred way of using the `ref` property is in conjunction with the `createRef()` function. Continuing with our example, we can rewrite it as:

```
import {createRef} from '@revideo/core';
// ...
const circle = createRef<Circle>();
view.add(<Circle ref={circle} />);
yield * circle().scale(2, 0.3);
```

Notice that `circle` is no longer just a variable that points to our circle. Instead, it's a signal-like function that can be used to access it. Invoking it without any arguments (`circle()`) returns our instance.

Going back to the example with the more complex scene, we can now rewrite it as:

```
const rectA = createRef<Rect>();
const rectB = createRef<Rect>();
const circle = createRef<Circle>();
view.add(
  <Layout>
    <Circle ref={circle}>
      <Rect ref={rectA} />
    </Circle>
    <Rect ref={rectB} />
  </Layout>,
);
```

## `makeRef()` function

Another common use case of the `ref` property is to assign the newly created instance to a property of some object. In the following example, we assign our circle to `circle.instance`:

```
const circle = {instance: null as Circle};
view.add(
  <Circle
    ref={instance => {
      circle.instance = instance;
    }}
  />,
);
```

We can use the `makeRef()` function to simplify this process:

```
import {makeRef} from '@revideo/core';
// ...
const circle = {instance: null as Circle};
view.add(
  <Circle ref={makeRef(circle, 'instance')} />,
);
```

### Array of references

`makeRef()` can be particularly useful when we create an array of nodes and want to grab references to all of them:

```
const circles: Circle[] = [];
view.add(
  <Layout>
    {range(10).map(index => (
      <Circle ref={makeRef(circles, index)} />
    ))}
  </Layout>,
);
```

In JavaScript, arrays are objects whose properties are their indices. So `makeRef(circles, index)` will set the nth element of our array to the created circle. As a result, we end up with an array of size `10` filled with circles that we can use to animate all of them.

You can also use the `createRefArray()` helper function to achieve the same result:

```
import {createRefArray, range} from '@revideo/core';
// ...
const circles = createRefArray<Circle>();
view.add(
  <Layout>
    {range(10).map(() => (
      <Circle ref={circles} />
    ))}
  </Layout>,
);
```

This time we don't specify the index. Whenever we pass the `circles` array to the `ref` property, the newly created circle will be appended to our array.

> Check out the looping section in the flow guide to see how an array of references can be used to orchestrate animations.

### Custom functions

`makeRef()` can also be used to return more than one reference from a custom function component:

```
function Label({
  refs,
  children,
}: {
  refs: {rect: Rect; text: Txt};
  children: string;
}) {
  return (
    <Rect ref={makeRef(refs, 'rect')}>
      <Txt ref={makeRef(refs, 'text')}>{children}</Txt>
    </Rect>
  );
}
const label = {rect: null as Rect, text: null as Txt};
view.add(<Label refs={label}>HELLO</Label>);
// we can now animate both the Rect and the Text of our label:
yield * label.rect.opacity(2, 0.3);
yield * label.text.fontSize(24, 0.3);
```

## `createRefMap()` function

As the scene grows in complexity, declaring a reference for each node can become tedious. The `createRefMap()` helper function lets us group references together based on the type of the node:

```
import {createRefMap} from '@revideo/core';
// ...
const labels = createRefMap<Txt>();
view.add(
  <>
    <Txt ref={labels.a}>A</Txt>
    <Txt ref={labels.b}>B</Txt>
    <Txt ref={labels.c}>C</Txt>
  </>,
);
```

The returned object is a map that can store however many references we need. Later on, we can retrieve the references using the same keys:

```
yield * labels.a().text('A changes', 0.3);
yield * labels.b().text('B changes', 0.3);
yield * labels.c().text('C changes', 0.3);
```

The returned object comes with a `mapRefs` method that lets us map over all references in the map:

```
yield * all(...labels.mapRefs(label => label.fill('white', 0.3)));
```

## `makeRefs()` function

We can use `makeRefs()` to eliminate type redundancy when using `makeRef()` with custom function components:

```
import {makeRef, makeRefs} from '@revideo/core';
// ...
function Label({
  refs,
  children,
}: {
  refs: {rect: Rect; text: Txt};
  children: string;
}) {
  return (
    <Rect ref={makeRef(refs, 'rect')}>
      <Txt ref={makeRef(refs, 'text')}>{children}</Txt>
    </Rect>
  );
}
const label = makeRefs<typeof Label>();
view.add(<Label refs={label}>HELLO</Label>);
```
