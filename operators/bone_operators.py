"""Bone renaming operators."""
from __future__ import annotations

from typing import Any, TYPE_CHECKING

import bpy
from bpy.types import Context, Operator

from .base_operator import BaseRenameOperator
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
        from ..core.csv_parser import CSVParser

        props = context.scene.bone_renamer_props

        # Validate file path
        if not props.csv_file_path:
            self.report({'ERROR'}, "No CSV file selected")
            return {'CANCELLED'}

        # Parse CSV file - ALL errors are caught and reported to user
        try:
            parse_result = CSVParser.parse_file(props.csv_file_path)
        except Exception as e:
            # Catch any unexpected errors not handled by CSVParser
            self.report({'ERROR'}, f"Unexpected error reading CSV: {str(e)}")
            return {'CANCELLED'}

        if not parse_result.is_valid:
            # CSVParser returns user-friendly error messages
            self.report({'ERROR'}, parse_result.error)
            return {'CANCELLED'}

        if parse_result.mapping_count == 0:
            self.report({'WARNING'}, "CSV file contains no valid mappings")
            return {'CANCELLED'}

        # Get existing bone names
        armature = context.object.data
        bone_names = {bone.name for bone in armature.edit_bones}

        # Filter mappings to only bones that exist
        valid_mappings, not_found = CSVParser.validate_mappings(
            parse_result.mappings,
            bone_names
        )

        if not valid_mappings:
            self.report(
                {'WARNING'},
                f"No bones match CSV entries ({not_found} entries not found in armature)"
            )
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
            layout.label(text="Are you sure to mass rename bones?",
                         icon='QUESTION')
            layout.separator()
            layout.label(text=f"Rename {self._match_count} bone(s)")
            layout.label(text="This operation can be undone with Ctrl+Z")

    def execute(self, context: Context) -> set[str]:
        """Apply bone renames based on CSV mappings. All errors caught and reported."""
        self._in_dialog = False
        if not self._mappings:
            self.report({'ERROR'}, "No mappings available")
            return {'CANCELLED'}

        try:
            armature = context.object.data
        except Exception as e:
            self.report({'ERROR'}, f"Failed to access armature data: {str(e)}")
            return {'CANCELLED'}

        renamed_count = 0
        failed_count = 0
        failed_bones = []

        # Apply renames using dictionary mapping - catch errors per bone
        for bone in armature.edit_bones:
            if bone.name in self._mappings:
                new_name = self._mappings[bone.name]
                try:
                    bone.name = new_name
                    renamed_count += 1
                except Exception as e:
                    failed_count += 1
                    failed_bones.append(f"{bone.name} ({str(e)})")

        # Report results with detailed error info
        if failed_count > 0:
            error_details = ", ".join(failed_bones[:3])  # Show first 3 errors
            if len(failed_bones) > 3:
                error_details += f", and {len(failed_bones) - 3} more"
            self.report(
                {'WARNING'},
                f"Renamed {renamed_count} bone(s), {failed_count} failed: {error_details}"
            )
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
