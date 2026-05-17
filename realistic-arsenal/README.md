# Realistic Arsenal — overview

> Vision and current state. For the actionable, per-workstream tracker (status,
> branches, blockers, verification), see [`PROGRESS.md`](./PROGRESS.md). For
> what is composed vs built, see [`ECOSYSTEM-AUDIT.md`](./ECOSYSTEM-AUDIT.md).

Formerly the "Cyberpunk Realism" suite. The separate weapon-identity and
crafting tracks are now **one mod**, because they share one root cause.

## Vision

The tier/quality scale is a meaningless abstraction. **A weapon is a weapon.**
Its identity comes from real attributes — archetype, ammo, condition,
hit-location — not a hidden Common→Iconic ladder, a rarity rainbow, or a
level delta. And it is **built and maintained from real, non-tiered
components and materials**, not from abstract "tier-3 components".

Removing the weapon-tier scale and removing the component-tier scale are the
*same* data surface — so this is one coherent mod, not two. It pairs directly
with **Immersive Scraping**: scrapping yields *real* components, which are
exactly what Realistic Arsenal's tier-free crafting consumes.

The guiding fantasy: **Night City is lethal in both directions.** A pistol
round is a pistol round whether it leaves your gun or a gonk's; what changes
outcomes is positioning, gear, condition, and what you hit — not whether an
enemy is "six levels above you".

Each concern is a standalone facet with its own `r6/scripts/realisticArsenal/`
folder and release archive, so the mod can later be split across repos without
rework.

## Design tenets (locked)

1. **Neutralise, never delete.** Collapse a signal's influence to a no-op
   rather than ripping it out. Survives game patches and deep mod stacks; does
   not fight the engine. Every redscript module has a default-on kill-switch
   that falls through to vanilla `wrappedMethod(...)`. (The data-layer
   de-tiering facets honour this in spirit: tiers collapse to a single neutral
   value / real components, and vanilla is recovered by uninstalling the data
   mod — tenet 1 remains the rule for the redscript layer.)
2. **Structural symmetry.** Parity between player and NPC is achieved by
   wrapping the *shared* code path — never by branching on "is this the
   player". Same rule both ways, by construction.
3. **Compose, don't reimplement.** Data-driven layers already covered by
   mature, configurable mods (e.g. NPC health pools) are delegated via
   documented composition, not rebuilt.
4. **Modular & multi-repo-ready.** Standalone modules, extractable at no cost.
5. **Discipline before `main`.** Work matures on the `feature/cyberpunk-realism`
   integration branch (one dash-separated sub-branch per workstream). A module
   reaches `main` only when **dry**: CI green **and** its wrapped game symbols
   verified in-game via `r6/cache/redscript.log` (or switched to the
   documented fallback seam). Public `main` never carries unfinished work.

Compose-first is also a *prioritisation* rule — see the suite doctrine in
`PROGRESS.md` — but it is doctrine, not a sixth tenet; these five are locked.

## Facets — what the mod does to date

| Facet | Concern | State |
|---|---|---|
| a — Damage de-scaling | Remove level + item-tier influence on damage (shared `RPGManager` static), strict NPC parity | Implemented, **pending in-game symbol verification** |
| b — Asymmetric scope-rule | Strip player-scaling from firearms while preserving the attribute→melee path | Planned (inside facet a's seam) |
| c — UI colour neutralisation | Stop the rarity rainbow signalling power | Implemented (best-effort symbol) |
| d — UI level-hiding | Blank level labels (nameplate / tooltip / level-up) | Planned sub-items |
| e — Loot / weapon-tier removal | Same weapon at drop/vendor/upgrade is one object, not a ladder | Scope-spike (data surface) |
| f — Component / crafting de-tiering | Real, non-tiered crafting components | Scope-spike + composed modules |
| g — Weapon condition / decay | Weapons degrade and need maintenance | Composed (Weapon Conditioning) |

## Composition (out of redscript scope)

Provisional — see the confidence caveat in
[`ECOSYSTEM-AUDIT.md`](./ECOSYSTEM-AUDIT.md) (Nexus is not auto-fetchable;
verdicts are search-snippet level until manually re-verified).

- **NPC health pools / time-to-kill** (data-driven):
  [No Enemy Scaling](https://www.nexusmods.com/cyberpunk2077/mods/24244) or
  [Damage Scaling and Balance](https://www.nexusmods.com/cyberpunk2077/mods/1712).
- **Notoriety / heat:**
  [Enemies of Dogtown](https://www.nexusmods.com/cyberpunk2077/mods/27898) +
  [Night City Remembers](https://www.nexusmods.com/cyberpunk2077/mods/29008) +
  [NCPD Duty Expansion](https://www.nexusmods.com/cyberpunk2077/mods/21547).
- **Consumables:**
  [Immersive Grenades](https://www.nexusmods.com/cyberpunk2077/mods/25334).
- **Skills (interim, C3):**
  [Skillful](https://www.nexusmods.com/cyberpunk2077/mods/9309)
  ([9281](https://www.nexusmods.com/cyberpunk2077/mods/9281)).
- **Weapon condition / decay:**
  [Weapon Conditioning](https://www.nexusmods.com/cyberpunk2077/mods/10479) —
  compose the decay layer only; its tier-gate contradicts the tier removal
  (see the audit's tension note).
- **Crafting modules:**
  [Preem Weaponsmith](https://www.nexusmods.com/cyberpunk2077/mods/9692) +
  [Enhanced Craft](https://www.nexusmods.com/cyberpunk2077/mods/4378) +
  optional [Immersive Crafting Access](https://www.nexusmods.com/cyberpunk2077/mods/16154)
  (−30% component cost).
- **Weapon colour (data-side alternative to facet c):**
  [Rarity Color Removed](https://www.nexusmods.com/cyberpunk2077/mods/20767).
- **Adjacency:**
  [Immersive Crafting](https://www.nexusmods.com/cyberpunk2077/mods/22824)
  restricts crafting to the stash (craft-side) — the natural pair to the
  **Immersive Scraping** mod in this repo (disassemble-side).
- **Rejected:**
  [Immersive Components](https://www.nexusmods.com/cyberpunk2077/mods/11880) —
  it only *renames* tiered components, it does not remove the tiers, so it
  does not serve the thesis.

## Roadmap

One flagship axis: **Weapon Identity — the tier scale is meaningless** (facets
a–g in [`PROGRESS.md`](./PROGRESS.md); the loot/component de-tiering, facets
e+f, is the differentiator nothing in the ecosystem covers).

Deferred / composed, not on the build axis:
- **C3** continuous progression — deferred, composed via Skillful (interim).
- **C4** *skill* decay — deferred on the persistence blocker. (Distinct from
  facet g *weapon* decay, which is composed — do not conflate.)
- **C6** organic notoriety — dropped, composed (EDO + NCR + NCPD Duty Exp.).

## How it relates to this repo

This repo also ships the standalone **Immersive Scraping** mod (stash-only
disassemble — see the [repo README](../README.md)), the natural companion:
scrapping yields the real, non-tiered components Realistic Arsenal's crafting
consumes, complementary to the composed Immersive Crafting (22824) stash-only
crafting mod. Realistic Arsenal lives in this `realistic-arsenal/` folder for
now because tooling is repo-scoped, but is structured to extract cleanly into
its own repo.
