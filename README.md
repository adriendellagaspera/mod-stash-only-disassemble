# cp2077-realism-mods

A repository of small, independent Cyberpunk 2077 realism mods. **Each mod
lives in its own homonymous top-level folder** with its own README and (where
it ships) release archive, so mods install independently and can be extracted
to separate repos without rework.

## Mods

- **[Immersive Scrapping](./immersive-scrapping/README.md)** —
  [`immersive-scrapping/`](./immersive-scrapping/) — confines item scrapping
  (disassembly) to the stash screen. **Shipped** (lands on `main` via its own
  PR).
- **[Realistic Arsenal](./realistic-arsenal/README.md)** —
  [`realistic-arsenal/`](./realistic-arsenal/) — the weapon tier scale stops
  driving weapon identity (damage / UI). Vision & decisions in its README;
  workstream tracker in
  [`realistic-arsenal/PROGRESS.md`](./realistic-arsenal/PROGRESS.md).
- **[Realistic Components](./realistic-components/README.md)** —
  [`realistic-components/`](./realistic-components/) — tiered abstract crafting
  components become one real, non-tiered component (recipe + disassembly
  rewrite, TweakXL data). Tracker in
  [`realistic-components/PROGRESS.md`](./realistic-components/PROGRESS.md).

The three pair up: scrapping yields *real* components (Immersive Scrapping) →
recipes/disassembly trade in them (Realistic Components) → weapons are no
longer tier-graded (Realistic Arsenal). Realistic Arsenal/Components are on
the integration branch and reach `main` only when dry.

## Layout

```
immersive-scrapping/      # Immersive Scrapping (reds + README)
realistic-arsenal/       # Realistic Arsenal (reds/tweaks + README + PROGRESS)
realistic-components/    # Realistic Components (tweaks + tool + README + PROGRESS)
tools/                   # build-time generators (not shipped, not run by game)
.github/                 # CI, release, issue/PR templates (repo-wide)
CHANGELOG.md SECURITY.md LICENSE
```

## Releases

Tagging `v*` builds and publishes per-mod archives
(`<mod>-{version}-cp2077-{2x,1x}.zip`). See each mod's README for its
game-version archive table and install path.
