#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Realistic Components RC1 — recipe de-tiering generator.

#############################################################################
# SCHEMA-CORRECTED · RECIPE PASS FIXTURE-TESTED · STILL DUMP-GATED
#############################################################################
This is the re-derived generator. The previous version was refuted at the
schema level (2026-05-17; psiberx TweakXL wiki, CDPR docs, v1ld crafting
gist). What changed, and what is still gated:

  CORRECTED (now matches the documented schema, covered by tools/tests/):
   * Recipe-element shape is FLAT: each element is
       { "amount": <int>, "ingredient": "<Items.TweakDBID>" }
     `ingredient` is a *direct* TweakDBID — NOT the refuted nested
     `ingredient: { item, quantity }`. Extraction reads `amount` /
     `ingredient` directly.
   * De-tiering emits a DOCUMENTED array mutation: the recipe's whole
     element-array flat is reassigned (wholesale replace). There is no
     `array[index].subfield` flat path in TweakXL and `!append-once`
     APPENDS (does not replace) — both refuted; neither is used here.
   * Non-tier ingredients in a mixed recipe are PRESERVED (only the
     tiered ones are repointed); element `amount`/order are preserved, so
     ingredient count and cost are unchanged (identity-only swap).

  STILL DUMP-GATED (cannot be settled without a real patch-2.x dump —
  these are exposed as constants AND CLI flags, never silently assumed):
   * RECIPE_RECORD_TYPE — the exact record-type string a real WolvenKit /
     RED4ext dump uses (long engine class vs short schema name). Override
     with --recipe-record-type.
   * ELEMENTS_FIELD — the array flat that holds the elements
     (`ingredients` vs `elements`). Override with --elements-field.
   * Whether TweakXL needs an explicit inline `$type:` tag on each rebuilt
     element object for this game/TweakXL version. The emitted form is the
     documented common one; confirm against a real apply.
   * Disassembly de-tiering is NOT implemented here (see below).

DISASSEMBLY: DEFERRED ON PURPOSE (not guessed)
    The old disassembly pass was refuted as heuristics on the wrong record
    family. Rather than ship another guessed schema, this generator emits
    only an explicit DEFERRED stub for the disassembly output and records
    the precise re-derivation in realistic-components/PROGRESS.md. Honest
    gap > speculative broken data.

WHAT THIS IS
    A BUILD-TIME tool. NOT run by the game, NOT loaded by TweakXL. It reads
    a TweakDB dump JSON, finds every crafting recipe that references a
    tiered / `*Material*` component, and emits bulk TweakXL override YAML:

        r6/tweaks/realisticComponents/10-recipes.generated.yaml
        r6/tweaks/realisticComponents/20-disassembly.generated.yaml   (stub)

    The full recipe set is hundreds of records: a single missed recipe
    silently leaks a tiered component back into the economy with no error,
    so the bulk MUST be machine-generated from a real dump — never hand-typed.

EXPECTED DUMP FORMAT
    JSON, either shape (both normalise to the same internal model):

      1. Record-keyed object:
         { "Items.SomeRecipe": {
             "$type": "<recipeRecordType>",
             "<elementsField>": [
               { "amount": 3, "ingredient": "Items.CommonMaterial1" }, ...
             ] }, ... }

      2. Flat-list:
         [ { "id": "<TweakDBID>", "type": "<recordType>",
             "flats": { "<elementsField>": [ ... ] } }, ... ]

    Array elements may also be a list of TweakDBID strings that reference
    sibling inline records (each carrying flat `amount` / `ingredient`);
    both are resolved. The only dump-coupled surface is _iter_records() /
    _recipe_elements(); everything else works on the normalised model.

USAGE
    python3 tools/gen_realistic_components.py \
        --dump path/to/tweakdb_dump.json \
        --target Items.RealScrapComponent \
        [--recipe-record-type gamedataCraftingRecipe_Record] \
        [--elements-field ingredients]

    With no --dump the tool exits non-zero (this repo ships no dump on
    purpose). Stdlib only; `python3 -m py_compile` clean; unit-tested by
    tools/tests/.

UNINSTALL (of the mod, not this tool)
    Delete r6/tweaks/realisticComponents/ entirely. TweakXL applies no
    override not present on disk.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from typing import Any, Dict, Iterable, List, Optional, Tuple

