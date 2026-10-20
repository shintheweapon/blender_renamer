"""Property group registration."""
from . import bone_properties
from . import material_properties
from . import mesh_properties
from . import object_properties


def register() -> None:
    """Register all property groups."""
    bone_properties.register()
    material_properties.register()
    mesh_properties.register()
    object_properties.register()


def unregister() -> None:
    """Unregister all property groups."""
    object_properties.unregister()
    mesh_properties.unregister()
    material_properties.unregister()
    bone_properties.unregister()
