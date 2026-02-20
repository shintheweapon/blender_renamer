"""
Blender Renamer - Batch renaming for bones, materials, and meshes.

This addon provides consistent batch renaming functionality across
multiple Blender data types with shared UI patterns and regex support.
"""

from . import ui
from . import operators
from . import properties
from .core import i18n
import bpy
import sys
import importlib
bl_info = {
    "name": "Blender Renamer",
    "author": "theweapon",
    "version": (0, 1, 0),
    "blender": (3, 0, 0),
    "location": "View3D > Sidebar > Renamer",
    "description": "Batch rename bones, materials, and meshes with regex support",
    "category": "Rigging",
    "doc_url": "",
    "tracker_url": "",
}

# Handle reloading for Blender's addon refresh

# Get the addon package name for proper imports
package_name = __name__


def _get_submodule_names() -> list[str]:
    """Get list of submodule names in dependency order."""
    return [
        ".core",
        ".core.i18n",
        ".core.rename_engine",
        ".core.version_compat",
        ".properties",
        ".properties.base_properties",
        ".properties.bone_properties",
        ".properties.material_properties",
        ".properties.mesh_properties",
        ".operators",
        ".operators.base_operator",
        ".operators.bone_operators",
        ".operators.material_operators",
        ".operators.mesh_operators",
        ".ui",
        ".ui.panel_base",
        ".ui.bone_panel",
        ".ui.material_panel",
        ".ui.mesh_panel",
    ]


def _reload_submodules() -> None:
    """Reload all submodules when addon is refreshed."""
    for name in _get_submodule_names():
        full_name = package_name + name
        if full_name in sys.modules:
            importlib.reload(sys.modules[full_name])


# Handle reloading - check if bpy is already imported (addon refresh)
if "bpy" in locals():
    _reload_submodules()

# Now import after potential reload


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
