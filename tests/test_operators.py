# Tests for the rename operators in Blender: names already in use

import os
import tempfile
import unittest

import bpy

from blender_renamer.operators import base_operator, bone_operators


def new_scene():
    """Empty the current file."""
    bpy.ops.wm.read_factory_settings(use_empty=True)


def mesh_object(object_name, mesh_name):
    """Create a mesh object linked to the scene."""
    obj = bpy.data.objects.new(object_name, bpy.data.meshes.new(mesh_name))
    bpy.context.scene.collection.objects.link(obj)
    return obj


def select_only(obj):
    """Make ``obj`` the only selected object and the active one."""
    for other in bpy.context.scene.objects:
        other.select_set(False)
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj


def remove_001(props):
    """Set Search '.001', Replace empty, plain text."""
    props.search_text = '.001'
    props.replace_text = ''
    props.use_regex = False


class MeshTakenNameTests(unittest.TestCase):

    def setUp(self):
        new_scene()
        props = bpy.context.scene.mesh_renamer_props
        remove_001(props)
        props.target_meshes = 'SELECTED'
        props.sync_object_names = False

    def test_free_name_is_used(self):
        obj = mesh_object('Body.001', 'Body.001')
        select_only(obj)
        bpy.ops.mesh.search_replace()
        self.assertEqual(obj.data.name, 'Body')

    def test_taken_name_leaves_the_mesh(self):
        # Blender would store the taken name 'X_Body' as 'X_Body.001'
        mesh_object('X_Body', 'X_Body')
        obj = mesh_object('Body', 'Body')
        select_only(obj)
        bpy.context.scene.mesh_renamer_props.prefix_text = 'X_'
        self.assertEqual(bpy.ops.mesh.add_prefix(), {'FINISHED'})
        self.assertEqual(obj.data.name, 'Body')

    def test_sync_skips_an_object_whose_name_is_taken(self):
        props = bpy.context.scene.mesh_renamer_props
        props.sync_object_names = True
        props.prefix_text = 'X_'
        mesh_object('X_Body', 'Other')
        obj = mesh_object('Body', 'Body')
        select_only(obj)
        bpy.ops.mesh.add_prefix()
        self.assertEqual(obj.data.name, 'X_Body')
        self.assertEqual(obj.name, 'Body')

    def test_sync_renames_the_object_when_free(self):
        bpy.context.scene.mesh_renamer_props.sync_object_names = True
        obj = mesh_object('Body.001', 'Body.001')
        select_only(obj)
        bpy.ops.mesh.search_replace()
        self.assertEqual((obj.name, obj.data.name), ('Body', 'Body'))


class MaterialTakenNameTests(unittest.TestCase):

    def setUp(self):
        new_scene()
        props = bpy.context.scene.material_renamer_props
        remove_001(props)
        props.target_materials = 'ACTIVE'
        self.obj = mesh_object('Body', 'Body')
        select_only(self.obj)

    def test_taken_name_leaves_the_material(self):
        bpy.data.materials.new('X_Skin').use_fake_user = True
        material = bpy.data.materials.new('Skin')
        self.obj.data.materials.append(material)
        bpy.context.scene.material_renamer_props.prefix_text = 'X_'
        bpy.ops.material.add_prefix()
        self.assertEqual(material.name, 'Skin')

    def test_free_name_is_used(self):
        material = bpy.data.materials.new('Skin.001')
        self.obj.data.materials.append(material)
        bpy.ops.material.search_replace()
        self.assertEqual(material.name, 'Skin')


