# Realistic Arsenal — ecosystem audit

Per realism domain, this records whether Realistic Arsenal **builds** the
concern, **scope-spikes** it (investigate before deciding), or **composes** an
existing mod. It is the entry gate for every workstream so we never re-litigate
"is this under-served?" from memory. Vision lives in [`README.md`](./README.md);
the actionable tracker in [`PROGRESS.md`](./PROGRESS.md).

## Confidence caveat

Nexus Mods blocks automated fetch (HTTP 403). All external-mod evidence below
is from **search snippets, not verified mod pages or in-game testing**. Every
`COMPOSE` verdict is **provisional** until the manual re-verification checklist
at the bottom is cleared on the real mod page / in a real install. Do **not**
ship a composition dependency on the strength of this table alone.

## Verdict vocabulary

- `INVALIDATED` — a prior assumption/idea is wrong or contradicted; dropped.
- `SURVIVES` — the idea remains valid and in-mod (we build or scope-spike it).
- `COVERED` — fully delivered by an existing mod; we build nothing.
- `PARTIAL` — an existing mod covers part; we still own the gap.
- `COMPOSE` — delegate to a named external mod (documented dependency, not
  reimplemented). A direct application of design tenet 3.

## The thesis this audit serves

> The tier/quality scale is meaningless. A weapon is a weapon — its identity
> comes from real attributes (archetype, ammo, condition, hit-location), and it
> is built and maintained from real, non-tiered components and materials.
> Removing the weapon-tier scale and removing the component-tier scale are the
> *same* TweakXL/data surface, so they are **one** workstream, not two.

Weapon-condition decay (composed, Weapon Conditioning) is the "maintained" half
of that thesis. It is **distinct from C4 skill decay** — do not conflate them.

## Per-domain inventory

| Domain | Vanilla pain | Stance | External mod(s) (Nexus ID) | Verdict | Confidence | Notes / tension |
|---|---|---|---|---|---|---|
| Notoriety / heat (was C6) | coarse near-binary wanted | delegate | Enemies of Dogtown 27898; Night City Remembers 29008; NCPD Duty Expansion 21547 | COMPOSE (was IDEA → DROPPED) | snippet | together approximate organic heat |
| Consumables / grenades | infinite pocket arsenal | delegate | Immersive Grenades 25334 | COMPOSE | snippet | finite/inventory model |
| Damage / level-tier scaling (facet a/b) | hidden level-delta sponge | **BUILD (flagship)** | health pools: No Enemy Scaling 24244 / Damage Scaling and Balance 1712 | SURVIVES (build) + COMPOSE (health) | snippet | redscript seam ours; health pools data-side |
| Rarity colour (facet c) | rainbow signals power | **BUILD** (redscript) + alt | Rarity Color Removed 20767 | SURVIVES + COMPOSE (data alt) | snippet | 20767 is a data-side alternative |
| Skills / learn-by-doing (C3) | milestone-gated growth | defer, delegate interim | Skillful 9309 / 9281 | DEFERRED + COMPOSE | snippet | interim until in-mod de-gate |
| **Skill** decay (C4) | none | defer | none viable | SURVIVES (deferred) | n/a | blocker = persistence, NOT the tick |
| **Weapon** decay / condition | weapons never degrade | delegate | Weapon Conditioning 10479 | COMPOSE (tier-gate tension) | snippet | compose decay layer only; see tension below |
| Loot / weapon-tier identity (facet e) | same gun Common→Iconic | **BUILD (flagship core)** | none removes the scale | SURVIVES (build) | snippet | TweakXL/data, mod-owned gap |
| Crafting / components (facet f) | tiered abstract components | **SCOPE-SPIKE** + delegate modules | Preem Weaponsmith 9692; Enhanced Craft 4378; Immersive Crafting Access 16154 (opt., −30% cost) | SURVIVES (spike) + COMPOSE | snippet | killing weapon tiers cascades component tiers |
| — components rename only | — | reject | Immersive Components 11880 | INVALIDATED | snippet | only **renames** tiered components ("Recycled Hardware Kit"…); does **not** remove tiers → does not serve the thesis |
| Crafting access locus (adjacency) | craft anywhere | note only | Immersive Crafting 22824 | COMPOSE-adjacent | snippet | restricts crafting to stash (craft-side); pairs with Immersive Scraping (disassemble-side) |
| Per-weapon identity | tier defines the gun | **BUILD** (unifying axis) | composed: 10479 (condition) + 9692 (modules) | SURVIVES (build) | snippet | archetype/ammo/condition/hit-loc |
| Economy (component cost) | — | optional delegate | Immersive Crafting Access 16154 | COMPOSE (optional) | snippet | −30% component cost layer |

### Weapon-decay vs tier-gate tension (load-bearing)

Weapon Conditioning (10479) bundles two things: (1) a **decay/condition/
jamming/repair** layer — wanted; and (2) a **tier-gate** ("no tier-up until
repaired", "tier tied to enemy rarity") that *reinforces* the very tier scale
Realistic Arsenal removes. We compose **only layer 1**. Once facet e removes the
tier scale, layer 2 becomes moot/contradictory. The manual checklist must
confirm layer 1 still functions standalone with tiers gone; if it cannot be
decoupled, weapon decay becomes a real gap to scope-spike rather than compose.

## Manual Nexus re-verification checklist

The maintainer performs these on the real mod pages / in a real install before
any composition is relied upon:

- [ ] 24244 No Enemy Scaling — maintained for current patch; data-only;
      coexists with the redscript damage flatten.
- [ ] 1712 Damage Scaling and Balance — config surface; alternative to 24244.
- [ ] 27898 / 29008 / 21547 — together approximate organic heat; no hard
      conflict with the damage flatten.
- [ ] 25334 Immersive Grenades — consumable scope only; no tier dependency.
- [ ] 9309 / 9281 Skillful — scales effects off proficiency without fighting
      the point system; acceptable C3 interim.
- [ ] 10479 Weapon Conditioning — **confirm the tier-gate logic** (no tier-up
      until repaired; tier ↔ enemy rarity) and that the decay/condition/
      jamming/repair layer still functions **standalone with tiers removed**.
- [ ] 9692 Preem Weaponsmith — adds **real** modules (muzzles/triggers,
      smart/tech conversion, recoil/fire-rate); optional progression locks;
      no hard tier dependency.
- [ ] 4378 Enhanced Craft — presets / skin / name / damage-type; non-tiered.
- [ ] 16154 Immersive Crafting Access — −30% component cost; optional economy.
- [ ] 11880 Immersive Components — **confirm rejection**: only renames tiered
      components, does NOT remove tiers; does not serve the thesis.
- [ ] 22824 Immersive Crafting — restricts crafting to the stash (craft-side);
      document adjacency to Immersive Scraping (disassemble-side).
- [ ] 20767 Rarity Color Removed — data-side colour removal; alternative or
      complement to the redscript colour facet.

## Outcome → tracker

Verdicts map onto [`PROGRESS.md`](./PROGRESS.md) as: the BUILD/SCOPE-SPIKE
domains (damage, colour, loot/tier, crafting/components, per-weapon identity)
collapse into the single flagship workstream **W1 — Weapon Identity**; COMPOSE
domains become `COMPOSED` dispositions (C6, consumables, weapon-decay, skills
interim); C4 stays `DEFERRED` on persistence; 11880 is recorded `INVALIDATED`.
