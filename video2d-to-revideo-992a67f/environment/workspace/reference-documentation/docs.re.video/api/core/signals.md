# Signals Module Documentation

The signals module from `@revideo/core` provides "value wrappers for easy dependency tracking and cache invalidation."

## Key Components

**Classes:** CompoundSignalContext, ComputedContext, DependencyContext, and SignalContext manage signal state and dependencies.

**Interfaces:** Signal, Computed, PromiseHandle, SignalExtensions, SignalGetter, SignalSetter, and SignalTween define the contract for reactive values.

## Primary Functions

`createSignal()` initializes a reactive value with optional interpolation and ownership tracking.

```typescript
createSignal<TValue>(
  initial?: SignalValue<TValue>,
  interpolation?: InterpolationFunction<TValue>,
  owner?: TOwner
): SimpleSignal<TValue>
```

`createComputed()` establishes derived values based on a factory function.

```typescript
createComputed<TValue>(
  factory: (...args: any[]) => TValue,
  owner?: any
): Computed<TValue>
```

`createComputedAsync()` handles promise-based computations with initial values.

```typescript
createComputedAsync<T>(
  factory: () => Promise<T>
): Computed<T | null>
```

Additional utilities include:
- `unwrap()` - extracts the current value from a signal
- `isReactive()` - tests whether a value is a reactive signal
- `modify()` - transforms signal values through custom modification functions

## Type System

`SignalValue<T>` represents either a raw value or a function returning that value. `SimpleSignal` provides basic signal functionality with optional return types. `CompoundSignal` creates multi-property signals with selective key tracking, while `SignalGenerator` enables animation sequences with timing, interpolation, and threading capabilities.
