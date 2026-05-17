# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed

- Renamed the root mod **Stash Only Disassemble → Immersive Scraping**
  ("scraping" is the public feature name; "disassemble" stays only as the
  internal/engine technical term). Source file `stashOnlyDisassemble.reds` →
  `immersiveScraping.reds`; install dir `r6/scripts/stashOnlyDisassemble/` →
  `r6/scripts/immersiveScraping/`; release archives
  `stash-only-disassemble-*` → `immersive-scraping-*`. Internal classes
  (`DisassemblePolicy` / `DisassembleGate`) and game-engine identifiers are
  intentionally unchanged. The GitHub repository slug and the advisory/commit
  URLs that depend on it are a separate owner action and are updated later.

### Added

- Initial public release of the mod.
- `DisassemblePolicy` — central abstraction for the disassemble action name,
  hint label, eligibility check, and execution (with audio cue).
- `DisassembleGate` — static flag tracking whether the stash screen is open.
- Single wrap on `CraftingSystem.CanItemBeDisassembled` to block disassembly
  outside the stash, the patch-stable choke point every inventory screen hits.
- `FullscreenVendorGameController` wraps to surface the disassemble action,
  hint, and confirmation / quantity-picker flows in the stash UI.
- CI: sanity checks (UTF-8, conflict markers, indentation, brace balance,
  annotation allowlist) and `redscript-cli format` parse check.
- Release workflow: tag `v*` → builds the install ZIP and publishes a GitHub
  Release with auto-generated notes.
- Level/Tier Flatten module (Cyberpunk Realism, tranche 1) — standalone
  companion that neutralises RPG level + item-tier influence on damage with
  strict, structural NPC parity:
  - `LevelTierFlattenPolicy` — single source of truth for the flatten values
    (neutral level coefficient, neutral tier multiplier, scalar clamp helper).
  - `LevelTierFlattenGate` — static kill-switch (default on); every wrap falls
    through to vanilla `wrappedMethod(...)` when off (neutralise, not delete).
  - Split `levelTierFlatten_cp2077-{2x,1x}.reds` wraps on the shared
    `RPGManager` scaling-coefficient static (no player/NPC branch), mirroring
    the existing `handleStorageSlot_*` per-patch compat pattern.
  - CI presence check and release workflow extended with two new archives
    `level-tier-flatten-{version}-cp2077-{2x,1x}.zip`.
- UI Flatten module (Cyberpunk Realism, tranche 2 — cosmetic): stops the UI
  advertising level/tier so it matches the de-scaled damage numbers.
  - `UiFlattenPolicy` / `UiFlattenGate` — neutral colour quality + hidden-
    level text, default-on kill-switch with vanilla fallthrough.
  - `uiFlatten_cp2077-{2x,1x}.reds` — rarity-colour neutralisation at the
    quality→colour resolver (best-effort symbol; level-hiding sub-items
    tracked in PROGRESS rather than speculatively coded).
  - CI presence check extended with the three `uiFlatten*` files.
- Cyberpunk Realism suite moved into its own `cyberpunk-realism/` folder
  (code + docs), extractable cleanly; CI presence and release staging
  paths rewired accordingly.
- Suite documentation: `cyberpunk-realism/README.md` (vision + current
  state) and `cyberpunk-realism/PROGRESS.md` (actionable per-chantier
  tracker, in-progress and roadmap, with multi-mod split notes and merge
  policy).

[Unreleased]: https://github.com/adriendellagaspera/mod-stash-only-disassemble/commits/main
