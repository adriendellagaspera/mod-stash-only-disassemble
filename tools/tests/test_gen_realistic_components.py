#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Unit tests for gen_realistic_components.py — the schema-corrected recipe
pass. These prove the generator is correct against the *documented* flat
element shape (`amount` + `ingredient` = direct TweakDBID) and the
documented wholesale-array override. They do NOT (cannot) prove the
dump-coupled symbols (record-type / elements-field strings) are right for a
real game dump — that stays gated on a real TweakDB dump.
"""

import importlib.util
import json
import os
import unittest

_HERE = os.path.dirname(os.path.abspath(__file__))
_MOD_PATH = os.path.join(_HERE, os.pardir, "gen_realistic_components.py")
_FIXTURE = os.path.join(_HERE, "fixtures", "sample_dump.json")

_spec = importlib.util.spec_from_file_location("gen_rc", _MOD_PATH)
gen = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(gen)

TARGET = "Items.RealScrapComponent"


def _overrides(dump):
    records = list(gen._iter_records(dump))
    by_id = gen._index(records)
    return records, by_id, gen.recipes_pass(
        records, by_id, gen.RECIPE_RECORD_TYPE, gen.ELEMENTS_FIELD, TARGET
    )


class TierRegexTests(unittest.TestCase):
    def test_matches_material_family(self):
        for good in (
            "Items.CommonMaterial1", "Items.RareMaterial2",
            "Items.LegendaryMaterial1", "Items.SomeWeirdMaterial",
        ):
            self.assertTrue(gen._is_tier_component(good), good)

    def test_rejects_non_tier(self):
        for bad in (
            "Items.RealScrapComponent", "Items.OrganicMatter",
            "Items.QuestItemToken", "", "Items.MaterialBench",
        ):
            self.assertFalse(gen._is_tier_component(bad), bad)


class FlatSchemaExtractionTests(unittest.TestCase):
    def test_flat_amount_and_direct_ingredient(self):
        el = {"amount": 7, "ingredient": "Items.RareMaterial1"}
        self.assertEqual(gen._elem_ingredient(el), "Items.RareMaterial1")
        self.assertEqual(gen._elem_amount(el), 7)

    def test_refuted_nested_shape_yields_no_ingredient(self):
        # The OLD (refuted) nested shape must NOT be silently accepted.
        el = {"ingredient": {"item": "Items.RareMaterial1", "quantity": 3}}
        self.assertIsNone(gen._elem_ingredient(el))

    def test_missing_amount_defaults_to_one(self):
        self.assertEqual(gen._elem_amount({"ingredient": "Items.X"}), 1)


class RecipePassTests(unittest.TestCase):
    def setUp(self):
        self.dump = {
            "Items.Mixed_Crafting": {
                "$type": "gamedataCraftingRecipe_Record",
                "ingredients": [
                    {"amount": 5, "ingredient": "Items.CommonMaterial1"},
                    {"amount": 2, "ingredient": "Items.RareMaterial1"},
                    {"amount": 1, "ingredient": "Items.QuestToken"},
                ],
            },
            "Items.NoTier_Crafting": {
                "$type": "gamedataCraftingRecipe_Record",
                "ingredients": [
                    {"amount": 3, "ingredient": "Items.OrganicMatter"},
                ],
            },
        }

    def test_only_tiered_recipes_are_overridden(self):
        _, _, ov = _overrides(self.dump)
        ids = [rid for rid, _ in ov]
        self.assertEqual(ids, ["Items.Mixed_Crafting"])

    def test_tier_repointed_nontier_and_amounts_preserved(self):
        _, _, ov = _overrides(self.dump)
        _, elements = ov[0]
        self.assertEqual(
            elements,
            [
                (5, TARGET),                 # CommonMaterial1 -> target
                (2, TARGET),                 # RareMaterial1   -> target
                (1, "Items.QuestToken"),     # non-tier preserved
            ],
        )

    def test_emitted_yaml_is_wholesale_array_override(self):
        _, _, ov = _overrides(self.dump)
        y = gen.emit_recipes_yaml(ov, TARGET, gen.ELEMENTS_FIELD)
        self.assertIn("Items.Mixed_Crafting:", y)
        self.assertIn("  %s:" % gen.ELEMENTS_FIELD, y)
        self.assertIn(
            "- { amount: 5, ingredient: Items.RealScrapComponent }", y
        )
        self.assertIn(
            "- { amount: 1, ingredient: Items.QuestToken }", y
        )
        # Refuted forms must not appear.
        self.assertNotIn("!append-once", y)
        self.assertNotIn(".ingredient.item", y)
        self.assertNotIn("[0]", y)

    def test_empty_when_no_overrides(self):
        y = gen.emit_recipes_yaml([], TARGET, gen.ELEMENTS_FIELD)
        self.assertIn("{}", y)


class DumpShapeEquivalenceTests(unittest.TestCase):
    def test_record_keyed_and_flat_list_agree(self):
        rec_keyed = {
            "Items.R_Crafting": {
                "$type": "gamedataCraftingRecipe_Record",
                "ingredients": [
                    {"amount": 2, "ingredient": "Items.EpicMaterial1"}
                ],
            }
        }
        flat_list = [
            {
                "id": "Items.R_Crafting",
                "type": "gamedataCraftingRecipe_Record",
                "flats": {
                    "ingredients": [
                        {"amount": 2, "ingredient": "Items.EpicMaterial1"}
                    ]
                },
            }
        ]
        self.assertEqual(_overrides(rec_keyed)[2], _overrides(flat_list)[2])

    def test_non_recipe_record_type_is_ignored(self):
        dump = {
            "Items.Decoy": {
                "$type": "gamedataItem_Record",
                "ingredients": [
                    {"amount": 9, "ingredient": "Items.LegendaryMaterial1"}
                ],
            }
        }
        self.assertEqual(_overrides(dump)[2], [])


class FixtureTests(unittest.TestCase):
    def setUp(self):
        with open(_FIXTURE, "r", encoding="utf-8") as fh:
            self.dump = json.load(fh)

    def test_fixture_overrides(self):
        _, _, ov = _overrides(self.dump)
        by_id = {rid: els for rid, els in ov}
        # Tiered recipe: two tier ingredients repointed, quest token kept.
        self.assertEqual(
            by_id["Items.IconicPistol_Crafting"],
            [(5, TARGET), (2, TARGET), (1, "Items.QuestItemToken")],
        )
        # Inline-ref recipe resolves siblings: EpicMaterial2 -> target.
        self.assertEqual(
            by_id["Items.InlineRefRecipe_Crafting"],
            [(4, TARGET), (1, "Items.PlainScrew")],
        )
        # No-tier recipe and the non-recipe record are absent.
        self.assertNotIn("Items.PlainSnack_Crafting", by_id)
        self.assertNotIn("Items.NotARecipe", by_id)


class CliTests(unittest.TestCase):
    def test_no_dump_exits_two(self):
        self.assertEqual(gen.main([]), 2)

    def test_custom_record_type_and_field(self):
        dump = {
            "Items.Alt": {
                "$type": "ShortRecipe",
                "elems": [{"amount": 1, "ingredient": "Items.RareMaterial1"}],
            }
        }
        records = list(gen._iter_records(dump))
        ov = gen.recipes_pass(
            records, gen._index(records), "ShortRecipe", "elems", TARGET
        )
        self.assertEqual(ov, [("Items.Alt", [(1, TARGET)])])


if __name__ == "__main__":
    unittest.main()
