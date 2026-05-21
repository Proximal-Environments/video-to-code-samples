# Flow | Revideo API Documentation

The `flow` module from `@revideo/core/lib/flow` provides utilities for controlling animation timing and execution.

## Interfaces

- `EveryCallback`
- `EveryTimer`
- `LoopCallback`

## Functions

**all(...tasks)** - Executes multiple tasks concurrently, waiting for all to complete.

**any(...tasks)** - Runs concurrent tasks and resolves when any one finishes.

**chain(...tasks)** - Executes tasks sequentially, one after another.

**delay(time, task)** - Defers task execution by a specified duration in seconds.

**every(interval, callback)** - "Call the given callback every N seconds."

**loop(factory)** / **loop(iterations, factory)** - Repeatedly executes a generator. Iterations complete before the next begins. Cannot finish on its own; use `yield` or `spawn` for concurrent operation.

**loopFor(seconds, factory)** - Runs a generator loop for a specified duration. Allows iterations to finish even when time expires.

**loopUntil(event, factory)** - Executes generator loop until a named time event occurs.

**noop()** - Performs no operation.

**run(runner)** / **run(name, runner)** - "Turn the given generator function into a task."

**sequence(delay, ...tasks)** - Starts tasks sequentially with consistent spacing between launches (doesn't wait for previous task completion).

**waitFor(seconds, after?)** - Pauses execution for a specified duration with optional follow-up task.

**waitUntil(event, after?)** - "Wait until the given time event." Time events display on the timeline and are editable.

## Detailed Signatures

```typescript
all(...tasks: ThreadGenerator[]): ThreadGenerator
```
Run all tasks concurrently and wait for all of them to finish.

```typescript
any(...tasks: ThreadGenerator[]): ThreadGenerator
```
Run all tasks concurrently and wait for any of them to finish.

```typescript
chain(...tasks: Callback[ThreadGenerator][]): ThreadGenerator
```
Run tasks one after another.

```typescript
delay(time: number, task: Callback[ThreadGenerator]): ThreadGenerator
```
Run the given generator or callback after a specific amount of time.

```typescript
every(interval: number, callback: EveryCallback): EveryTimer
```
Call the given callback every N seconds.

```typescript
loop(factory: LoopCallback): ThreadGenerator
loop(iterations: number, factory: LoopCallback): ThreadGenerator
```
Run the given generator in a loop.

```typescript
loopFor(seconds: number, factory: LoopCallback): ThreadGenerator
```
Run a generator in a loop for the given amount of time.

```typescript
loopUntil(event: string, factory: LoopCallback): ThreadGenerator
```
Run a generator in a loop until the given time event.

```typescript
noop(): ThreadGenerator
```
Do nothing.

```typescript
run(runner: () => ThreadGenerator): ThreadGenerator
```
Turn the given generator function into a task.

```typescript
sequence(delay: number, ...tasks: ThreadGenerator[]): ThreadGenerator
```
Start all tasks one after another with a constant delay between.

```typescript
waitFor(seconds: number = 0, after?: ThreadGenerator): ThreadGenerator
```
Wait for the given amount of time.

```typescript
waitUntil(event: string, after?: ThreadGenerator): ThreadGenerator
```
Wait until the given time event.
