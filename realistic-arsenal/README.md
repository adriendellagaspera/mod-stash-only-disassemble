# Realistic Arsenal — overview

> Vision and locked decisions. For the actionable, per-workstream tracker
> (status, branches, blockers, verification, composition checklist), see
> [`PROGRESS.md`](./PROGRESS.md).

Formerly part of the "Cyberpunk Realism" suite. This mod is **weapons only**.
The scope-spike refuted the premise that weapon tiers and crafting-component
tiers are the same data surface (they are two independent TweakDB surfaces),
so component de-tiering is a **separate sibling mod**,
[Realistic Components](../realistic-components/README.md).

## Vision

The weapon tier/quality scale is a meaningless abstraction. **A weapon is a
weapon.** Its identity comes from real attributes — archetype, ammo,
condition, hit-location — not a hidden Common→Iconic ladder, a rarity
rainbow, or a level delta.

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
   de-tiering facet honours this in spirit: tiers collapse to a single neutral
   value, and vanilla is recovered by uninstalling the data mod — tenet 1
   remains the rule for the redscript layer.)
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
| e — Loot / weapon-tier removal | Same weapon at drop/vendor/upgrade is one object, not a ladder | Planned (BUILD via TweakXL data; spike done, not harness-blocked) |
| g — Weapon condition / decay | Weapons degrade and need maintenance | Composed (Weapon Conditioning) |

(There is no facet f here — component / crafting de-tiering is the separate
[Realistic Components](../realistic-components/README.md) mod.)

## Composition (out of redscript scope)

Provisional — Nexus Mods is not auto-fetchable (HTTP 403), so these verdicts
are search-snippet level, not verified mod pages or in-game testing. Every
composition below is a **locked direction but an unconfirmed dependency**: do
not rely on one until it is re-verified on the real mod page / in a real
install. The per-mod re-verification checklist lives in
[`PROGRESS.md`](./PROGRESS.md).

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
  (see the tension note in `PROGRESS.md` facet g).
- **Weapon colour (data-side alternative to facet c):**
  [Rarity Color Removed](https://www.nexusmods.com/cyberpunk2077/mods/20767).

Crafting/component composition (Preem Weaponsmith, Enhanced Craft, Immersive
Crafting Access, the rejected Immersive Components, the Immersive Crafting
adjacency) lives in the [Realistic Components](../realistic-components/README.md)
mod — those mods presuppose tiers and are not composed here.

## Roadmap

One flagship axis: **Weapon Identity — the weapon tier scale is meaningless**
(facets a–g in [`PROGRESS.md`](./PROGRESS.md); facet e — data weapon-tier
removal — is the differentiator nothing in the ecosystem covers).

Deferred / composed, not on the build axis:
- **C3** continuous progression — deferred, composed via Skillful (interim).
- **C4** *skill* decay — deferred on the persistence blocker. (Distinct from
  facet g *weapon* decay, which is composed — do not conflate.)
- **C6** organic notoriety — dropped, composed (EDO + NCR + NCPD Duty Exp.).

## How it relates to this repo

Sibling mods in this repo:

- **[Immersive Scraping](../README.md)** (stash-only disassemble) — scrapping
  yields the real, non-tiered components that tier-free crafting consumes.
- **[Realistic Components](../realistic-components/README.md)** — de-tiers the
  crafting-component graph (the consumer side of those scrapped components);
  the sibling de-tiering mod to this one.

Realistic Arsenal lives in this `realistic-arsenal/` folder for now because
tooling is repo-scoped, but is structured to extract cleanly into its own repo.