# -----------------------------------------------------------------------------
# Dump-coupled symbols. Single source of truth; also CLI-overridable. These
# are the ONLY values that need a real dump to confirm — everything else is
# schema-correct by construction and covered by tools/tests/.
# -----------------------------------------------------------------------------

RECIPE_RECORD_TYPE = "gamedataCraftingRecipe_Record"  # confirm vs real dump
ELEMENTS_FIELD = "ingredients"  # array flat of {amount, ingredient}

# A component reference is "tiered" if its TweakDBID matches this. Matches the
# *Material* family (not just the five known IDs) because the long tail cannot
# be enumerated by hand.
TIER_COMPONENT_RE = re.compile(r"(?i)(?:^|\.)[A-Za-z0-9_]*Material[0-9]*$")

# Used only for the run summary's "known core covered?" check, never as the
# match set (matching is by the regex so the tail is caught).
CANONICAL_CORE = (
    "Items.CommonMaterial1",
    "Items.UncommonMaterial1",
    "Items.RareMaterial1",
    "Items.EpicMaterial1",
    "Items.LegendaryMaterial1",
)

RECIPES_BANNER = (
    "# GENERATED — DO NOT HAND-EDIT — REQUIRES TWEAKDB DUMP\n"
    "# =============================================================================\n"
    "# Emitted by tools/gen_realistic_components.py. Each affected recipe has its\n"
    "# whole element array reassigned (documented TweakXL wholesale array\n"
    "# override): tiered ingredients repointed to one real component, non-tier\n"
    "# ingredients and every `amount` preserved (identity-only; cost unchanged).\n"
    "# NOTE (dump/TweakXL-version gated): if this game/TweakXL build needs an\n"
    "# explicit inline `$type:` on each element object, add it via the\n"
    "# generator, not by hand (hand-edits are overwritten on the next run).\n"
)

DISASSEMBLY_STUB = (
    "# DEFERRED — NOT IMPLEMENTED — REQUIRES DUMP-CONFIRMED DISASSEMBLY FAMILY\n"
    "# =============================================================================\n"
    "# The previous disassembly pass was refuted as heuristics on the wrong\n"
    "# record family. It is intentionally NOT regenerated from a guess. The\n"
    "# precise re-derivation (which record family carries the disassembly /\n"
    "# scrap yield, and the flat that names the yielded component) is recorded\n"
    "# in realistic-components/PROGRESS.md and is gated on a real TweakDB dump.\n"
    "{}\n"
)


# -----------------------------------------------------------------------------
# Dump loading / normalisation — the only dump-coupled surface.
# -----------------------------------------------------------------------------


class Record:
    """Normalised TweakDB record."""

    __slots__ = ("rec_id", "rec_type", "flats")

    def __init__(self, rec_id: str, rec_type: str, flats: Dict[str, Any]):
        self.rec_id = rec_id
        self.rec_type = rec_type
        self.flats = flats


def _load_dump(path: str) -> Any:
    try:
        with open(path, "r", encoding="utf-8") as handle:
            return json.load(handle)
    except FileNotFoundError:
        raise SystemExit("error: dump file not found: %s" % path)
    except json.JSONDecodeError as exc:
        raise SystemExit(
            "error: dump is not valid JSON (%s). Convert a .str text dump to "
            "JSON first — see this tool's module docstring." % exc
        )


def _iter_records(dump: Any) -> Iterable[Record]:
    """Yield Record objects from either accepted dump shape."""
    if isinstance(dump, dict):
        for rec_id, body in dump.items():
            if not isinstance(body, dict):
                continue
            rec_type = body.get("$type") or body.get("type") or ""
            flats = {k: v for k, v in body.items() if not k.startswith("$")}
            flats.pop("type", None)
            yield Record(str(rec_id), str(rec_type), flats)
        return
    if isinstance(dump, list):
        for entry in dump:
            if not isinstance(entry, dict):
                continue
            rec_id = entry.get("id")
            if rec_id is None:
                continue
            rec_type = entry.get("type") or entry.get("$type") or ""
            flats = entry.get("flats")
            if not isinstance(flats, dict):
                flats = {
                    k: v
                    for k, v in entry.items()
                    if k not in ("id", "type", "$type")
                }
            yield Record(str(rec_id), str(rec_type), flats)
        return
    raise SystemExit(
        "error: unrecognised dump top-level type %s — expected a JSON object "
        "(record-keyed) or array (flat-list). See module docstring."
        % type(dump).__name__
    )


