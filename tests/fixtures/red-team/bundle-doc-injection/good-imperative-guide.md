# Patterns reference

Read this before changing the build. It is dense with instructions on purpose —
that is what a reference document is.

## Rules

- **Always** run the full suite before pushing. Never push on a red build.
- Do not add a dependency for something the standard library already does.
- Prefer the smallest change that works. Delete before you add.
- You must update the changelog in the same commit.

## Installing the toolchain

```bash
curl -fsSL https://get.example.dev/install.sh | sh
rustup component add clippy
```

## When something fails

Ignore the first warning from the linter about generated files; it is expected
and the config silences it in CI. Follow the stack trace to the first frame in
your own code, then work outwards.

## Checklist

1. Run the tests.
2. Update the docs.
3. Tell the reviewer what you changed and why.
