# Changelog

## 0.2.0 (unreleased)

### Fixed
- A new name already used by another item of the same kind (object, mesh, material, or a bone of the same armature)
  no longer gets Blender's number added. The item is left as it was, and the report lists the names skipped. Before,
  for example, removing `.001` while `Body` existed left `Body.001` and still reported it as renamed.
- Sync Object Names skips an object whose new name another object uses, and reports it.
- CSV import skips a bone whose new name another bone uses, so a CSV that swaps two names changes neither. Before, a
  swap gave names such as `Spine.001`.

### Added
- Tests, run inside Blender: `blender.exe --factory-startup -b -P tests/run_tests.py`.
- The extension build leaves out `tests/` and `.gitignore`.

## 0.1.0

### Added
- Bone, Material and Mesh Renamer panels in the 3D Viewport sidebar tab "Renamer": Search & Replace (plain text or
  regex), Add Prefix, Add Suffix, Add Prefix & Suffix.
- Bone CSV import with a confirmation dialog or Silent Mode.
- Material option Include Unused; Mesh options Sync Object Names and Include Linked.
- Simplified Chinese interface.
