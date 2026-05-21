# Latex Component Documentation

## Overview

The `Latex` class is a node for rendering mathematical equations using LaTeX. It extends the `Img` component.

## Constructor

```typescript
public override new Latex(props: LatexProps): Latex
```

## Key Properties

### `tex`
```typescript
readonly public tex: SimpleSignal<string, Latex>
```
The LaTeX string to render as a mathematical equation.

### `options`
```typescript
readonly public options: SimpleSignal<OptionList, Latex>
```
Configuration options for LaTeX rendering.

### Inherited Properties

All Img properties: position, transform, size, appearance, layout, curve, effects.

## Example Usage

```typescript
import ...
export default makeScene2D(function* (view) {
  view.add(
    <Latex
      tex="{\color{white} ax^2+bx+c=0 \implies x=\frac{-b \pm \sqrt{b^2-4ac}}{2a}}"
      width={600}
    />,
  );
});
```
