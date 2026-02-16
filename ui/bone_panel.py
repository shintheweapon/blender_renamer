"""Bone renamer UI panel."""
from __future__ import annotations

import bpy
from bpy.types import Context

from .panel_base import BaseRenamerPanel


class VIEW3D_PT_bone_renamer(BaseRenamerPanel):
    """Panel for bone renaming tools."""

    bl_label = "Bone Renamer"
    bl_idname = "VIEW3D_PT_bone_renamer"
    bl_order = 0  # First panel in the category

    @classmethod
    def poll(cls, context: Context) -> bool:
        """Show panel when armature is selected."""
        return context.object and context.object.type == 'ARMATURE'

    def draw(self, context: Context) -> None:
        """Draw the panel UI."""
        layout = self.layout
        props = context.scene.bone_renamer_props

        # Check if in Edit Mode
        if context.object.mode != 'EDIT':
            self.draw_warning(layout, "Switch to Edit Mode")
            return

        # Target selection
        self.draw_target_section(layout, props, "target_bones", 'BONE_DATA')

        # Search & Replace section
        self.draw_search_replace_section(
            layout, props, "bone.search_replace"
        )

        # Prefix & Suffix section
        self.draw_prefix_suffix_section(
            layout, props,
            "bone.add_prefix",
            "bone.add_suffix",
            "bone.add_prefix_suffix"
        )

        # Tips
        self.draw_tips_section(layout, [
            "Enable regex for patterns like ^(.*)$",
            "Use \\1, \\2 for regex groups",
            "Operations support undo (Ctrl+Z)",
        ])


def register() -> None:
    """Register bone panel."""
    bpy.utils.register_class(VIEW3D_PT_bone_renamer)


def unregister() -> None:
    """Unregister bone panel."""
    bpy.utils.unregister_class(VIEW3D_PT_bone_renamer)
