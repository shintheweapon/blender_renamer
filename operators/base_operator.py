"""Base operator class for all renaming operations."""
from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING, Any

import bpy
from bpy.types import Operator, Context

from ..core.rename_engine import RenameEngine, RenameOperation, RenameConfig, RenameResult

if TYPE_CHECKING:
    from bpy.types import PropertyGroup


class BaseRenameOperator(Operator):
    """
    Abstract base class for rename operators.

    Subclasses must implement:
        - get_properties(context) -> PropertyGroup
        - get_items(context, properties) -> list
        - get_item_type_name() -> str (e.g., "bone", "material")

    Optionally override:
        - additional_poll(context) -> bool
        - pre_rename_hook(context, items) -> None
        - post_rename_hook(context, results) -> None
    """

    bl_options = {'REGISTER', 'UNDO'}

    # Subclasses set this to determine which operation type
    operation: RenameOperation = RenameOperation.SEARCH_REPLACE

    @classmethod
    def poll(cls, context: Context) -> bool:
        """Check if operator can be executed."""
        return cls.additional_poll(context)

    @classmethod
    def additional_poll(cls, context: Context) -> bool:
        """Override for additional poll conditions. Default returns True."""
        return True

    @abstractmethod
    def get_properties(self, context: Context) -> PropertyGroup:
        """Return the PropertyGroup for this operator's domain."""
        raise NotImplementedError

    @abstractmethod
    def get_items(self, context: Context, properties: PropertyGroup) -> list[Any]:
        """Return the list of items to rename."""
        raise NotImplementedError

    @abstractmethod
    def get_item_type_name(self) -> str:
        """Return the human-readable name for items (e.g., 'bone', 'material')."""
        raise NotImplementedError

    def pre_rename_hook(self, context: Context, items: list[Any]) -> None:
        """Called before renaming. Override for setup logic."""
        pass

    def post_rename_hook(self, context: Context, results: list[RenameResult]) -> None:
        """Called after renaming. Override for cleanup logic."""
        pass

    def create_config(self, properties: PropertyGroup) -> RenameConfig:
        """Create RenameConfig from properties."""
        return RenameConfig(
            search_text=getattr(properties, 'search_text', ''),
            replace_text=getattr(properties, 'replace_text', ''),
            prefix_text=getattr(properties, 'prefix_text', ''),
            suffix_text=getattr(properties, 'suffix_text', ''),
            use_regex=getattr(properties, 'use_regex', False),
            case_sensitive=getattr(properties, 'case_sensitive', True),
        )

    def execute(self, context: Context) -> set[str]:
        """Execute the rename operation."""
        props = self.get_properties(context)
        config = self.create_config(props)
        item_type = self.get_item_type_name()

        # Validate configuration
        error = RenameEngine.validate_config(self.operation, config)
        if error:
            self.report({'WARNING'}, error)
            return {'CANCELLED'}

        # Get items to rename
        items = self.get_items(context, props)
        if not items:
            self.report({'WARNING'}, f"No {item_type}s to rename")
            return {'CANCELLED'}

        # Pre-rename hook
        self.pre_rename_hook(context, items)

        # Perform renaming
        results = RenameEngine.rename_items(items, self.operation, config)

        # Post-rename hook
        self.post_rename_hook(context, results)

        # Report results
        changed = sum(1 for r in results if r.was_changed)
        errors = [r for r in results if not r.success]

        if errors:
            self.report({'ERROR'}, f"Errors: {errors[0].error}")
            return {'CANCELLED'}

        self.report({'INFO'}, f"Renamed {changed} {item_type}(s)")
        return {'FINISHED'}