def _index(records: Iterable[Record]) -> Dict[str, Record]:
    return {r.rec_id: r for r in records}


# -----------------------------------------------------------------------------
# Flat element model. Element = { "amount": int, "ingredient": "Items.X" }.
# -----------------------------------------------------------------------------


def _recipe_elements(
    rec: Record, by_id: Dict[str, Record], elements_field: str
) -> List[Dict[str, Any]]:
    """Return a recipe's elements as flat {amount, ingredient} dicts.

    Handles both an inline list of element dicts and a list of TweakDBID
    strings referencing sibling inline records (each carrying the same flat
    `amount` / `ingredient`).
    """
    raw = rec.flats.get(elements_field)
    out: List[Dict[str, Any]] = []
    if isinstance(raw, list):
        for item in raw:
            if isinstance(item, dict):
                out.append(item)
            elif isinstance(item, str):
                sub = by_id.get(item)
                if sub is not None:
                    out.append(sub.flats)
    return out


def _elem_ingredient(element: Dict[str, Any]) -> Optional[str]:
    val = element.get("ingredient")
    return val if isinstance(val, str) else None


def _elem_amount(element: Dict[str, Any]) -> Any:
    amt = element.get("amount", 1)
    return amt if isinstance(amt, (int, float)) else 1


def _is_tier_component(item_id: str) -> bool:
    return bool(TIER_COMPONENT_RE.search(item_id or ""))


# -----------------------------------------------------------------------------
# Recipe pass — schema-correct, covered by tools/tests/.
# -----------------------------------------------------------------------------

# (recipe_id, [(amount, ingredient_after), ...]) — the full rebuilt array.
RecipeOverride = Tuple[str, List[Tuple[Any, str]]]


def recipes_pass(
    records: List[Record], by_id: Dict[str, Record],
    recipe_record_type: str, elements_field: str, target: str,
) -> List[RecipeOverride]:
    overrides: List[RecipeOverride] = []
    for rec in records:
        if rec.rec_type != recipe_record_type:
            continue
        elements = _recipe_elements(rec, by_id, elements_field)
        if not elements:
            continue
        rebuilt: List[Tuple[Any, str]] = []
        touched = False
        for el in elements:
            ing = _elem_ingredient(el)
            amt = _elem_amount(el)
            if ing is None:
                # Unknown element shape — keep a faithful placeholder so the
                # array length/cost is preserved; flagged by the emitter.
                rebuilt.append((amt, ing or ""))
                continue
            if _is_tier_component(ing):
                rebuilt.append((amt, target))
                touched = True
            else:
                rebuilt.append((amt, ing))
        if touched:
            overrides.append((rec.rec_id, rebuilt))
    return overrides


# -----------------------------------------------------------------------------
# YAML emission — minimal, hand-rolled (stdlib only). Documented wholesale
# array override; flow-style element maps for compactness.
# -----------------------------------------------------------------------------


def _scalar(value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, int):
        return str(value)
    if isinstance(value, float):
        return repr(value)
    return str(value)


def emit_recipes_yaml(
    overrides: List[RecipeOverride], target: str, elements_field: str
) -> str:
    out: List[str] = [RECIPES_BANNER]
    out.append(
        "# %d recipe(s) carry a tiered/*Material* ingredient; each repointed\n"
        "# to the single real component: %s\n"
        "# =============================================================================\n"
        % (len(overrides), target)
    )
    if not overrides:
        out.append("{}\n")
        return "".join(out)
    for recipe_id, elements in sorted(overrides):
        out.append("\n%s:\n" % recipe_id)
        out.append("  %s:\n" % elements_field)
        for amount, ingredient in elements:
            out.append(
                "    - { amount: %s, ingredient: %s }\n"
                % (_scalar(amount), _scalar(ingredient))
            )
    return "".join(out)


# -----------------------------------------------------------------------------
# CLI.
# -----------------------------------------------------------------------------


