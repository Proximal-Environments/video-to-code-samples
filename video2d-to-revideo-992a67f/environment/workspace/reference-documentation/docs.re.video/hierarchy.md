# Scene Hierarchy

*Note: These docs were adopted from the original Motion Canvas docs*

## Overview

Scenes are collections of nodes displayed in animations, organized in a tree hierarchy with the scene view at its root -- a structure comparable to the Document Object Model used in HTML and XML.

## Creating Scene Hierarchies

Motion Canvas uses a custom JSX runtime to make code more readable. Rather than instantiating nodes directly, developers can write XML-like markup. Importantly, Motion Canvas does not use React; there is no virtual DOM or reconciliation. JSX tags map directly to Node instances.

### Example Markup:
```
view.add(
  <>
    <Circle />
    <Layout>
      <Rect />
      <Txt>Hi</Txt>
    </Layout>
  </>,
);
```

This is equivalent to the non-JSX version:
```
view.add([
  new Circle({}),
  new Layout({
    children: [
      new Rect({}),
      new Txt({text: 'Hi'}),
    ],
  }),
]);
```

## Modifying the Hierarchy

After creation, nodes can be added, removed, and rearranged using helper methods on the `Node` class:

### `Node.add`
Appends given node(s) as children at the end of the list.

### `Node.insert`
Inserts given node(s) at a specified index in the children list.

### `Node.remove`
Removes a node from the tree.

### `Node.reparent`
Changes a node's parent while maintaining its absolute transform position.

### Movement Methods
- **`Node.moveUp`**: Exchanges places with the sibling above
- **`Node.moveDown`**: Exchanges places with the sibling below
- **`Node.moveToTop`**: Places node at the end of children list (renders on top)
- **`Node.moveToBottom`**: Places node at the beginning (renders below all siblings)
- **`Node.moveTo`**: Moves node to a specific position relative to siblings
- **`Node.moveAbove`**: Moves node above a provided sibling
- **`Node.moveBelow`**: Moves node below a provided sibling
- **`Node.removeChildren`**: Removes all children

## Querying the Hierarchy

The `findAll` method searches through descendants using predicates. For example, to find all text nodes:

```
const texts = view.findAll(is(Txt));
```

Predicates can be custom functions:
```
const wideNodes = view.findAll(node => node.scale.x() > 1);
```

### Query Methods

- **`Node.findAll`**: Returns all descendants matching a predicate
- **`Node.findFirst`**: Returns the first descendant matching a predicate
- **`Node.findLast`**: Returns the last descendant matching a predicate
- **`Node.findAncestor`**: Returns the closest ancestor matching a predicate

These methods support the built-in `is()` utility function for type-based queries.
