"""Object renaming operators."""
from __future__ import annotations

from typing import TYPE_CHECKING

import bpy
from bpy.types import Context, Object

from .base_operator import BaseRenameOperator, id_name_taken
from ..core.rename_engine import RenameOperation

if TYPE_CHECKING:
    from bpy.types import PropertyGroup


class ObjectRenameOperatorMixin:
    """Mixin providing object-specific functionality."""

    @classmethod
    def additional_poll(cls, context: Context) -> bool:
        """Check if objects exist to rename."""
        return len(bpy.data.objects) > 0

    def get_properties(self, context: Context) -> PropertyGroup:
        """Get object renamer properties."""
        return context.scene.object_renamer_props

    def get_items(self, context: Context, properties: PropertyGroup) -> list[Object]:
        """Get objects to rename based on target selection; linked objects cannot be renamed."""
        target = properties.target_objects

        if target == 'ALL':
            objects = list(bpy.data.objects)
        elif target == 'SELECTED':
            objects = list(context.selected_objects)
        elif context.object:
            objects = [context.object]
        else:
            objects = []

        return [obj for obj in objects if not obj.library]

    def get_item_type_name(self) -> str:
        """Return item type name."""
        return "object"

    def name_taken(self, context: Context, item: Object, name: str) -> bool:
        """True when another object already uses ``name``."""
        return id_name_taken(bpy.data.objects, item, name)


class OBJECT_OT_search_replace(ObjectRenameOperatorMixin, BaseRenameOperator):
    """Search and replace text in object names"""
    bl_idname = "object.search_replace"
    bl_label = "Search & Replace"
    bl_description = "Search and replace text in object names"
    operation = RenameOperation.SEARCH_REPLACE


class OBJECT_OT_add_prefix(ObjectRenameOperatorMixin, BaseRenameOperator):
    """Add prefix to object names"""
    bl_idname = "object.add_prefix"
    bl_label = "Add Prefix"
    bl_description = "Add prefix to object names"
    operation = RenameOperation.ADD_PREFIX


class OBJECT_OT_add_suffix(ObjectRenameOperatorMixin, BaseRenameOperator):
    """Add suffix to object names"""
    bl_idname = "object.add_suffix"
    bl_label = "Add Suffix"
    bl_description = "Add suffix to object names"
    operation = RenameOperation.ADD_SUFFIX


class OBJECT_OT_add_prefix_suffix(ObjectRenameOperatorMixin, BaseRenameOperator):
    """Add both prefix and suffix to object names"""
    bl_idname = "object.add_prefix_suffix"
    bl_label = "Add Prefix & Suffix"
    bl_description = "Add both prefix and suffix to object names"
    operation = RenameOperation.ADD_PREFIX_SUFFIX


# Registration
classes = (
    OBJECT_OT_search_replace,
    OBJECT_OT_add_prefix,
    OBJECT_OT_add_suffix,
    OBJECT_OT_add_prefix_suffix,
)


def register() -> None:
    """Register object operators."""
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister() -> None:
    """Unregister object operators."""
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
