"""Mesh renamer UI panel."""
from __future__ import annotations

import bpy
from bpy.types import Context
from bpy.app.translations import pgettext_iface as _

from .panel_base import BaseRenamerPanel


class VIEW3D_PT_mesh_renamer(BaseRenamerPanel):
    """Panel for mesh datablock renaming tools."""

    bl_label = "Mesh Renamer"
    bl_idname = "VIEW3D_PT_mesh_renamer"
    bl_order = 2  # Third panel in the category

    @classmethod
    def poll(cls, context: Context) -> bool:
        """Show panel when meshes exist."""
        return len(bpy.data.meshes) > 0 or (
            context.object and context.object.type == 'MESH'
        )

    def draw(self, context: Context) -> None:
        """Draw the panel UI."""
        layout = self.layout
        props = context.scene.mesh_renamer_props

        # Target selection
        self.draw_target_section(layout, props, "target_meshes", 'MESH_DATA')

        # Mesh-specific options
        box = layout.box()
        box.label(text=_("Options:"), icon='SETTINGS')
        box.prop(props, "sync_object_names")
        box.prop(props, "include_linked")

        # Search & Replace section
        self.draw_search_replace_section(
            layout, props, "mesh.search_replace"
        )

        # Prefix & Suffix section
        self.draw_prefix_suffix_section(
            layout, props,
            "mesh.add_prefix",
            "mesh.add_suffix",
            "mesh.add_prefix_suffix"
        )

        # Mesh count info
        self.draw_count_info(
            layout, "Total meshes in file", len(bpy.data.meshes))


def register() -> None:
    """Register mesh panel."""
    bpy.utils.register_class(VIEW3D_PT_mesh_renamer)


def unregister() -> None:
    """Unregister mesh panel."""
    bpy.utils.unregister_class(VIEW3D_PT_mesh_renamer)
