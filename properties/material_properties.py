"""Material-specific renamer properties."""
from __future__ import annotations

import bpy
from bpy.props import EnumProperty, StringProperty, BoolProperty

from .base_properties import BaseRenamerProperties


class MaterialRenamerProperties(BaseRenamerProperties):
    """Properties for material renaming operations."""

    # Override base properties with proper annotations for Blender
    search_text: StringProperty(
        name="Search",
        description="Text to search for in material names",
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
        description="Text to add before material names",
        default=""
    )

    suffix_text: StringProperty(
        name="Suffix",
        description="Text to add after material names",
        default=""
    )

    # Material-specific properties
    target_materials: EnumProperty(
        name="Target",
        description="Which materials to rename",
        items=[
            ('ALL', 'All Materials', 'Rename all materials in the file'),
            ('SELECTED', 'Selected Objects', 'Rename materials on selected objects'),
            ('ACTIVE', 'Active Object', 'Rename materials on the active object only'),
        ],
        default='SELECTED'
    )

    include_unused: BoolProperty(
        name="Include Unused",
        description="Include materials with no users (0 users)",
        default=False
    )


def register() -> None:
    """Register material renamer properties."""
    bpy.utils.register_class(MaterialRenamerProperties)
    bpy.types.Scene.material_renamer_props = bpy.props.PointerProperty(
        type=MaterialRenamerProperties
    )


def unregister() -> None:
    """Unregister material renamer properties."""
    del bpy.types.Scene.material_renamer_props
    bpy.utils.unregister_class(MaterialRenamerProperties)