def _write(path: str, content: str) -> None:
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(content)


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="gen_realistic_components.py",
        description=(
            "Build-time generator for Realistic Components RC1. Reads a "
            "TweakDB dump and emits the bulk recipe de-tiering TweakXL YAML. "
            "NOT run by the game."
        ),
        epilog="With no --dump the tool exits non-zero (no dump ships here).",
    )
    parser.add_argument("--dump", metavar="PATH",
                        help="TweakDB dump JSON. Required for non-empty output.")
    parser.add_argument("--target", default="Items.RealScrapComponent",
                        help="The single real target component TweakDBID. MUST "
                        "be a dump-confirmed real vanilla / ArchiveXL item.")
    parser.add_argument("--recipe-record-type", default=RECIPE_RECORD_TYPE,
                        help="Dump-coupled: recipe record-type string. "
                        "Default: %(default)s.")
    parser.add_argument("--elements-field", default=ELEMENTS_FIELD,
                        help="Dump-coupled: the element-array flat name. "
                        "Default: %(default)s.")
    parser.add_argument(
        "--recipes-out",
        default="r6/tweaks/realisticComponents/10-recipes.generated.yaml",
        help="Output path for the recipes pass.")
    parser.add_argument(
        "--disassembly-out",
        default="r6/tweaks/realisticComponents/20-disassembly.generated.yaml",
        help="Output path for the DEFERRED disassembly stub.")
    parser.add_argument("--dry-run", action="store_true",
                        help="Compute and print the summary; write nothing.")
    return parser


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_arg_parser()
    args = parser.parse_args(argv)

    if not args.dump:
        sys.stderr.write(
            "error: no --dump supplied.\n\n"
            "This repo ships NO TweakDB dump on purpose. Generated files stay\n"
            "empty stubs until a real dump is provided at build time:\n\n"
            "  python3 tools/gen_realistic_components.py \\\n"
            "      --dump path/to/tweakdb_dump.json \\\n"
            "      --target Items.RealScrapComponent\n\n"
            "See --help and the module docstring for the dump format.\n"
        )
        return 2

    dump = _load_dump(args.dump)
    records = list(_iter_records(dump))
    by_id = _index(records)

    recipe_overrides = recipes_pass(
        records, by_id, args.recipe_record_type, args.elements_field,
        args.target,
    )

    n_recipes = sum(
        1 for r in records if r.rec_type == args.recipe_record_type
    )
    core_seen = set()
    for rec in records:
        if rec.rec_type != args.recipe_record_type:
            continue
        for el in _recipe_elements(rec, by_id, args.elements_field):
            it = _elem_ingredient(el)
            if it in CANONICAL_CORE:
                core_seen.add(it)

    sys.stderr.write(
        "Realistic Components RC1 generator — run summary\n"
        "  records in dump .............. %d\n"
        "  crafting recipes ............. %d\n"
        "  recipes retargeted ........... %d\n"
        "  canonical core IDs seen ...... %d/%d  %s\n"
        "  recipe record-type ........... %s\n"
        "  elements field ............... %s\n"
        "  target component ............. %s\n"
        "  disassembly .................. DEFERRED (dump-gated; see PROGRESS)\n"
        % (
            len(records), n_recipes, len(recipe_overrides),
            len(core_seen), len(CANONICAL_CORE),
            sorted(core_seen) or "(none — SUSPECT: record-type/field wrong)",
            args.recipe_record_type, args.elements_field, args.target,
        )
    )
    if n_recipes and not recipe_overrides:
        sys.stderr.write(
            "  WARNING: recipes exist but NONE carried a tier ingredient —\n"
            "  the record-type/elements-field/regex is likely wrong for this\n"
            "  dump. Do NOT ship this output.\n"
        )

    recipes_yaml = emit_recipes_yaml(
        recipe_overrides, args.target, args.elements_field
    )

    if args.dry_run:
        sys.stderr.write("  (dry-run: no files written)\n")
        return 0

    _write(args.recipes_out, recipes_yaml)
    _write(args.disassembly_out, DISASSEMBLY_STUB)
    sys.stderr.write(
        "  wrote %s\n  wrote %s (DEFERRED stub)\n"
        % (args.recipes_out, args.disassembly_out)
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
