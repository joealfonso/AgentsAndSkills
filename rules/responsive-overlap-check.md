# UI: check layouts at every width before calling it done

Paste into a front-end project's CLAUDE.md.

```markdown
## Layout verification

After every UI or CSS change, check the layout in a browser at 320, 360, 390, 430, 768 and 1280px before saying the work is done. Check every screen or component you touched, scrolled to the bottom as well.

- Never judge a layout from one screenshot at one width.
- Prefer elements in the normal flow (they wrap) over absolute positioning near text.
- When something overlaps, decide whether it's a real collision or intentional (content scrolling under a fixed bar) and fix the real ones.
- Say in the wrap-up which widths were checked.
```

**Why:** an absolutely positioned label landed on top of a counter at phone width. It looked fine in a single desktop-width preview and was only caught on a real phone.
