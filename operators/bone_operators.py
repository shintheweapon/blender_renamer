"""Bone renaming operators."""
from __future__ import annotations

from typing import Any, TYPE_CHECKING

import bpy
from bpy.types import Context, Operator
from bpy.app.translations import pgettext_iface as _

from .base_operator import BaseRenameOperator, skipped_message
from ..core.rename_engine import RenameOperation

if TYPE_CHECKING:
    from bpy.types import PropertyGroup


class BoneRenameOperatorMixin:
    """Mixin providing bone-specific functionality."""

    @classmethod
    def additional_poll(cls, context: Context) -> bool:
        """Check if armature is selected and in Edit mode."""
        return (
            context.object is not None
            and context.object.type == 'ARMATURE'
            and context.object.mode == 'EDIT'
        )

    def get_properties(self, context: Context) -> PropertyGroup:
        """Get bone renamer properties."""
        return context.scene.bone_renamer_props

    def get_items(self, context: Context, properties: PropertyGroup) -> list[Any]:
        """Get bones to rename based on target selection."""
        armature = context.object.data

        if properties.target_bones == 'SELECTED':
            return [b for b in armature.edit_bones if b.select]
        return list(armature.edit_bones)

    def get_item_type_name(self) -> str:
        """Return item type name."""
        return "bone"

    def name_taken(self, context: Context, item: Any, name: str) -> bool:
        """True when another bone of the armature already uses ``name``."""
        return bone_name_taken(context.object.data.edit_bones, item, name)


def bone_name_taken(edit_bones: Any, bone: Any, name: str) -> bool:
    """
    Tell whether another bone of the same armature uses a name.

    Parameters
    ----------
    edit_bones : bpy.types.ArmatureEditBones
        The armature's edit bones.
    bone : bpy.types.EditBone
        The bone about to be renamed.
    name : str
        Its new name.

    Returns
    -------
    bool
        True when a different bone already has ``name``.
    """
    other = edit_bones.get(name)
    return other is not None and other != bone


def load_mappings(csv_path: str, edit_bones: Any) -> tuple[dict[str, str] | None, str | None, str | None]:
    """
    Read a CSV of bone renames and keep the pairs whose old name is a bone.

    Parameters
    ----------
    csv_path : str
        Path of the CSV file (Custom_Bones,FS_Bones with a header row).
    edit_bones : bpy.types.ArmatureEditBones
        The armature's edit bones.

    Returns
    -------
    tuple of (dict or None, str or None, str or None)
        The pairs to apply with None, None; or None with a report level
        ('ERROR' or 'WARNING') and a message saying why there are none.
    """
    from ..core.csv_parser import CSVParser

    if not csv_path:
        return None, 'ERROR', "No CSV file selected"

    # Parse CSV file; all errors are caught and reported to the user
    try:
        parse_result = CSVParser.parse_file(csv_path)
    except Exception as e:
        # Catch any unexpected errors not handled by CSVParser
        return None, 'ERROR', f"Unexpected error reading CSV: {str(e)}"

    if not parse_result.is_valid:
        # CSVParser returns user-friendly error messages
        return None, 'ERROR', parse_result.error

    if parse_result.mapping_count == 0:
        return None, 'WARNING', "CSV file contains no valid mappings"

    # Filter mappings to only bones that exist
    bone_names = {bone.name for bone in edit_bones}
    valid_mappings, not_found = CSVParser.validate_mappings(parse_result.mappings, bone_names)

    if not valid_mappings:
        return None, 'WARNING', f"No bones match CSV entries ({not_found} entries not found in armature)"

    return valid_mappings, None, None


def apply_mappings(edit_bones: Any, mappings: dict[str, str]) -> tuple[int, list[str], list[str]]:
    """
    Rename bones by an old name to new name mapping.

    A bone whose new name another bone already uses is left as it was, so a
    swap (A to B, B to A) changes nothing.

    Parameters
    ----------
    edit_bones : bpy.types.ArmatureEditBones
        The armature's edit bones.
    mappings : dict of str to str
        New name for each old name.

    Returns
    -------
    tuple of (int, list of str, list of str)
        The number of bones renamed, the old names of bones skipped because
        their new name was taken, and "name (error)" for each failure.
    """
    renamed_count = 0
    taken = []
    failed_bones = []
    for bone in list(edit_bones):
        if bone.name not in mappings:
            continue
        new_name = mappings[bone.name]
        if new_name == bone.name:
            continue
        if bone_name_taken(edit_bones, bone, new_name):
            taken.append(bone.name)
            continue
        try:
            bone.name = new_name
            renamed_count += 1
        except Exception as e:
            failed_bones.append(f"{bone.name} ({str(e)})")
    return renamed_count, taken, failed_bones


