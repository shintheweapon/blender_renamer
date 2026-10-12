# Tests for the Simplified Chinese interface: every text the add-on shows has
# a translation in the context Blender looks it up in

import unittest

import bpy

PROPERTY_GROUPS = ('bone_renamer_props', 'material_renamer_props',
                   'mesh_renamer_props', 'object_renamer_props')
COMMANDS = {
    'bone': ('search_replace', 'add_prefix', 'add_suffix', 'add_prefix_suffix', 'csv_import'),
    'material': ('search_replace', 'add_prefix', 'add_suffix', 'add_prefix_suffix'),
    'mesh': ('search_replace', 'add_prefix', 'add_suffix', 'add_prefix_suffix'),
    'object': ('search_replace', 'add_prefix', 'add_suffix', 'add_prefix_suffix'),
}


def missing_translations():
    """
    List the add-on's texts that stay English in Chinese.

    Option names and tooltips, target choices, and command labels and
    tooltips are looked up the way Blender does: options in their own
    context, command labels under 'Operator', command tooltips with no
    context.

    Returns
    -------
    list of str
        "kind: text" for each text without a translation.
    """
    tr = bpy.app.translations
    missing = []

    def check(kind, text, translate):
        if text and translate(text) == text:
            missing.append(f"{kind}: {text}")

    for group in PROPERTY_GROUPS:
        for prop in getattr(bpy.context.scene, group).bl_rna.properties:
            if prop.identifier in ('rna_type', 'name'):
                continue
            ctx = prop.translation_context
            check('option', prop.name, lambda t: tr.pgettext_iface(t, ctx))
            check('option tooltip', prop.description, lambda t: tr.pgettext_tip(t, ctx))
            if prop.type == 'ENUM':
                for item in prop.enum_items:
                    check('choice', item.name, lambda t: tr.pgettext_iface(t, ctx))
                    check('choice tooltip', item.description, lambda t: tr.pgettext_tip(t, ctx))
    for module, names in COMMANDS.items():
        for name in names:
            rna = getattr(getattr(bpy.ops, module), name).get_rna_type()
            check('command', rna.name, lambda t: tr.pgettext_iface(t, 'Operator'))
            check('command tooltip', rna.description, tr.pgettext_tip)
    return sorted(set(missing))


class ChineseTests(unittest.TestCase):

    def setUp(self):
        view = bpy.context.preferences.view
        self.saved = (view.language, view.use_translate_interface, view.use_translate_tooltips)
        view.language = 'zh_HANS'
        view.use_translate_interface = True
        view.use_translate_tooltips = True

    def tearDown(self):
        view = bpy.context.preferences.view
        view.language, view.use_translate_interface, view.use_translate_tooltips = self.saved

    def test_every_text_has_chinese(self):
        self.assertEqual(missing_translations(), [])


if __name__ == '__main__':
    unittest.main()
