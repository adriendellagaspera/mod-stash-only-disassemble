# Realistic Components — overview

> Vision and locked decisions. For the actionable workstream tracker (status,
> surface, risks, composition checklist), see [`PROGRESS.md`](./PROGRESS.md).

Sibling of [Realistic Arsenal](../realistic-arsenal/README.md). Split out from
it once the scope-spike refuted the premise that weapon tiers and
crafting-component tiers are the same data surface — they are **two
independent TweakDB surfaces**, so they are two mods.

## Vision

Crafting components are abstract tier props: "Common / Uncommon / Rare / Epic /
Legendary component". They exist only to gate recipes behind a rarity ladder.
**A component is a real thing** — scrap, electronics, polymer, gun parts — not
a colour-coded tier. Realistic Components points every tiered component
reference at a single real, non-tiered component, so crafting and disassembly
trade in materials, not in a hidden ladder.

It is the **consumer side** of [Immersive Scraping](../README.md): scrapping
yields real components; this mod makes recipes and disassembly speak that same
real-component language instead of the vanilla tier props.

## How it works (decided by the scope-spike)

- **BUILD via TweakXL data — no redscript.** Crafting components are their own
  `Items.*Material*` records; recipes reference them through
  `RecipeData` / `RecipeElement` ingredient entries. The mod rewrites each
  recipe's `RecipeElement` ingredients and the disassembly-yield records to
  the single real component.
- Because it is pure data, the mod is **not** blocked on the in-game
  redscript symbol-verification harness (unlike Realistic Arsenal facets a/c).
- It is a **separate edit** from weapon de-tiering: overriding weapon
  `Quality.*` records does nothing to recipe ingredients. That independence
  is the whole reason this is its own mod.

## Composition

Provisional — Nexus is not auto-fetchable (HTTP 403); verdicts are
search-snippet level until re-verified (checklist in [`PROGRESS.md`](./PROGRESS.md)).

- **Adjacent customisation (NOT for de-tiering):**
  [Preem Weaponsmith](https://www.nexusmods.com/cyberpunk2077/mods/9692) and
  [Enhanced Craft](https://www.nexusmods.com/cyberpunk2077/mods/4378) add real
  modules / presets, but they **presuppose tiers** (Enhanced Craft multiplies
  component cost by tier) and pull redscript dependencies. They are not
  composed for de-tiering; if run alongside, expect tier assumptions to
  conflict with a de-tiered component graph — use with care.
- **Optional economy:**
  [Immersive Crafting Access](https://www.nexusmods.com/cyberpunk2077/mods/16154)
  (−30% component cost).
- **Adjacency:**
  [Immersive Crafting](https://www.nexusmods.com/cyberpunk2077/mods/22824)
  restricts crafting to the stash (craft-side) — the natural pair to the
  [Immersive Scraping](../README.md) mod (disassemble-side).
- **Rejected:**
  [Immersive Components](https://www.nexusmods.com/cyberpunk2077/mods/11880) —
  it only *renames* tiered components, it does not remove the tiers, so it
  does not serve the thesis.

## Status

Planned. No data files yet — the recipe-graph rewrite is scoped but not
written; the release archive is deferred until there is content to ship
(same discipline as the rest of the repo: package only when a module is
real). See [`PROGRESS.md`](./PROGRESS.md).
