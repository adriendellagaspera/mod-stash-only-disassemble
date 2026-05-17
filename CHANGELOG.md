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
  `cp2077-realism-mods` (umbrella slug: the repo now hosts two mods —
  Immersive Scraping and Realistic Arsenal). Advisory and commit URLs in
  `SECURITY.md` / `CHANGELOG.md` recanonicalised to the new slug.
- Renamed and refocused the "Cyberpunk Realism" suite into a single mod
  **Realistic Arsenal**. The separate weapon-identity and crafting tracks are
  merged under one thesis (*the tier scale is meaningless; a weapon is a weapon,
  built and maintained from real non-tiered components*), since removing weapon
  tiers and removing component tiers are the same data surface. Folder
  `cyberpunk-realism/` → `realistic-arsenal/`; install dir
  `r6/scripts/levelTierFlatten/` → `r6/scripts/realisticArsenal/`; archives
  `level-tier-flatten-*` → `realistic-arsenal-*`. Weapon-condition decay is now
  composed (Weapon Conditioning), distinct from the deferred skill-decay
  workstream. The composed-vs-built rationale and confidence caveat live in
  the suite README; the per-mod re-verification checklist in PROGRESS.md.

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
