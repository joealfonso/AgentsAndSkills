# Data: remove features you can't make reliable

Paste into CLAUDE.md for data-driven products.

```markdown
## Unreliable features

Audit a derived feature before trusting it. If its data can't be made reliable, remove it completely (code, data files, scripts, README) and say so. Don't leave it in with a warning. When the feature is the core of the product, fix the data instead.
```

**Why:** a skeptical audit found a time-travel slider that read zero for a quarter of its range (a swallowed fetch error) and a migration view that tracked observers instead of animals. Both were removed, while the core range data was fixed because the product depends on it.
