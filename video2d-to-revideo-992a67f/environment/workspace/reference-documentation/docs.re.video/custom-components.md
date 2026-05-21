# Custom Components

Components are classes like `Rect` and `Circle` that abstract rendering and data functionality into reusable, modular pieces. To use a component in a scene, add it to the view and provide arguments to the component.

```
<Switch initialState={false} />
```

## Defining Props

To define what arguments a component will take, first define an interface. All properties of the interface must be wrapped in `SignalValue<>`:

```
export interface SwitchProps extends NodeProps {
  initialState?: SignalValue<boolean>;
  accent?: SignalValue<PossibleColor>;
}
```

## Creating the Component Class

Create a class for your components. The component class must extend `Node` or one of its subclasses.

```
export interface SwitchProps extends NodeProps {
  // properties
}

export class Switch extends Node {
  // implementation
}
```

## Using Properties

To use the properties defined in the interface, your class must contain a property with the same name. Motion Canvas provides type decorators like `@initial()` and `@signal()`:

```
export class Switch extends Node {
  @initial(false)
  @signal()
  public declare readonly initialState: SimpleSignal<boolean, this>;

  @initial('#68ABDF')
  @colorSignal()
  public declare readonly accent: ColorSignal<this>;
}
```

Colors are wrapped in `ColorSignal<>` while other types are wrapped in `SimpleSignal<>`. Properties must be initialised with the `public`, `declare` and `readonly` keywords.

## Adding Elements to the View

Add elements to the view by using `this.add()`:

```
export class Switch extends Node {
  public constructor(props?: SwitchProps) {
    super({...props});
    this.add(
      <Rect>
        <Circle />
      </Rect>,
    );
  }
}
```

## Adding Methods

Since this is a class, you can add methods for animating a component:

```
export class Switch extends Node {
  public *toggle(duration: number) {
    yield* all(
      tween(duration, value => {
        // ...
      }),
      tween(duration, value => {
        // ...
      }),
    );
    this.isOn = !this.isOn;
  }
}
```

## Complete Example

```typescript
import {
  Circle,
  Node,
  NodeProps,
  Rect,
  colorSignal,
  initial,
  signal,
} from '@revideo/2d';
import {
  Color,
  ColorSignal,
  PossibleColor,
  SignalValue,
  SimpleSignal,
  all,
  createRef,
  createSignal,
  easeInOutCubic,
  tween,
} from '@revideo/core';

export interface SwitchProps extends NodeProps {
  initialState?: SignalValue<boolean>;
  accent?: SignalValue<PossibleColor>;
}

export class Switch extends Node {
  @initial(false)
  @signal()
  public declare readonly initialState: SimpleSignal<boolean, this>;

  @initial('#68ABDF')
  @colorSignal()
  public declare readonly accent: ColorSignal<this>;

  private isOn: boolean;
  private readonly indicatorPosition = createSignal(0);
  private readonly offColor = new Color('#242424');
  private readonly indicator = createRef<Circle>();
  private readonly container = createRef<Rect>();

  public constructor(props?: SwitchProps) {
    super({...props});

    this.isOn = this.initialState();
    this.indicatorPosition(this.isOn ? 50 : -50);

    this.add(
      <Rect
        ref={this.container}
        fill={this.isOn ? this.accent() : this.offColor}
        size={[200, 100]}
        radius={100}
      >
        <Circle
          x={() => this.indicatorPosition()}
          ref={this.indicator}
          size={[80, 80]}
          fill="#ffffff"
        />
      </Rect>,
    );
  }

  public *toggle(duration: number) {
    yield* all(
      tween(duration, value => {
        const oldColor = this.isOn ? this.accent() : this.offColor;
        const newColor = this.isOn ? this.offColor : this.accent();
        this.container().fill(
          Color.lerp(oldColor, newColor, easeInOutCubic(value)),
        );
      }),
      tween(duration, value => {
        const currentPos = this.indicator().position();
        this.indicatorPosition(
          easeInOutCubic(value, currentPos.x, this.isOn ? -50 : 50),
        );
      }),
    );
    this.isOn = !this.isOn;
  }
}
```
