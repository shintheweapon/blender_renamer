"""Mesh datablock renaming operators."""
from __future__ import annotations

from typing import Any, TYPE_CHECKING

import bpy
from bpy.types import Context, Mesh, Object

from .base_operator import BaseRenameOperator
from ..core.rename_engine import RenameOperation, RenameResult

if TYPE_CHECKING:
    from bpy.types import PropertyGroup


class MeshRenameOperatorMixin:
    """Mixin providing mesh-specific functionality."""

    # Store object-mesh pairs for sync feature
    _object_mesh_pairs: list[tuple[Object, Mesh]] = []

    @classmethod
    def additional_poll(cls, context: Context) -> bool:
        """Check if meshes exist to rename."""
        return len(bpy.data.meshes) > 0 or (
            context.object is not None and context.object.type == 'MESH'
        )

    def get_properties(self, context: Context) -> PropertyGroup:
        """Get mesh renamer properties."""
        return context.scene.mesh_renamer_props

    def get_items(self, context: Context, properties: PropertyGroup) -> list[Mesh]:
        """Get meshes to rename based on target selection."""
        meshes: set[Mesh] = set()
        target = properties.target_meshes
        include_linked = properties.include_linked

        # Clear pairs for sync feature
        self._object_mesh_pairs = []

        def add_mesh(obj: Object, mesh: Mesh) -> None:
            """Add mesh to set and track object pair if syncing."""
            if not include_linked and mesh.library:
                return
            if mesh not in meshes:
                meshes.add(mesh)
                if properties.sync_object_names:
                    self._object_mesh_pairs.append((obj, mesh))

        if target == 'ALL':
            for mesh in bpy.data.meshes:
                if include_linked or not mesh.library:
                    meshes.add(mesh)

        elif target == 'SELECTED':
            for obj in context.selected_objects:
                if obj.type == 'MESH' and obj.data:
                    add_mesh(obj, obj.data)

        elif target == 'ACTIVE':
            if context.object and context.object.type == 'MESH':
                add_mesh(context.object, context.object.data)

        return list(meshes)

    def get_item_type_name(self) -> str:
        """Return item type name."""
        return "mesh"

    def post_rename_hook(self, context: Context, results: list[RenameResult]) -> None:
        """Sync object names if enabled."""
        props = self.get_properties(context)
        if not props.sync_object_names:
            return

        # Build a map of old mesh names to new names
        name_changes = {r.old_name: r.new_name for r in results if r.was_changed}

        for obj, mesh in self._object_mesh_pairs:
            # Check if this mesh was renamed
            for old_name, new_name in name_changes.items():
                if mesh.name == new_name:
                    obj.name = new_name
                    break


class MESH_OT_search_replace(MeshRenameOperatorMixin, BaseRenameOperator):
    """Search and replace text in mesh names"""
    bl_idname = "mesh.search_replace"
    bl_label = "Search & Replace"
    bl_description = "Search and replace text in mesh datablock names"
    operation = RenameOperation.SEARCH_REPLACE


class MESH_OT_add_prefix(MeshRenameOperatorMixin, BaseRenameOperator):
    """Add prefix to mesh names"""
    bl_idname = "mesh.add_prefix"
    bl_label = "Add Prefix"
    bl_description = "Add prefix to mesh datablock names"
    operation = RenameOperation.ADD_PREFIX


class MESH_OT_add_suffix(MeshRenameOperatorMixin, BaseRenameOperator):
    """Add suffix to mesh names"""
    bl_idname = "mesh.add_suffix"
    bl_label = "Add Suffix"
    bl_description = "Add suffix to mesh datablock names"
    operation = RenameOperation.ADD_SUFFIX


class MESH_OT_add_prefix_suffix(MeshRenameOperatorMixin, BaseRenameOperator):
    """Add both prefix and suffix to mesh names"""
    bl_idname = "mesh.add_prefix_suffix"
    bl_label = "Add Prefix & Suffix"
    bl_description = "Add both prefix and suffix to mesh datablock names"
    operation = RenameOperation.ADD_PREFIX_SUFFIX


# Registration
classes = (
    MESH_OT_search_replace,
    MESH_OT_add_prefix,
    MESH_OT_add_suffix,
    MESH_OT_add_prefix_suffix,
)


def register() -> None:
    """Register mesh operators."""
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister() -> None:
    """Unregister mesh operators."""
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
