# Algorithms yield Steps and do not touch pygame

Algorithms were blocking functions that mutated Node colors, called a render callback, and polled pygame for `QUIT` themselves, so they could not be tested without a display and froze the app's own event loop during a Search. Each Algorithm is now a pure Python generator that yields Steps; only the app module imports pygame and consumes one Step per frame.

## Consequences

- Algorithms are unit-testable headlessly, which is what makes the test suite and `pytest` without a display possible.
- The window stays responsive during a Search, so `QUIT`/`ESC` is handled in one place instead of inside each Algorithm.
- Anyone adding an Algorithm must yield Steps rather than draw; resist the urge to call pygame from `algorithms/`.
