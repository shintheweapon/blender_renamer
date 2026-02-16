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
    ) -> list[RenameResult]:
        """
        Rename a sequence of items.

        Args:
            items: Sequence of items to rename
            operation: The type of rename operation
            config: Configuration for the operation
            name_getter: Optional custom function to get name (default: item.name)
            name_setter: Optional custom function to set name (default: item.name = x)

        Returns:
            List of RenameResult objects describing each operation
        """
        results: list[RenameResult] = []

        get_name = name_getter or (lambda x: x.name)
        set_name = name_setter or (lambda x, n: setattr(x, 'name', n))

        for item in items:
            old_name = get_name(item)
            new_name, error = cls.compute_new_name(old_name, operation, config)

            if error:
                results.append(RenameResult(old_name, old_name, False, error))
                continue

            if new_name != old_name:
                try:
                    set_name(item, new_name)
                    results.append(RenameResult(old_name, new_name, True))
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
