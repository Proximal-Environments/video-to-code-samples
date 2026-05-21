# Filters and Effects

*Note: These docs were adopted from the original [Motion Canvas](https://motioncanvas.io/docs/) docs*

Because Motion Canvas is built on top of the Browser's 2D Rendering Context, we can make use of several canvas operations that are provided by the Browser.

## Filters

Filters let you apply various effects to your nodes. You can find all available filters on [MDN](https://developer.mozilla.org/en-US/docs/Web/API/CanvasRenderingContext2D/filter).

Every node has a `filters` property containing an array of filters that will be applied to the node. You can declare this array yourself, or use the `filters` property to configure individual filters.

### Using the Filters Property

Individual filters don't need to be initialized. If a filter you set doesn't exist, it will be automatically created and added to the list of filters. If you have multiple filters of the same type, accessing the property will only modify the first instance (you can use the array method for more control).

```typescript
yield* iconRef().filters.blur(10, 1);
yield* iconRef().filters.blur(0, 1);
```

### Important Notes on Filter Order

The order in which you apply effects matters. Different sequences of the same filters produce different visual results depending on which filter is applied first.

> Some filters, like `opacity` and `drop-shadow`, have their own dedicated properties directly on the `Node` class.

## Masking and Composite Operations

Composite operations define how the thing we draw (source) interacts with what is already on the canvas (destination). This allows us to define complex masks. MDN has [comprehensive visualizations of all available composite operations](https://developer.mozilla.org/en-US/docs/Web/API/CanvasRenderingContext2D/globalCompositeOperation#operations).

### How Masking Works

You can create a mask by treating one node as the "masking" or "stencil" layer, and another node as the "value" layer. The mask layer defines whether the value layer will be visible or not. The value layer will be what's actually visible in the end.

### Available Composite Operations for Masking

Any of the following composite operations can be used to create a mask:
- `source-in`
- `source-out`
- `destination-in`
- `destination-out`

There is also a `xor` operation which can be helpful if you want two value layers that hide each other on overlap.

## Cached Nodes

Both filters and composite operations require a cached `Node`. Filters can set it automatically, while composite operations require you to set it explicitly on an ancestor `Node` (usually the parent node).

A cached `Node` and its children are rendered on an offscreen canvas first, before getting added to the main scene. For filters this is needed because they are applied to the entire canvas. By creating a new canvas and moving the elements that should get affected by the filters over, applying filters to the entire "new" canvas, and then moving back the result, you effectively only apply the filters to the moved elements.

### Enabling Cache

To turn a `Node` into a cached node, simply pass the `cache` property:

```typescript
<Node cache>...</Node>
// or
<Node cache={true}>...</Node>
```

All components inherit from `Node`, so you can set the cache on all of them.
