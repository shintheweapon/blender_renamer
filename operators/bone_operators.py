"""Bone renaming operators."""
from __future__ import annotations

from typing import Any, TYPE_CHECKING

import bpy
from bpy.types import Context

from .base_operator import BaseRenameOperator
from ..core.rename_engine import RenameOperation

if TYPE_CHECKING:
    from bpy.types import PropertyGroup


class BoneRenameOperatorMixin:
    """Mixin providing bone-specific functionality."""

    @classmethod
    def additional_poll(cls, context: Context) -> bool:
        """Check if armature is selected and in Edit mode."""
        return (
            context.object is not None
            and context.object.type == 'ARMATURE'
            and context.object.mode == 'EDIT'
        )

    def get_properties(self, context: Context) -> PropertyGroup:
        """Get bone renamer properties."""
        return context.scene.bone_renamer_props

    def get_items(self, context: Context, properties: PropertyGroup) -> list[Any]:
        """Get bones to rename based on target selection."""
        armature = context.object.data

        if properties.target_bones == 'SELECTED':
            return [b for b in armature.edit_bones if b.select]
        return list(armature.edit_bones)

    def get_item_type_name(self) -> str:
        """Return item type name."""
        return "bone"


class BONE_OT_search_replace(BoneRenameOperatorMixin, BaseRenameOperator):
    """Search and replace text in bone names"""
    bl_idname = "bone.search_replace"
    bl_label = "Search & Replace"
    bl_description = "Search and replace text in bone names"
    operation = RenameOperation.SEARCH_REPLACE


class BONE_OT_add_prefix(BoneRenameOperatorMixin, BaseRenameOperator):
    """Add prefix to bone names"""
    bl_idname = "bone.add_prefix"
    bl_label = "Add Prefix"
    bl_description = "Add prefix to bone names"
    operation = RenameOperation.ADD_PREFIX


class BONE_OT_add_suffix(BoneRenameOperatorMixin, BaseRenameOperator):
    """Add suffix to bone names"""
    bl_idname = "bone.add_suffix"
    bl_label = "Add Suffix"
    bl_description = "Add suffix to bone names"
    operation = RenameOperation.ADD_SUFFIX


class BONE_OT_add_prefix_suffix(BoneRenameOperatorMixin, BaseRenameOperator):
    """Add both prefix and suffix to bone names"""
    bl_idname = "bone.add_prefix_suffix"
    bl_label = "Add Prefix & Suffix"
    bl_description = "Add both prefix and suffix to bone names"
    operation = RenameOperation.ADD_PREFIX_SUFFIX


# Registration
classes = (
    BONE_OT_search_replace,
    BONE_OT_add_prefix,
    BONE_OT_add_suffix,
    BONE_OT_add_prefix_suffix,
)


def register() -> None:
    """Register bone operators."""
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister() -> None:
    """Unregister bone operators."""
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
