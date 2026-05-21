# Experimental Features

Motion Canvas adheres to the [semver](https://semver.org/) versioning scheme, which guarantees backward compatibility within the same major version. For instance, code written with `v3.2.0` will function properly with subsequent releases like `v3.2.1`, `v3.3.0`, or `v3.4.0`.

However, experimental features operate under different rules. These features can change at any moment and potentially disrupt your animations. They exist primarily for testing and gathering user feedback.

### Identifying Experimental Features

Throughout the documentation, experimental capabilities are identified with warning labels.

### Enabling Experimental Features

To utilize experimental features in your project, activate them in your project configuration file:

```typescript
// project.ts
export default makeProject({
  experimentalFeatures: true,
  // ...
});
```
