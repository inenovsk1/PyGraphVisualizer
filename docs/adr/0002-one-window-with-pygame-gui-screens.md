# One window that switches between a pygame_gui Menu and the Board

The app used to open a single window onto one Board, with the Algorithm and Board size fixed by the command line. Choosing a Config and being offered a next Session now happen inside the app. We keep one OS window and switch what it shows (the Menu or a Session), and build the Menu and the Prompt with `pygame_gui`.

Opening the Board in a second OS window (`pygame.Window`) was rejected: in fullscreen mode two windows would fight over the display, and the Menu would have to stay alive and in sync beside every Session. `pygame_gui` was chosen over hand-drawn buttons because the Menu is expected to grow (more Config options, other screens), and text entry, dropdowns and focus handling are the parts that are tedious to hand-roll.

## Consequences

- `pygame_gui` becomes a runtime dependency alongside `pygame-ce`.
- The Board still fills the whole window and is drawn by `BoardView`; `pygame_gui` is used only for the Menu and the Prompt.
- Board size limits, Speed levels and the `Config` live in a pygame-free module so they stay unit-testable, as in ADR-0001.
- Anything that wants a separate window later (a side-by-side comparison of two Algorithms, say) must revisit this decision.
