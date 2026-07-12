# Contributing

Thank you for your interest in Obsyx.

The project prioritizes quality, maintainability, and consistency over rapid feature additions.

---

## Philosophy

Every contribution should improve at least one of the following:

- Readability
- Performance
- Consistency
- Maintainability
- User experience

---

## Architecture

Obsyx follows a modular design.

```
Core
 ↓
Environment
 ↓
Appearance
 ↓
Layouts
 ↓
Rules
 ↓
Interaction
 ↓
Runtime
```

Each module should have a clearly defined responsibility.

Avoid large configuration files containing unrelated functionality.

---

## Coding Style

- Keep functions focused.
- Avoid duplicated configuration.
- Prefer reusable abstractions.
- Group related functionality together.
- Document non-obvious decisions.

---

## Before Opening a Pull Request

- Test on a clean configuration.
- Ensure formatting is consistent.
- Remove experimental code.
- Update documentation if behavior changes.

---

## Reporting Issues

Please include:

- Distribution
- Kernel
- Hyprland version
- GPU
- Steps to reproduce
- Relevant logs

---

The goal of Obsyx is not to become the largest Hyprland configuration, but one of the most maintainable.