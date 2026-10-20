"""
Blender Renamer: batch renaming for bones, materials, meshes and objects.

This addon provides consistent batch renaming functionality across
multiple Blender data types with shared UI patterns and regex support.
"""

import importlib
import sys

# Get the addon package name for proper imports
package_name = __name__


def _get_submodule_names() -> list[str]:
    """Get list of submodule names in dependency order."""
    return [
        ".core",
        ".core.i18n",
        ".core.rename_engine",
        ".properties",
        ".properties.base_properties",
        ".properties.bone_properties",
        ".properties.material_properties",
        ".properties.mesh_properties",
        ".properties.object_properties",
        ".operators",
        ".operators.base_operator",
        ".operators.bone_operators",
        ".operators.material_operators",
        ".operators.mesh_operators",
        ".operators.object_operators",
        ".ui",
        ".ui.panel_base",
        ".ui.bone_panel",
        ".ui.material_panel",
        ".ui.mesh_panel",
        ".ui.object_panel",
    ]


def _reload_submodules() -> None:
    """Reload all submodules when addon is refreshed."""
    for name in _get_submodule_names():
        full_name = package_name + name
        if full_name in sys.modules:
            importlib.reload(sys.modules[full_name])


# Handle reloading: bpy is already in this module's namespace only when Blender
# refreshes the addon, so this runs on a refresh and not on the first load
if "bpy" in locals():
    _reload_submodules()

import bpy  # noqa: E402

from . import ui  # noqa: E402
from . import operators  # noqa: E402
from . import properties  # noqa: E402
from .core import i18n  # noqa: E402

bl_info = {
    "name": "Blender Renamer",
    "author": "theweapon",
    "version": (0, 2, 0),
    "blender": (4, 2, 0),
    "location": "View3D > Sidebar > Renamer",
    "description": "Batch rename bones, materials, meshes, and objects with regex support",
    "category": "Rigging",
    "doc_url": "",
    "tracker_url": "",
}


def register() -> None:
    """Register all addon classes and properties."""
    i18n.register()
    # Register in dependency order: properties first, then operators, then UI
    properties.register()
    operators.register()
    ui.register()


def unregister() -> None:
    """Unregister all addon classes and properties."""
    # Unregister in reverse order
    ui.unregister()
    operators.unregister()
    properties.unregister()
    i18n.unregister()


if __name__ == "__main__":
    register()
