# Realistic Components — progress & workstream tracker

Actionable state. Vision and locked decisions live in
[`README.md`](./README.md). This mod has a single workstream.

## Status legend

- `PLANNED` — scoped, not yet built.
- `SCOPE-SPIKE` — time-boxed investigation; deliverable is a decision.
- `BLOCKED` — cannot progress until a named blocker clears.
- `DONE` — shipped (data written + verified in a real install).

## RC1 — Component / crafting de-tiering

- **Status:** `PLANNED` (scope-spike done 2026-05-17 — surface decided).
- **Goal:** point every tiered crafting-component reference at one real,
  non-tiered component; make disassembly yield that same component.
- **Surface (decided):** **BUILD via TweakXL data, no redscript.** Components
  are `Items.*Material*` records; recipes reference them via
  `RecipeData` / `RecipeElement` ingredient entries. Rewrite each recipe's
  `RecipeElement` ingredients and the disassembly-yield records to the single
  real component. **Not harness-blocked** (pure data — can progress while
  Realistic Arsenal facets a/c stay blocked).
- **Why a separate mod (cascade refuted):** weapon quality (`Quality.*`
  stat-modifier records + `RPGManager`) and component tiers
  (`Items.*Material*` via `RecipeData`/`RecipeElement`) are **two independent
  TweakDB surfaces**. Overriding weapon `Quality.*` does nothing to recipe
  ingredients. This refutation of the "same surface" premise is exactly why
  component de-tiering was split out of Realistic Arsenal.
- **Build, not compose:** no mod de-tiers the component graph — those that
  touch crafting (Preem Weaponsmith, Enhanced Craft) *presuppose* tiers.
- **Main risk:** large recipe surface — every craftable recipe + every
  disassembly-yield record. A missed recipe leaks a tiered component. Needs
  an exhaustive recipe sweep (consider a generated YAML build step; runtime
  is still pure TweakXL data).
- **Confidence:** the "no mod already does this" gap holds at medium
  confidence (Nexus fetch is 403-blocked) — run the manual Nexus pass below
  before finalising.
- **Exit to `DONE`:** TweakXL YAML written; every recipe + disassembly record
  rerouted; in a real install, no tiered component appears in any
  recipe/disassembly; then add the release archive (deferred until now).

## Composition re-verification (planned · manual)

Crafting/component-mod verdicts in README Composition are search-snippet
level (Nexus 403). Confirm each on the real mod page / in a real install:

- [ ] 9692 Preem Weaponsmith — confirm it presupposes tiers and pulls
      redscript deps (so: adjacent customisation only, not composed for
      de-tiering).
- [ ] 4378 Enhanced Craft — confirm it scales component cost by tier
      (presupposes tiers; adjacent only).
- [ ] 16154 Immersive Crafting Access — −30% component cost; optional,
      tier-agnostic.
- [ ] 11880 Immersive Components — confirm the rejection: only renames tiered
      components, does NOT remove tiers.
- [ ] 22824 Immersive Crafting — restricts crafting to the stash (craft-side);
      adjacency to the Immersive Scraping mod (disassemble-side).

## Packaging

Deferred: no archive / CI presence entry until RC1 has real data files
(repo discipline — package only a module that exists). When ready, mirror
the per-mod folder/archive pattern (`realistic-components-*`).
