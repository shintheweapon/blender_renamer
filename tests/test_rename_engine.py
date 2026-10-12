# Tests for core/rename_engine.py (no Blender data needed)

import unittest

from blender_renamer.core.rename_engine import RenameConfig, RenameEngine, RenameOperation


class Item:
    """A stand-in for anything with a name."""

    def __init__(self, name):
        self.name = name


class ShortNameItem(Item):
    """Stores at most 5 characters, as Blender shortens long names."""

    def __setattr__(self, key, value):
        super().__setattr__(key, value[:5] if key == 'name' else value)


REMOVE_001 = RenameConfig(search_text='.001', replace_text='')


class RenameItemsTests(unittest.TestCase):

    def test_free_name_is_renamed(self):
        item = Item('Body.001')
        results = RenameEngine.rename_items([item], RenameOperation.SEARCH_REPLACE, REMOVE_001,
                                            name_taken=lambda i, n: False)
        self.assertEqual(item.name, 'Body')
        self.assertTrue(results[0].was_changed)
        self.assertFalse(results[0].taken)

    def test_taken_name_leaves_the_item_and_is_reported(self):
        item = Item('Body.001')
        results = RenameEngine.rename_items([item], RenameOperation.SEARCH_REPLACE, REMOVE_001,
                                            name_taken=lambda i, n: n == 'Body')
        self.assertEqual(item.name, 'Body.001')
        self.assertTrue(results[0].taken)
        self.assertTrue(results[0].success)
        self.assertFalse(results[0].was_changed)
        self.assertEqual(results[0].new_name, 'Body.001')

    def test_unchanged_name_is_not_checked(self):
        item = Item('Body')
        results = RenameEngine.rename_items([item], RenameOperation.SEARCH_REPLACE, REMOVE_001,
                                            name_taken=lambda i, n: True)
        self.assertFalse(results[0].taken)
        self.assertFalse(results[0].was_changed)

    def test_stored_name_is_recorded(self):
        item = ShortNameItem('Arm')
        config = RenameConfig(suffix_text='_Left')
        results = RenameEngine.rename_items([item], RenameOperation.ADD_SUFFIX, config)
        self.assertEqual(results[0].new_name, 'Arm_L')


class SearchReplaceTests(unittest.TestCase):

    def test_case_insensitive_replacement_is_plain_text(self):
        config = RenameConfig(search_text='_L', replace_text='\\1', case_sensitive=False)
        new_name, error = RenameEngine.compute_new_name('arm_l', RenameOperation.SEARCH_REPLACE, config)
        self.assertEqual((new_name, error), ('arm\\1', None))

    def test_regex_replacement_keeps_groups(self):
        config = RenameConfig(search_text='^(.*)_([LR])$', replace_text='\\1.\\2', use_regex=True)
        new_name, error = RenameEngine.compute_new_name('arm_L', RenameOperation.SEARCH_REPLACE, config)
        self.assertEqual((new_name, error), ('arm.L', None))


if __name__ == '__main__':
    unittest.main()
