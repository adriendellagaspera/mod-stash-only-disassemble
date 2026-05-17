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
  intentionally unchanged.
- Renamed the GitHub repository `mod-stash-only-disassemble` →
  `cp2077-realism-mods` (umbrella slug: the repo now hosts three mods —
  Immersive Scraping, Realistic Arsenal and Realistic Components). Advisory
  and commit URLs in `SECURITY.md` / `CHANGELOG.md` recanonicalised to the
  new slug.
- Refocused the "Cyberpunk Realism" suite into **two sibling de-tiering
  mods**. A scope-spike (TweakDB patch 2.x) refuted the premise that weapon
  tiers and crafting-component tiers are the same data surface — they are two
  independent TweakDB surfaces (`Quality.*`/`RPGManager` vs
  `RecipeData`/`RecipeElement`) — so they are split:
  - **Realistic Arsenal** (weapons): the former suite folder
    `cyberpunk-realism/` → `realistic-arsenal/`; install dir
    `r6/scripts/levelTierFlatten/` → `r6/scripts/realisticArsenal/`; archives
    `level-tier-flatten-*` → `realistic-arsenal-*`. Weapon-condition decay
    composed (Weapon Conditioning), distinct from the deferred skill-decay
    workstream.
  - **Realistic Components** (crafting): new `realistic-components/` folder —
    de-tiers the recipe/disassembly graph via TweakXL data (planned; no data
    files / archive yet, packaged only when real).
  Preem Weaponsmith / Enhanced Craft reclassified as *adjacent customisation*
  mods (they presuppose tiers — not composed for de-tiering). Per-mod
  composition re-verification checklists live in each mod's PROGRESS.md.

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
- Realistic Arsenal — damage facet — standalone
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
    `realistic-arsenal-{version}-cp2077-{2x,1x}.zip`.
- Realistic Arsenal — UI facet (cosmetic): stops the UI
  advertising level/tier so it matches the de-scaled damage numbers.
  - `UiFlattenPolicy` / `UiFlattenGate` — neutral colour quality + hidden-
    level text, default-on kill-switch with vanilla fallthrough.
  - `uiFlatten_cp2077-{2x,1x}.reds` — rarity-colour neutralisation at the
    quality→colour resolver (best-effort symbol; level-hiding sub-items
    tracked in PROGRESS rather than speculatively coded).
  - CI presence check extended with the three `uiFlatten*` files.
- Realistic Arsenal lives in its own `realistic-arsenal/` folder
  (code + docs), extractable cleanly; CI presence and release staging
  paths rewired accordingly.
- Suite documentation: `realistic-arsenal/README.md` (vision + current
  state) and `realistic-arsenal/PROGRESS.md` (actionable per-workstream
  tracker, in-progress and roadmap, with multi-mod split notes and merge
  policy).

[Unreleased]: https://github.com/adriendellagaspera/cp2077-realism-mods/commits/main
