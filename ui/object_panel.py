"""Object renamer UI panel."""
from __future__ import annotations

import bpy
from bpy.types import Context

from .panel_base import BaseRenamerPanel


class VIEW3D_PT_object_renamer(BaseRenamerPanel):
    """Panel for object renaming tools."""

    bl_label = "Object Renamer"
    bl_idname = "VIEW3D_PT_object_renamer"
    bl_order = 3  # Fourth panel in the category

    @classmethod
    def poll(cls, context: Context) -> bool:
        """Show panel when objects exist."""
        return len(bpy.data.objects) > 0

    def draw(self, context: Context) -> None:
        """Draw the panel UI."""
        layout = self.layout
        props = context.scene.object_renamer_props

        # Target selection
        self.draw_target_section(layout, props, "target_objects", 'OBJECT_DATA')

        # Search & Replace section
        self.draw_search_replace_section(
            layout, props, "object.search_replace"
        )

        # Prefix & Suffix section
        self.draw_prefix_suffix_section(
            layout, props,
            "object.add_prefix",
            "object.add_suffix",
            "object.add_prefix_suffix"
        )

        # Object count info
        self.draw_count_info(
            layout, "Total objects in file", len(bpy.data.objects))


def register() -> None:
    """Register object panel."""
    bpy.utils.register_class(VIEW3D_PT_object_renamer)


def unregister() -> None:
    """Unregister object panel."""
    bpy.utils.unregister_class(VIEW3D_PT_object_renamer)
