# Stash Only Disassemble

A small Cyberpunk 2077 mod that confines item disassembly to the stash screen.

## What it does

- Adds the **Disassemble** action to items shown in the stash UI (V's apartment, safehouses, etc.).
- Disables disassembly everywhere else (inventory, backpack, vendors) by gating
  `CraftingSystem.CanItemBeDisassembled` on whether the stash is currently open.

The result: you can't accidentally break down an item from your active inventory,
but the stash becomes your dedicated salvage bench.

## Requirements

- **Cyberpunk 2077 Patch 2.0 or later** (September 2023, Phantom Liberty overhaul).
  The mod targets `CraftingSystem.CanItemBeDisassembled` and
  `FullscreenVendorGameController` as they exist in the 2.x game scripts.
  Compatibility with Patch 1.x is not guaranteed.
- [redscript](https://github.com/jac3km4/redscript) v0.5.x or later (usually
  installed via [RED4ext](https://github.com/WopsS/RED4ext) or a mod manager
  like Vortex).

## Version compatibility

| Game patch | Status |
|---|---|
| 2.0 and later | Supported and tested |
| 1.x (pre–Phantom Liberty) | Not guaranteed — game API surface differs |

CI validates syntax against the redscript v1.0.0-preview parser series
(preview5, preview.14, preview.22). The v0.5.x stable compiler used by current
game releases cannot be exercised in CI without the game bundle, so in-game
manual testing covers that path.

## Installation

1. Install redscript if you don't have it already.
2. Copy `stashOnlyDisassemble.reds` into:
   ```
   <Cyberpunk 2077>/r6/scripts/stashOnlyDisassemble/
   ```
3. Launch the game. redscript will compile the script on startup; check
   `r6/cache/redscript.log` if anything goes wrong.

## Uninstall

Delete the folder you created in step 2 and restart the game.

## How it works

Two small pieces of state cooperate:

- `DisassembleGate` — a static `Bool` flipped on/off in
  `FullscreenVendorGameController.OnInitialize` / `OnUninitialize` whenever a stash
  screen opens or closes.
- `DisassemblePolicy` — owns the action name, hint label, and the
  "is this item disassemblable" check, so controllers don't duplicate that logic.

The core blocker is a single wrap on `CraftingSystem.CanItemBeDisassembled` — the
canonical gate every inventory screen consults before showing the disassemble hint
or running the action. Wrapping it once is more patch-stable than chasing every
UI controller individually.
