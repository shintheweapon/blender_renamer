"""Material renaming operators."""
from __future__ import annotations

from typing import Any, TYPE_CHECKING

import bpy
from bpy.types import Context, Material

from .base_operator import BaseRenameOperator
from ..core.rename_engine import RenameOperation

if TYPE_CHECKING:
    from bpy.types import PropertyGroup


class MaterialRenameOperatorMixin:
    """Mixin providing material-specific functionality."""

    @classmethod
    def additional_poll(cls, context: Context) -> bool:
        """Check if materials exist to rename."""
        return len(bpy.data.materials) > 0 or (
            context.object is not None and len(context.object.material_slots) > 0
        )

    def get_properties(self, context: Context) -> PropertyGroup:
        """Get material renamer properties."""
        return context.scene.material_renamer_props

    def get_items(self, context: Context, properties: PropertyGroup) -> list[Material]:
        """Get materials to rename based on target selection."""
        materials: set[Material] = set()
        target = properties.target_materials
        include_unused = properties.include_unused

        if target == 'ALL':
            for mat in bpy.data.materials:
                if include_unused or mat.users > 0:
                    materials.add(mat)

        elif target == 'SELECTED':
            for obj in context.selected_objects:
                for slot in obj.material_slots:
                    if slot.material:
                        materials.add(slot.material)

        elif target == 'ACTIVE':
            if context.object:
                for slot in context.object.material_slots:
                    if slot.material:
                        materials.add(slot.material)

        return list(materials)

    def get_item_type_name(self) -> str:
        """Return item type name."""
        return "material"


class MATERIAL_OT_search_replace(MaterialRenameOperatorMixin, BaseRenameOperator):
    """Search and replace text in material names"""
    bl_idname = "material.search_replace"
    bl_label = "Search & Replace"
    bl_description = "Search and replace text in material names"
    operation = RenameOperation.SEARCH_REPLACE


class MATERIAL_OT_add_prefix(MaterialRenameOperatorMixin, BaseRenameOperator):
    """Add prefix to material names"""
    bl_idname = "material.add_prefix"
    bl_label = "Add Prefix"
    bl_description = "Add prefix to material names"
    operation = RenameOperation.ADD_PREFIX


class MATERIAL_OT_add_suffix(MaterialRenameOperatorMixin, BaseRenameOperator):
    """Add suffix to material names"""
    bl_idname = "material.add_suffix"
    bl_label = "Add Suffix"
    bl_description = "Add suffix to material names"
    operation = RenameOperation.ADD_SUFFIX


class MATERIAL_OT_add_prefix_suffix(MaterialRenameOperatorMixin, BaseRenameOperator):
    """Add both prefix and suffix to material names"""
    bl_idname = "material.add_prefix_suffix"
    bl_label = "Add Prefix & Suffix"
    bl_description = "Add both prefix and suffix to material names"
    operation = RenameOperation.ADD_PREFIX_SUFFIX


# Registration
classes = (
    MATERIAL_OT_search_replace,
    MATERIAL_OT_add_prefix,
    MATERIAL_OT_add_suffix,
    MATERIAL_OT_add_prefix_suffix,
)


def register() -> None:
    """Register material operators."""
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister() -> None:
    """Unregister material operators."""
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
