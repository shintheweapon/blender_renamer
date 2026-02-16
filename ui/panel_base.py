"""Base panel class with shared drawing utilities."""
from __future__ import annotations

from typing import TYPE_CHECKING

from bpy.types import Panel, UILayout

if TYPE_CHECKING:
    from bpy.types import Context, PropertyGroup


class BaseRenamerPanel(Panel):
    """
    Base class for renamer panels.

    Provides common UI drawing methods for consistent appearance
    across bone, material, and mesh renamer panels.
    """

    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Renamer'  # Single unified category for all panels

    @staticmethod
    def draw_target_section(
        layout: UILayout,
        props: PropertyGroup,
        target_prop: str,
        icon: str,
        label: str = "Target"
    ) -> None:
        """Draw the target selection section."""
        box = layout.box()
        box.label(text=f"{label}:", icon=icon)
        box.prop(props, target_prop, expand=True)

    @staticmethod
    def draw_search_replace_section(
        layout: UILayout,
        props: PropertyGroup,
        operator_idname: str
    ) -> None:
        """Draw the search & replace section."""
        box = layout.box()
        box.label(text="Search & Replace:", icon='VIEWZOOM')
        box.prop(props, "search_text")
        box.prop(props, "replace_text")

        row = box.row()
        row.prop(props, "use_regex")
        if not props.use_regex:
            row.prop(props, "case_sensitive")

        box.operator(operator_idname, icon='FILE_REFRESH')

    @staticmethod
    def draw_prefix_suffix_section(
        layout: UILayout,
        props: PropertyGroup,
        prefix_op: str,
        suffix_op: str,
        both_op: str
    ) -> None:
        """Draw the prefix & suffix section."""
        box = layout.box()
        box.label(text="Prefix & Suffix:", icon='SORTALPHA')
        box.prop(props, "prefix_text")
        box.prop(props, "suffix_text")

        row = box.row(align=True)
        row.operator(prefix_op, icon='FORWARD')
        row.operator(suffix_op, icon='BACK')

        box.operator(both_op, icon='ARROW_LEFTRIGHT')

    @staticmethod
    def draw_tips_section(layout: UILayout, tips: list[str]) -> None:
        """Draw a tips/info section."""
        layout.separator()
        info_box = layout.box()
        info_box.label(text="Tips:", icon='HELP')
        for tip in tips:
            info_box.label(text=tip)

    @staticmethod
    def draw_warning(layout: UILayout, message: str) -> None:
        """Draw a warning/info message."""
        layout.label(text=message, icon='INFO')

    @staticmethod
    def draw_count_info(layout: UILayout, label: str, count: int) -> None:
        """Draw a count information line."""
        layout.separator()
        layout.label(text=f"{label}: {count}")
