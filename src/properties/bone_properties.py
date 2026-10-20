"""Bone-specific renamer properties."""
from __future__ import annotations

import bpy
from bpy.props import EnumProperty, StringProperty, BoolProperty

from .base_properties import BaseRenamerProperties


class BoneRenamerProperties(BaseRenamerProperties):
    """Properties for bone renaming operations."""

    # Override base properties with proper annotations for Blender
    search_text: StringProperty(
        name="Search",
        description="Text to search for in bone names",
        default=""
    )

    replace_text: StringProperty(
        name="Replace",
        description="Text to replace with",
        default=""
    )

    use_regex: BoolProperty(
        name="Use Regex",
        description="Enable regular expression pattern matching",
        default=False
    )

    case_sensitive: BoolProperty(
        name="Case Sensitive",
        description="Make search case-sensitive (only for non-regex)",
        default=True
    )

    prefix_text: StringProperty(
        name="Prefix",
        description="Text to add before bone names",
        default=""
    )

    suffix_text: StringProperty(
        name="Suffix",
        description="Text to add after bone names",
        default=""
    )

    # Bone-specific properties
    target_bones: EnumProperty(
        name="Target",
        description="Which bones to rename",
        items=[
            ('ALL', 'All Bones', 'Rename all bones in the armature'),
            ('SELECTED', 'Selected Bones', 'Rename only selected bones'),
        ],
        default='SELECTED'
    )

    # CSV Import properties
    csv_file_path: StringProperty(
        name="CSV File",
        description="Path to CSV file with bone rename mappings (Custom_Bones,FS_Bones)",
        default="",
        subtype='FILE_PATH'
    )

    csv_silent_mode: BoolProperty(
        name="Silent Mode",
        description="Skip confirmation dialog and apply CSV renames immediately",
        default=False
    )


def register() -> None:
    """Register bone renamer properties."""
    bpy.utils.register_class(BoneRenamerProperties)
    bpy.types.Scene.bone_renamer_props = bpy.props.PointerProperty(
        type=BoneRenamerProperties
    )


def unregister() -> None:
    """Unregister bone renamer properties."""
    del bpy.types.Scene.bone_renamer_props
    bpy.utils.unregister_class(BoneRenamerProperties)
