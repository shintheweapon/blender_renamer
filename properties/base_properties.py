"""Base properties shared across all renamer types."""
from __future__ import annotations

from bpy.props import StringProperty, BoolProperty
from bpy.types import PropertyGroup


class BaseRenamerProperties(PropertyGroup):
    """
    Base properties for all renaming operations.

    This class is NOT registered directly - it serves as a base for
    the specific property groups (bone, material, mesh).
    """

    # Search & Replace
    search_text: StringProperty(
        name="Search",
        description="Text to search for",
        default=""
    )

    replace_text: StringProperty(
        name="Replace",
        description="Text to replace with",
        default=""
    )

    use_regex: BoolProperty(
        name="Use Regex",
        description="Enable regular expression pattern matching",
        default=False
    )

    case_sensitive: BoolProperty(
        name="Case Sensitive",
        description="Make search case-sensitive (only for non-regex)",
        default=True
    )

    # Prefix & Suffix
    prefix_text: StringProperty(
        name="Prefix",
        description="Text to add before names",
        default=""
    )

    suffix_text: StringProperty(
        name="Suffix",
        description="Text to add after names",
        default=""
    )