class BoneTakenNameTests(unittest.TestCase):

    def setUp(self):
        new_scene()
        props = bpy.context.scene.bone_renamer_props
        remove_001(props)
        props.target_bones = 'ALL'
        data = bpy.data.armatures.new('Armature')
        self.obj = bpy.data.objects.new('Armature', data)
        bpy.context.scene.collection.objects.link(self.obj)
        select_only(self.obj)
        bpy.ops.object.mode_set(mode='EDIT')

    def tearDown(self):
        bpy.ops.object.mode_set(mode='OBJECT')

    def add_bones(self, *names):
        for name in names:
            bone = self.obj.data.edit_bones.new(name)
            bone.tail = (0, 0, 1)

    def names(self):
        return sorted(b.name for b in self.obj.data.edit_bones)

    def test_taken_name_leaves_the_bone(self):
        self.add_bones('Arm', 'Arm.001')
        bpy.ops.bone.search_replace()
        self.assertEqual(self.names(), ['Arm', 'Arm.001'])

    def test_free_name_is_used(self):
        self.add_bones('Arm.001')
        bpy.ops.bone.search_replace()
        self.assertEqual(self.names(), ['Arm'])

    def test_csv_swap_changes_nothing_and_reports_both(self):
        self.add_bones('Hand', 'Spine')
        renamed, taken, failed = bone_operators.apply_mappings(
            self.obj.data.edit_bones, {'Hand': 'Spine', 'Spine': 'Hand'})
        self.assertEqual(self.names(), ['Hand', 'Spine'])
        self.assertEqual((renamed, sorted(taken), failed), (0, ['Hand', 'Spine'], []))

    def test_csv_free_name_is_used(self):
        self.add_bones('Hand')
        renamed, taken, failed = bone_operators.apply_mappings(
            self.obj.data.edit_bones, {'Hand': 'L_Hand'})
        self.assertEqual(self.names(), ['L_Hand'])
        self.assertEqual((renamed, taken, failed), (1, [], []))


class ObjectRenamerTests(unittest.TestCase):

    def setUp(self):
        new_scene()
        props = bpy.context.scene.object_renamer_props
        remove_001(props)
        props.target_objects = 'SELECTED'

    def test_selected_object_name_changes_and_its_mesh_does_not(self):
        obj = mesh_object('Body.001', 'Mesh.003')
        select_only(obj)
        self.assertEqual(bpy.ops.object.search_replace(), {'FINISHED'})
        self.assertEqual((obj.name, obj.data.name), ('Body', 'Mesh.003'))

    def test_taken_name_leaves_the_object(self):
        mesh_object('X_Body', 'Other')
        obj = mesh_object('Body', 'Body')
        select_only(obj)
        bpy.context.scene.object_renamer_props.prefix_text = 'X_'
        self.assertEqual(bpy.ops.object.add_prefix(), {'FINISHED'})
        self.assertEqual(obj.name, 'Body')

    def test_all_renames_every_object(self):
        bpy.context.scene.object_renamer_props.target_objects = 'ALL'
        first = mesh_object('Arm.001', 'Arm.001')
        second = mesh_object('Leg.001', 'Leg.001')
        bpy.ops.object.search_replace()
        self.assertEqual((first.name, second.name), ('Arm', 'Leg'))

    def test_suffix_and_both(self):
        props = bpy.context.scene.object_renamer_props
        props.prefix_text = 'L_'
        props.suffix_text = '_fs'
        obj = mesh_object('Hand', 'Hand')
        select_only(obj)
        bpy.ops.object.add_suffix()
        self.assertEqual(obj.name, 'Hand_fs')
        bpy.ops.object.add_prefix_suffix()
        self.assertEqual(obj.name, 'L_Hand_fs_fs')

    def test_linked_objects_are_skipped(self):
        mesh_object('LibBody.001', 'LibMesh')
        path = os.path.join(tempfile.mkdtemp(), 'lib.blend')
        bpy.data.libraries.write(path, {bpy.data.objects['LibBody.001']})
        new_scene()
        with bpy.data.libraries.load(path, link=True) as (source, target):
            target.objects = ['LibBody.001']
        linked = bpy.data.objects['LibBody.001']
        bpy.context.scene.collection.objects.link(linked)
        bpy.context.scene.object_renamer_props.target_objects = 'ALL'
        self.assertEqual(bpy.ops.object.search_replace(), {'CANCELLED'})
        self.assertEqual(linked.name, 'LibBody.001')


class SkippedMessageTests(unittest.TestCase):

    def test_lists_three_names_then_the_rest(self):
        message = base_operator.skipped_message('mesh', 2, ['A', 'B', 'C', 'D', 'E'])
        self.assertEqual(message, "Renamed 2 mesh(s); 5 skipped, name already used: "
                                  "'A', 'B', 'C', and 2 more")

    def test_one_name(self):
        self.assertEqual(base_operator.skipped_message('bone', 0, ['Arm']),
                         "Renamed 0 bone(s); 1 skipped, name already used: 'Arm'")


if __name__ == '__main__':
    unittest.main()
