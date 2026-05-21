# Layouts

_Note: These docs were adopted from the original Motion Canvas docs_

Layouts allow you to arrange your nodes using Flexbox. Any node extending the `Layout` node can become a part of the layout. This includes, but is not limited to: `Rect`, `Circle`, and `Img`.

## Layout root

Layouts are an opt-in feature, meaning that they need to be enabled. It's done by setting the `layout` property on the Node that we want to become the root of our layout:

```
// layout root
<Rect layout>
  {/* layout child */}
  <Circle width={320} height={320} />
</Rect>
```

In the example above, we marked the `<Rect>` as the layout root. This will cause the position and size of its descendants to be controlled by Flexbox (In this case there's only one valid descendant: `<Circle>`). The layout root itself is treated differently than its children - its size is controlled by Flexbox, but the position stays unaffected.

> Just setting the `layout` property doesn't always turn the node into a layout root. If the node is already a part of the layout, it will be treated like the rest of the descendants:

```
// layout root
<Rect layout>
  {/* layout child, NOT a layout root */}
  <Rect layout>
    {/* layout child */}
    <Circle width={320} height={320} />
  </Rect>
</Rect>
```

## Size and offset

Aside from the position, rotation, and scale, any node extending the `Layout` class has additional `size` and `offset` properties:

### `Layout.size`

```
readonly public size: Vector2LengthSignalLayout
```

Represents the size of this node.

A size is a two-dimensional vector, where `x` represents the `width`, and `y` represents the `height`.

The value of both x and y is of type `Length` which is either:

- `number` - the desired length in pixels
- `${number}%` - a string with the desired length in percents, for example `'50%'`
- `null` - an automatic length

When retrieving the size, all units are converted to pixels, using the current state of the layout. For example, retrieving the width set to `'50%'`, while the parent has a width of `200px` will result in the number `100` being returned.

When the node is not part of the layout, setting its size using percents refers to the size of the entire scene.

### `Layout.offset`

```
readonly public offset: Vector2SignalLayout
```

Represents the offset of this node's origin.

By default, the origin of a node is located at its center. The origin serves as the pivot point when rotating and scaling a node, but it doesn't affect the placement of its children.

The value is relative to the size of this node. A value of `1` means as far to the right/bottom as possible. Here are a few examples of offsets:

- `[-1, -1]` - top left corner
- `[1, -1]` - top right corner
- `[0, 1]` - bottom edge
- `[-1, 1]` - bottom left corner

## Cardinal directions

Layout nodes come with a set of helper properties that let you position them in respect to their edges/corners. In the example below we use them to place two squares on the left and right side of a gray rectangle. The yellow square is positioned so that its right edge is in the same place as the left edge of the rectangle. Meanwhile, the red square is placed so that its bottom left corner aligns with the bottom right corner of the rectangle. All possible directions include: `middle`, `top`, `bottom`, `left`, `right`, `topLeft`, `topRight`, `bottomLeft`, and `bottomRight`.

```
import ...
export default makeScene2D(function* (view) {
  const rect = createRef<Rect>();

  view.add(
    <>
      <Rect
        ref={rect}
        width={200}
        height={100}
        rotation={-10}
        fill={'#333333'}
      />
      <Rect
        size={50}
        fill={'#e6a700'}
        rotation={rect().rotation}
        // Try changing "right" to "top"
        right={rect().left}
      />
      <Rect
        size={100}
        fill={'#e13238'}
        rotation={10}
        bottomLeft={rect().bottomRight}
      />
    </>,
  );

  yield* rect().rotation(10, 1).to(-10, 1);
});
```

## Flexbox configuration

Most flexbox attributes available in CSS are available as `Layout` properties. You can check out this Flexbox guide to better understand how they work. The most useful properties are listed below:

### `Layout.padding`

```
readonly public padding: SpacingSignalLayout
```

### `Layout.margin`

```
readonly public margin: SpacingSignalLayout
```

### `Layout.gap`

```
readonly public gap: Vector2LengthSignalLayout
```

### `Layout.direction`

```
readonly public direction: SimpleSignalFlexDirectionLayout
```

### `Layout.alignItems`

```
readonly public alignItems: SimpleSignalFlexItemsLayout
```

### `Layout.justifyContent`

```
readonly public justifyContent: SimpleSignalFlexContentLayout
```

## Groups

Nodes that don't extend the `Layout` class, such as the `Node` itself, are unaffected by the layout and are treated as if they were never there. This lets you apply filters and transformations to layout nodes without affecting the hierarchy.

From the layout's perspective, all `<Rect>`s in the example below are siblings:

```
<Layout direction={'column'} width={960} gap={40} layout>
  <Node opacity={0.1}>
    <Rect height={240} fill={'#ff6470'} />
    <Rect height={240} fill={'#ff6470'} />
  </Node>
  <Rect height={240} fill={'#ff6470'} />
</Layout>
```
