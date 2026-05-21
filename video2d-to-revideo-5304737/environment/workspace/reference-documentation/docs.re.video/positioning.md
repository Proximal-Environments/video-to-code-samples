# Positioning

_Note: These docs were adopted from the original Motion Canvas docs_

Motion Canvas uses a Cartesian coordinate system. Its origin is located in the center of the scene, with the x-axis going to the right and the y-axis going down.

## Transform

All nodes are positioned relative to their parents. This means that any transformations applied to the parent are also applied to its children. The transform of each node consists of the following properties:

### `Node.position`

```
readonly public position: Vector2SignalNode
```

Represents the position of this node in local space of its parent.

### `Node.scale`

```
readonly public scale: Vector2SignalNode
```

Represents the scale of this node in local space of its parent.

### `Node.rotation`

```
readonly public rotation: SimpleSignalnumberNode
```

Represents the rotation (in degrees) of this node relative to its parent.

## Absolute transform

Each of the basic transform properties has a dedicated helper method that operates in world space.

This can be helpful, for instance, when we need to match the transforms of two nodes located within different parents. Consider the following example:

```typescript
const circleA = createRef<Node>();
const circleB = createRef<Node>();
view.add(
  <>
    <Node position={[200, 100]}>
      <Circle
        position={[0, 100]}
        ref={circleA}
        width={20}
        height={20}
        fill={'white'}
      />
    </Node>
    <Circle ref={circleB} width={10} height={10} fill={'red'} />
  </>,
);
circleB().absolutePosition(circleA().absolutePosition());
```

We access the absolute position (position in world space) of `circleA` and assign it as the absolute position of `circleB`. This will move the `circleB` right on top of `circleA`.

**Note:** We still need to set the `absolutePosition` of `circleB` and not just the `position`. It may seem redundant since `circleB` is a direct child of the scene view. But the local space of the scene view is not the same as the world space.

### `Node.absolutePosition`

```
readonly public absolutePosition: SimpleVector2SignalNode
```

A helper signal for operating on the position in world space.

Retrieving the position using this signal returns the position in world space. Similarly, setting the position using this signal transforms the new value to local space.

If the new value is a function, the position of this node will be continuously updated to always match the position returned by the function. This can be useful to "pin" the node in a specific place or to make it follow another node's position.

Unlike `position`, this signal is not compound - it doesn't contain separate signals for the `x` and `y` components.

### `Node.absoluteScale`

```
readonly public absoluteScale: SimpleVector2SignalNode
```

A helper signal for operating on the scale in world space.

Retrieving the scale using this signal returns the scale in world space. Similarly, setting the scale using this signal transforms the new value to local space.

If the new value is a function, the scale of this node will be continuously updated to always match the position returned by the function.

Unlike `scale`, this signal is not compound - it doesn't contain separate signals for the `x` and `y` components.

### `Node.absoluteRotation`

```
readonly public absoluteRotation: SimpleSignalnumberNode
```

A helper signal for operating on the rotation in world space.

Retrieving the rotation using this signal returns the rotation in world space. Similarly, setting the rotation using this signal transforms the new value to local space.

If the new value is a function, the rotation of this node will be continuously updated to always match the rotation returned by the function.

## Matrices

For more advanced uses, nodes expose all the matrices necessary to map vectors from one space to another. For example, the helper properties described above could be reimplemented using the `worldToParent` and `localToWorld` matrices:

```typescript
// getting the absolute position:
node.absolutePosition();
// same as:
Vector2.zero.transformAsPoint(node.localToWorld());
// setting the absolute position:
node.absolutePosition(vector);
// same as:
node.position(vector.transformAsPoint(node.worldToParent()));
```

The available matrices include:

### `Node.localToWorld`

```
public localToWorld(): DOMMatrix
```

Get the local-to-world matrix for this node. This matrix transforms vectors from local space of this node to world space.

### `Node.worldToLocal`

```
public worldToLocal(): DOMMatrix
```

Get the world-to-local matrix for this node. This matrix transforms vectors from world space to local space of this node.

### `Node.localToParent`

```
public localToParent(): DOMMatrix
```

Get the local-to-parent matrix for this node. This matrix transforms vectors from local space of this node to local space of this node's parent.

### `Node.worldToParent`

```
public worldToParent(): DOMMatrix
```

Get the world-to-parent matrix for this node. This matrix transforms vectors from world space to local space of this node's parent.
