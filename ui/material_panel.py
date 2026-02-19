"""Material renamer UI panel."""
from __future__ import annotations

import bpy
from bpy.types import Context
from bpy.app.translations import pgettext_iface as _

from .panel_base import BaseRenamerPanel


class VIEW3D_PT_material_renamer(BaseRenamerPanel):
    """Panel for material renaming tools."""

    bl_label = "Material Renamer"
    bl_idname = "VIEW3D_PT_material_renamer"
    bl_order = 1  # Second panel in the category

    @classmethod
    def poll(cls, context: Context) -> bool:
        """Show panel when materials exist."""
        return len(bpy.data.materials) > 0 or (
            context.object and len(context.object.material_slots) > 0
        )

    def draw(self, context: Context) -> None:
        """Draw the panel UI."""
        layout = self.layout
        props = context.scene.material_renamer_props

        # Target selection
        self.draw_target_section(layout, props, "target_materials", 'MATERIAL')

        # Material-specific options
        box = layout.box()
        box.label(text=_("Options:"), icon='SETTINGS')
        box.prop(props, "include_unused")

        # Search & Replace section
        self.draw_search_replace_section(
            layout, props, "material.search_replace"
        )

        # Prefix & Suffix section
        self.draw_prefix_suffix_section(
            layout, props,
            "material.add_prefix",
            "material.add_suffix",
            "material.add_prefix_suffix"
        )

        # Material count info
        self.draw_count_info(
            layout, "Total materials in file", len(bpy.data.materials))


def register() -> None:
    """Register material panel."""
    bpy.utils.register_class(VIEW3D_PT_material_renamer)


def unregister() -> None:
    """Unregister material panel."""
    bpy.utils.unregister_class(VIEW3D_PT_material_renamer)
