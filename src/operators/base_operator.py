"""Base operator class for all renaming operations."""
from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING, Any

import bpy
from bpy.types import Operator, Context

from ..core.rename_engine import RenameEngine, RenameOperation, RenameConfig, RenameResult

if TYPE_CHECKING:
    from bpy.types import PropertyGroup

# How many taken names a report lists before "and N more"
MAX_LISTED_NAMES = 3


def skipped_message(item_type: str, changed: int, taken: list[str]) -> str:
    """
    Build the report for a rename that skipped names already in use.

    Parameters
    ----------
    item_type : str
        Kind of item, e.g. "mesh".
    changed : int
        Number of items renamed.
    taken : list of str
        Names of the items left as they were.

    Returns
    -------
    str
        For example "Renamed 2 mesh(s); 1 skipped, name already used: 'Body'".
    """
    listed = ", ".join(f"'{name}'" for name in taken[:MAX_LISTED_NAMES])
    if len(taken) > MAX_LISTED_NAMES:
        listed += f", and {len(taken) - MAX_LISTED_NAMES} more"
    return (f"Renamed {changed} {item_type}(s); {len(taken)} skipped, "
            f"name already used: {listed}")


def report_outcome(item_type: str, results: list[RenameResult],
                   extra_taken: list[str]) -> tuple[str, str, set[str]]:
    """
    Choose the report and the operator result after a rename.

    An operator that renamed something must finish, so that Blender adds an
    undo step for it, even when other items failed.

    Parameters
    ----------
    item_type : str
        Kind of item, e.g. "mesh".
    results : list of RenameResult
        One result per item.
    extra_taken : list of str
        Further names left as they were because their new name was taken
        (for example objects in Sync Object Names).

    Returns
    -------
    tuple of (str, str, set of str)
        The report level ('INFO', 'WARNING' or 'ERROR'), the message, and
        ``{'FINISHED'}`` or ``{'CANCELLED'}``.
    """
    changed = sum(1 for r in results if r.was_changed)
    errors = [r for r in results if not r.success]
    taken = [r.old_name for r in results if r.taken] + list(extra_taken)

    if errors:
        message = f"Errors: {errors[0].error}"
        if changed:
            return 'WARNING', f"Renamed {changed} {item_type}(s); {message}", {'FINISHED'}
        return 'ERROR', message, {'CANCELLED'}
    if taken:
        return 'WARNING', skipped_message(item_type, changed, taken), {'FINISHED'}
    return 'INFO', f"Renamed {changed} {item_type}(s)", {'FINISHED'}


def id_name_taken(collection: Any, item: Any, name: str) -> bool:
    """
    Tell whether another data-block of the same kind and library uses a name.

    Parameters
    ----------
    collection : bpy.types.bpy_prop_collection
        The data-blocks of this kind, e.g. ``bpy.data.meshes``.
    item : bpy.types.ID
        The data-block about to be renamed.
    name : str
        Its new name.

    Returns
    -------
    bool
        True when a different data-block in the same library (or local
        file) already has ``name``.
    """
    library = item.library.filepath if item.library else None
    other = collection.get((name, library))
    return other is not None and other != item


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

    def name_taken(self, context: Context, item: Any, name: str) -> bool:
        """
        Tell whether another item already uses a name.

        Override for each kind of item; the base version never finds one.

        Parameters
        ----------
        context : bpy.types.Context
            Current Blender context.
        item : Any
            The item about to be renamed.
        name : str
            Its new name.

        Returns
        -------
        bool
            True when another item of the same kind already uses ``name``.
        """
        return False

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

        # Perform renaming; hooks add the names they could not use here
        self._taken_names = []
        results = RenameEngine.rename_items(
            items, self.operation, config,
            name_taken=lambda item, name: self.name_taken(context, item, name))

        # Post-rename hook
        self.post_rename_hook(context, results)

        # Report results
        level, message, outcome = report_outcome(item_type, results, self._taken_names)
        self.report({level}, message)
        return outcome
