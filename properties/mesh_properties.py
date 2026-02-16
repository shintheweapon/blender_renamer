"""Mesh-specific renamer properties."""
from __future__ import annotations

import bpy
from bpy.props import EnumProperty, BoolProperty, StringProperty

from .base_properties import BaseRenamerProperties


class MeshRenamerProperties(BaseRenamerProperties):
    """Properties for mesh datablock renaming operations."""

    # Override base properties with proper annotations for Blender
    search_text: StringProperty(
        name="Search",
        description="Text to search for in mesh names",
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
        description="Text to add before mesh names",
        default=""
    )

    suffix_text: StringProperty(
        name="Suffix",
        description="Text to add after mesh names",
        default=""
    )

    # Mesh-specific properties
    target_meshes: EnumProperty(
        name="Target",
        description="Which mesh datablocks to rename",
        items=[
            ('ALL', 'All Meshes', 'Rename all mesh datablocks in the file'),
            ('SELECTED', 'Selected Objects', 'Rename meshes of selected objects'),
            ('ACTIVE', 'Active Object', 'Rename mesh of the active object only'),
        ],
        default='SELECTED'
    )

    sync_object_names: BoolProperty(
        name="Sync Object Names",
        description="Also rename the parent object to match the mesh name",
        default=False
    )

    include_linked: BoolProperty(
        name="Include Linked",
        description="Include linked/library meshes (will show warning if read-only)",
        default=False
    )


def register() -> None:
    """Register mesh renamer properties."""
    bpy.utils.register_class(MeshRenamerProperties)
    bpy.types.Scene.mesh_renamer_props = bpy.props.PointerProperty(
        type=MeshRenamerProperties
    )


def unregister() -> None:
    """Unregister mesh renamer properties."""
    del bpy.types.Scene.mesh_renamer_props
    bpy.utils.unregister_class(MeshRenamerProperties)
