"""Core renaming engine - pure Python, no Blender dependencies."""
from __future__ import annotations

import re
from dataclasses import dataclass
from enum import Enum, auto
from typing import Any, Callable, Sequence


class RenameOperation(Enum):
    """Types of renaming operations."""
    SEARCH_REPLACE = auto()
    ADD_PREFIX = auto()
    ADD_SUFFIX = auto()
    ADD_PREFIX_SUFFIX = auto()


@dataclass(frozen=True)
class RenameConfig:
    """Configuration for a rename operation."""
    search_text: str = ""
    replace_text: str = ""
    prefix_text: str = ""
    suffix_text: str = ""
    use_regex: bool = False
    case_sensitive: bool = True


@dataclass
class RenameResult:
    """Result of a rename operation."""
    old_name: str
    new_name: str
    success: bool
    error: str | None = None
    # The new name was already used by another item, so the item was left as it was
    taken: bool = False

    @property
    def was_changed(self) -> bool:
        """Check if the name was actually changed."""
        return self.success and self.old_name != self.new_name


class RenameEngine:
    """
    Core engine for performing rename operations.

    This class is stateless and operates on any object with a 'name' attribute.
    """

    @staticmethod
    def compute_new_name(
        old_name: str,
        operation: RenameOperation,
        config: RenameConfig
    ) -> tuple[str, str | None]:
        """
        Compute the new name without applying it.

        Args:
            old_name: The current name
            operation: The type of rename operation
            config: Configuration for the operation

        Returns:
            Tuple of (new_name, error_message). Error is None on success.
        """
        try:
            if operation == RenameOperation.SEARCH_REPLACE:
                return RenameEngine._search_replace(old_name, config), None
            elif operation == RenameOperation.ADD_PREFIX:
                return config.prefix_text + old_name, None
            elif operation == RenameOperation.ADD_SUFFIX:
                return old_name + config.suffix_text, None
            elif operation == RenameOperation.ADD_PREFIX_SUFFIX:
                return config.prefix_text + old_name + config.suffix_text, None
            else:
                return old_name, f"Unknown operation: {operation}"
        except re.error as e:
            return old_name, f"Regex error: {e}"
        except Exception as e:
            return old_name, f"Error: {e}"

    @staticmethod
    def _search_replace(name: str, config: RenameConfig) -> str:
        """Perform search and replace on a name."""
        if config.use_regex:
            return re.sub(config.search_text, config.replace_text, name)
        elif config.case_sensitive:
            return name.replace(config.search_text, config.replace_text)
        else:
            # Case-insensitive replacement
            pattern = re.compile(re.escape(config.search_text), re.IGNORECASE)
            return pattern.sub(config.replace_text, name)

    @classmethod
    def rename_items(
        cls,
        items: Sequence[Any],
        operation: RenameOperation,
        config: RenameConfig,
        name_getter: Callable[[Any], str] | None = None,
        name_setter: Callable[[Any, str], None] | None = None,
        name_taken: Callable[[Any, str], bool] | None = None,
    ) -> list[RenameResult]:
        """
        Rename a sequence of items.

        An item whose new name another item already uses is left as it was,
        and its result has ``taken`` set. After a rename the name is read
        back, so the result holds the name actually stored (Blender shortens
        long names).

        Parameters
        ----------
        items : sequence
            Items to rename.
        operation : RenameOperation
            The type of rename operation.
        config : RenameConfig
            Configuration for the operation.
        name_getter : callable, optional
            Get an item's name (default: ``item.name``).
        name_setter : callable, optional
            Set an item's name (default: ``item.name = new_name``).
        name_taken : callable, optional
            ``name_taken(item, new_name)`` is True when another item already
            uses ``new_name`` (default: never).

        Returns
        -------
        list of RenameResult
            One result per item, in the order of ``items``.
        """
        results: list[RenameResult] = []

        get_name = name_getter or (lambda x: x.name)
        set_name = name_setter or (lambda x, n: setattr(x, 'name', n))
        is_taken = name_taken or (lambda x, n: False)

        for item in items:
            old_name = get_name(item)
            new_name, error = cls.compute_new_name(old_name, operation, config)

            if error:
                results.append(RenameResult(old_name, old_name, False, error))
                continue

            if new_name != old_name:
                if is_taken(item, new_name):
                    results.append(RenameResult(old_name, old_name, True, taken=True))
                    continue
                try:
                    set_name(item, new_name)
                    results.append(RenameResult(old_name, get_name(item), True))
                except Exception as e:
                    results.append(RenameResult(old_name, old_name, False, str(e)))
            else:
                results.append(RenameResult(old_name, new_name, True))

        return results

    @classmethod
    def validate_config(
        cls,
        operation: RenameOperation,
        config: RenameConfig
    ) -> str | None:
        """
        Validate configuration before applying.

        Args:
            operation: The type of rename operation
            config: Configuration for the operation

        Returns:
            Error message if invalid, None if valid.
        """
        if operation == RenameOperation.SEARCH_REPLACE:
            if not config.search_text:
                return "Search text is empty"
            if config.use_regex:
                try:
                    re.compile(config.search_text)
                except re.error as e:
                    return f"Invalid regex pattern: {e}"

        elif operation == RenameOperation.ADD_PREFIX:
            if not config.prefix_text:
                return "Prefix text is empty"

        elif operation == RenameOperation.ADD_SUFFIX:
            if not config.suffix_text:
                return "Suffix text is empty"

        elif operation == RenameOperation.ADD_PREFIX_SUFFIX:
            if not config.prefix_text and not config.suffix_text:
                return "Both prefix and suffix are empty"

        return None
