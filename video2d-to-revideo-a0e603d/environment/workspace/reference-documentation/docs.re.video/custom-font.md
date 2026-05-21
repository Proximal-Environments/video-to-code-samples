# Custom font

*Note: These docs were adopted from the original [Motion Canvas](https://motioncanvas.io/docs/) docs*

## Loading fonts from the web

To use a font from hosters like Google Fonts, first create a CSS file under `src`:

```
root
└─src
  ├─scenes/
  ├─revideo.d.ts
  ├─project.meta
  ├─project.ts
  └─global.css
```

Inside `global.css`, import the font using `@import url(your link)`:

```css
@import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;700&display=swap');
```

Then, in `project.ts`, import the CSS file:

```typescript
import {makeProject} from '@revideo/core';
import example from './scenes/example?scene';
import './global.css'; // <- import the css

export default makeProject({
  scenes: [example],
});
```

Now you can reference the fonts in the `fontFamily` property in this project:

```jsx
<Txt fontFamily={'Fira Code'}>Fira Code</Txt>
```

## Loading fonts from local

For local fonts, make a directory `fonts` and put your font inside it:

```
root
└─public
  └─fonts
    └─CASCADIACODE.TTF
```

Inside `global.css`, import the font using `@font-face`:

```css
@import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;700&display=swap');

@font-face {
  font-family: 'Cascadia Code';
  src:
    local('Cascadia Code'),
    url(public/fonts/CASCADIACODE.TTF) format('truetype');
}
```

The font name will match the string in `@font-face/font-family` from the CSS:

```jsx
<Layout direction={'column'} alignItems={'center'} layout>
  <Txt fontFamily={'Fira Code'}>Fira Code</Txt>
  <Txt fontFamily={'Cascadia Code'}>Cascadia Code</Txt>
</Layout>
```
