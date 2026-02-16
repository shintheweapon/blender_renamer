"""Blender version compatibility utilities."""
from __future__ import annotations

import bpy

# Version tuple for comparisons
BLENDER_VERSION = bpy.app.version


def is_blender_3() -> bool:
    """Check if running Blender 3.x."""
    return 3 <= BLENDER_VERSION[0] < 4


def is_blender_4() -> bool:
    """Check if running Blender 4.x."""
    return 4 <= BLENDER_VERSION[0] < 5


def is_blender_4_2_plus() -> bool:
    """Check if running Blender 4.2+ (extension system)."""
    return BLENDER_VERSION >= (4, 2, 0)


def is_blender_5() -> bool:
    """Check if running Blender 5.x or later."""
    return BLENDER_VERSION[0] >= 5


def get_version_string() -> str:
    """Get Blender version as string."""
    return f"{BLENDER_VERSION[0]}.{BLENDER_VERSION[1]}.{BLENDER_VERSION[2]}"


# Panel constants - consistent across 3.x, 4.x, 5.x
PANEL_REGION_TYPE_UI = 'UI'
PANEL_SPACE_TYPE_VIEW3D = 'VIEW_3D'


def register_class_safe(cls: type) -> None:
    """Register a class with version-appropriate handling."""
    try:
        bpy.utils.register_class(cls)
    except ValueError as e:
        # Class might already be registered
        if "already registered" not in str(e).lower():
            raise


def unregister_class_safe(cls: type) -> None:
    """Unregister a class safely."""
    try:
        bpy.utils.unregister_class(cls)
    except RuntimeError:
        # Class might not be registered
        pass
