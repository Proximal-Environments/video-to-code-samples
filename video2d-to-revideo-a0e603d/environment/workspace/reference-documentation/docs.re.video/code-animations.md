# Code Animations

### Overview

The [`Code`](/api/2d/components/Code) node displays code snippets with syntax highlighting and animation capabilities.

### Parsing and Highlighting

The default highlighter uses Lezer to parse and highlight code, but requires language grammars. To set up JavaScript highlighting:

```bash
npm i @lezer/javascript
```

Then configure in your project:

```typescript
import {makeProject} from '@revideo/core';
import example from './scenes/example?scene';
import {Code, LezerHighlighter} from '@revideo/2d';
import {parser} from '@lezer/javascript';

Code.defaultHighlighter = new LezerHighlighter(parser);

export default makeProject({
  scenes: [example],
});
```

Enable JSX and TypeScript support via dialects:

```typescript
Code.defaultHighlighter = new LezerHighlighter(
  parser.configure({
    dialect: 'jsx ts',
  }),
);
```

### Defining Code

Set code via the `code` property using strings or template strings:

```typescript
view.add(
  <Code
    fontSize={28}
    code={'const number = 7;'}
  />,
);
```

Use backticks for multi-line snippets. A leading backslash escapes the first newline:

```typescript
view.add(
  <Code
    fontSize={28}
    code={`\
function example() {
  const number = 7;
}`}
  />,
);
```

### Using Signals

Template strings evaluate signals immediately and won't update. Use the `CODE` tag function instead:

```typescript
const nameSignal = Code.createSignal('number');
view.add(
  <Code
    fontSize={28}
    code={CODE`const ${nameSignal} = 7;`}
  />,
);

yield* waitFor(1);
nameSignal('newValue'); // Updates the snippet
```

### Animating Code

#### Diffing

Tween the `code` property to use the patience diff algorithm:

```typescript
yield* code().code('const nine = 9;', 0.6);
```

#### append and prepend

Add code at the beginning or end:

```typescript
code().code.append(`const one = 1;`);
yield* code().code.append('\nconst two = 2;', 0.6);
yield* code().code.append(0.6)`const three = 3;`;
yield* code().code.prepend('// example\n', 0.6);
```

#### insert, replace, and remove

Modify code at specific points using code ranges:

```typescript
yield* code().code.insert([2, 0], '  return 7;\n', 0.6);
yield* code().code.replace(word(1, 15, 6), 'Goodbye!', 0.6);
yield* code().code.remove(lines(2), 0.6);

yield* all(
  code().code.replace(word(0, 9, 7), 'greet', 0.6),
  code().code.replace(word(1, 15, 8), 'Hello!', 0.6),
);
```

#### edit

Define changes visually using helper functions in a template string:

```typescript
yield* code().code.edit(0.6)`\
function example() {
  ${insert(`// This is a comment
  `)}console.log("${replace('Hello!', 'Goodbye!')}");${remove(`
  return 7;`)}
}`;
```

### Code Ranges

A CodeRange specifies a character span using line and column numbers (both zero-based):

```typescript
[[startLine, startColumn], [endLine, endColumn]];

// First three characters of line 1
[[1, 0], [1, 3]];
```

Helper functions create common ranges:

```typescript
// 3 characters starting at line 1, column 3
word(1, 3, 3);

// From line 1, column 3 to end of line
word(1, 3);

// Lines 1 to 3 inclusive
lines(1, 3);

// Line 2 only
lines(2);
```

Find ranges in code using search methods:

```typescript
yield* code().code.replace(
  code().findFirstRange('example'),
  'greet',
  0.6,
);
```

Available methods: `findFirstRange`, `findAllRanges`, `findLastRange`.

### Code Selection

Highlight specific code portions via the `selection` property:

```typescript
// Select all instances (case-insensitive)
yield* code().selection(code().findAllRanges(/hello/gi), 0.6);

// Select line 1
yield* code().selection(lines(1), 0.6);

// Reset selection
yield* code().selection(DEFAULT, 0.6);
```

### Custom Themes

Pass a custom `HighlightStyle` to LezerHighlighter:

```typescript
import {Code, LezerHighlighter} from '@revideo/2d';
import {HighlightStyle} from '@codemirror/language';
import {tags} from '@lezer/highlight';
import {parser} from '@lezer/javascript';

const MyStyle = HighlightStyle.define([
  {tag: tags.keyword, color: 'red'},
  {tag: tags.function(tags.variableName), color: 'yellow'},
  {tag: tags.number, color: 'blue'},
  {tag: tags.string, color: 'green'},
]);

Code.defaultHighlighter = new LezerHighlighter(parser, MyStyle);
```

### Multiple Languages

Override the default highlighter per node:

```typescript
import {Code, LezerHighlighter} from '@revideo/2d';
import {parser} from '@lezer/rust';

const RustHighlighter = new LezerHighlighter(parser);

view.add(
  <Code
    highlighter={RustHighlighter}
    code={`fn hello() {
  println!("Hello!");
}`}
  />,
);
```

Create reusable custom components:

```typescript
import {Code, LezerHighlighter, withDefaults} from '@revideo/2d';
import {parser} from '@lezer/rust';

const RustHighlighter = new LezerHighlighter(parser);
export const RustCode = withDefaults(Code, {
  highlighter: RustHighlighter,
});
```
