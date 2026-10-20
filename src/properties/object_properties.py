"""Object-specific renamer properties."""
from __future__ import annotations

import bpy
from bpy.props import EnumProperty, BoolProperty, StringProperty

from .base_properties import BaseRenamerProperties


class ObjectRenamerProperties(BaseRenamerProperties):
    """Properties for object renaming operations."""

    # Override base properties with proper annotations for Blender
    search_text: StringProperty(
        name="Search",
        description="Text to search for in object names",
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
        description="Text to add before object names",
        default=""
    )

    suffix_text: StringProperty(
        name="Suffix",
        description="Text to add after object names",
        default=""
    )

    # Object-specific properties
    target_objects: EnumProperty(
        name="Target",
        description="Which objects to rename",
        items=[
            ('ALL', 'All Objects', 'Rename all objects in the file'),
            ('SELECTED', 'Selected Objects', 'Rename selected objects'),
            ('ACTIVE', 'Active Object', 'Rename the active object only'),
        ],
        default='SELECTED'
    )


def register() -> None:
    """Register object renamer properties."""
    bpy.utils.register_class(ObjectRenamerProperties)
    bpy.types.Scene.object_renamer_props = bpy.props.PointerProperty(
        type=ObjectRenamerProperties
    )


def unregister() -> None:
    """Unregister object renamer properties."""
    del bpy.types.Scene.object_renamer_props
    bpy.utils.unregister_class(ObjectRenamerProperties)
