# Revideo Tweening API Documentation

## Overview

The tweening module from `@revideo/core/lib/tweening` provides "interpolation and timing of tweens" for animations.

## Interfaces

- `InterpolationFunction`
- `Spring`
- `TimingFunction`

## Spring Variables

Seven preset spring configurations are available:
- `BeatSpring`
- `BounceSpring`
- `JumpSpring`
- `PlopSpring`
- `SmoothSpring`
- `StrikeSpring`
- `SwingSpring`

## Core Tweening Functions

**Basic Tweens:**
- `tween()` - Animates over specified seconds with progress callbacks
- `spring()` - Uses spring physics with optional tolerance and callbacks

**Interpolation Functions:**
- `linear()` - Direct linear interpolation between values
- `deepLerp()` - Interpolates between Records/objects with mismatched keys
- `boolLerp()` - Interpolates between two values based on threshold
- `textLerp()` - Interpolates between strings
- `arcLerp()` - Arc-based interpolation returning Vector2

**Easing Functions:**

*Ease In variants:*
- `easeInBack`
- `easeInBounce`
- `easeInCirc`
- `easeInCubic`
- `easeInElastic`
- `easeInExpo`
- `easeInQuad`
- `easeInQuart`
- `easeInQuint`
- `easeInSine`

*Ease Out variants:*
- `easeOutBack`
- `easeOutBounce`
- `easeOutCirc`
- `easeOutCubic`
- `easeOutElastic`
- `easeOutExpo`
- `easeOutQuad`
- `easeOutQuart`
- `easeOutQuint`
- `easeOutSine`

*Ease InOut variants:*
- `easeInOutBack`
- `easeInOutBounce`
- `easeInOutCirc`
- `easeInOutCubic`
- `easeInOutElastic`
- `easeInOutExpo`
- `easeInOutQuad`
- `easeInOutQuart`
- `easeInOutQuint`
- `easeInOutSine`

**Custom Easing Creators:**
- `createEaseInBack(s)`
- `createEaseOutBack(s)`
- `createEaseInOutBack(s)`
- `createEaseInBounce(n, d)`
- `createEaseOutBounce(n, d)`
- `createEaseInOutBounce(n, d)`
- `createEaseInElastic(s)`
- `createEaseOutElastic(s)`
- `createEaseInOutElastic(s)`

**Utility Functions:**
- `clamp()` - Constrains value between min/max
- `clampRemap()` - Remaps value within constrained range
- `map()` - Maps value from one range to another
- `remap()` - Extended range mapping function
- `sin()` - Sine-based interpolation
- `cos()` - Cosine-based interpolation
- `makeSpring()` - Creates custom spring with mass, stiffness, damping, velocity
