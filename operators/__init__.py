"""Operator registration."""
from . import bone_operators
from . import material_operators
from . import mesh_operators


def register() -> None:
    """Register all operators."""
    bone_operators.register()
    material_operators.register()
    mesh_operators.register()


def unregister() -> None:
    """Unregister all operators."""
    mesh_operators.unregister()
    material_operators.unregister()
    bone_operators.unregister()
