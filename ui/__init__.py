"""UI panel registration."""
from . import bone_panel
from . import material_panel
from . import mesh_panel


def register() -> None:
    """Register all UI panels."""
    bone_panel.register()
    material_panel.register()
    mesh_panel.register()


def unregister() -> None:
    """Unregister all UI panels."""
    mesh_panel.unregister()
    material_panel.unregister()
    bone_panel.unregister()