class BONE_OT_search_replace(BoneRenameOperatorMixin, BaseRenameOperator):
    """Search and replace text in bone names"""
    bl_idname = "bone.search_replace"
    bl_label = "Search & Replace"
    bl_description = "Search and replace text in bone names"
    operation = RenameOperation.SEARCH_REPLACE


class BONE_OT_add_prefix(BoneRenameOperatorMixin, BaseRenameOperator):
    """Add prefix to bone names"""
    bl_idname = "bone.add_prefix"
    bl_label = "Add Prefix"
    bl_description = "Add prefix to bone names"
    operation = RenameOperation.ADD_PREFIX


class BONE_OT_add_suffix(BoneRenameOperatorMixin, BaseRenameOperator):
    """Add suffix to bone names"""
    bl_idname = "bone.add_suffix"
    bl_label = "Add Suffix"
    bl_description = "Add suffix to bone names"
    operation = RenameOperation.ADD_SUFFIX


class BONE_OT_add_prefix_suffix(BoneRenameOperatorMixin, BaseRenameOperator):
    """Add both prefix and suffix to bone names"""
    bl_idname = "bone.add_prefix_suffix"
    bl_label = "Add Prefix & Suffix"
    bl_description = "Add both prefix and suffix to bone names"
    operation = RenameOperation.ADD_PREFIX_SUFFIX


class BONE_OT_csv_import(Operator):
    """Import CSV file and rename bones based on mappings"""
    bl_idname = "bone.csv_import"
    bl_label = "Import CSV Renames"
    bl_description = "Rename bones using CSV mapping file (Custom_Bones -> FS_Bones)"
    bl_options = {'REGISTER', 'UNDO'}

    # Internal state for confirmation dialog
    _mappings: dict[str, str] = {}
    _match_count: int = 0
    _in_dialog: bool = False

    @classmethod
    def poll(cls, context: Context) -> bool:
        """Check if armature is selected and in Edit mode."""
        return (
            context.object is not None
            and context.object.type == 'ARMATURE'
            and context.object.mode == 'EDIT'
        )

    def invoke(self, context: Context, event) -> set[str]:
        """Parse CSV, validate, and show confirmation dialog (unless silent mode)."""
        props = context.scene.bone_renamer_props
        valid_mappings, level, message = load_mappings(
            props.csv_file_path, context.object.data.edit_bones)
        if valid_mappings is None:
            self.report({level}, message)
            return {'CANCELLED'}

        # Store mappings for execute()
        self._mappings = valid_mappings
        self._match_count = len(valid_mappings)

        # Silent mode: skip confirmation
        if props.csv_silent_mode:
            return self.execute(context)

        # Show confirmation dialog with custom UI
        self._in_dialog = True
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context: Context) -> None:
        """Draw confirmation dialog content (only during confirmation phase)."""
        layout = self.layout
        if self._in_dialog:
            layout.label(text=_("Are you sure to mass rename bones?"),
                         icon='QUESTION')
            layout.separator()
            layout.label(
                text=_("Rename {count} bone(s)").format(
                    count=self._match_count)
            )
            layout.label(text=_("This operation can be undone with Ctrl+Z"))

    def execute(self, context: Context) -> set[str]:
        """Apply bone renames based on CSV mappings. All errors caught and reported."""
        self._in_dialog = False
        if not self._mappings:
            # A repeated run (Repeat Last) has no pairs from invoke(); read the CSV again
            mappings, level, message = load_mappings(
                context.scene.bone_renamer_props.csv_file_path, context.object.data.edit_bones)
            if mappings is None:
                self.report({level}, message)
                return {'CANCELLED'}
            self._mappings = mappings

        try:
            armature = context.object.data
        except Exception as e:
            self.report({'ERROR'}, f"Failed to access armature data: {str(e)}")
            return {'CANCELLED'}

        # Apply renames using the dictionary mapping; errors are caught per bone
        renamed_count, taken, failed_bones = apply_mappings(armature.edit_bones, self._mappings)
        failed_count = len(failed_bones)

        # Report results with detailed error info
        if failed_count > 0:
            error_details = ", ".join(failed_bones[:3])  # Show first 3 errors
            if len(failed_bones) > 3:
                error_details += f", and {len(failed_bones) - 3} more"
            self.report(
                {'WARNING'},
                f"Renamed {renamed_count} bone(s), {failed_count} failed: {error_details}"
            )
        elif taken:
            self.report({'WARNING'}, skipped_message("bone", renamed_count, taken))
        else:
            self.report(
                {'INFO'}, f"Successfully renamed {renamed_count} bone(s) from CSV")

        return {'FINISHED'}


# Registration
classes = (
    BONE_OT_search_replace,
    BONE_OT_add_prefix,
    BONE_OT_add_suffix,
    BONE_OT_add_prefix_suffix,
    BONE_OT_csv_import,
)


def register() -> None:
    """Register bone operators."""
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister() -> None:
    """Unregister bone operators."""
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
