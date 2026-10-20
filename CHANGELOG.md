# Changelog

## Unreleased

### Changed
- The add-on's files are in `src/`; `build.ps1` builds `dist/blender_renamer-<version>.zip` and checks its layout.
  The zip holds only the add-on: the README, changelog, licence text and example CSV stay in the repository.

## 0.2.0

### Added
- **Object Renamer** panel: the same operations for object names (the orange triangle in the Outliner), with Target
  All Objects, Selected Objects or Active Object. Linked (library) objects are skipped. The Mesh Renamer renames mesh
  data (the green triangle) only.
- Chinese uses 物体 for Object, as Blender does; the Sync Object Names label now says 同步物体名称.
- Tests, run inside Blender: `blender.exe --factory-startup -b -P tests/run_tests.py`.
- The extension build leaves out `tests/` and `.gitignore`.

### Changed
- The add-on reloads its modules only when Blender refreshes it, not on the first load.
- `bl_info` names Blender 4.2 as the minimum, as the manifest does.
- README: the license link, the repository link, the count of example CSV mappings (83), the supported Blender
  versions, and two typos.

### Removed
- `core/version_compat.py`, which nothing used, and the obsolete `zh_CN` locale id (Blender uses `zh_HANS`).
- The Mesh Renamer's **Include Linked** option. Blender cannot rename linked (library) meshes, so the option could
  only cause errors; linked meshes are always skipped.

### Fixed
- Sync Object Names did nothing with Target All Meshes; it now renames the object of each mesh, as with Selected and
  Active.
- Case-insensitive Search & Replace read the Replace text as a regular expression template, so a backslash in it
  failed (for example `\1`). The Replace text is now used as it is.
- All Materials renamed the local materials, then stopped with an error at a linked material and left no undo step.
  Linked materials are now skipped. When some items are renamed and others fail, the command still finishes, so
  Ctrl+Z undoes the renames.
- Tooltips were English in the Chinese interface: command tooltips were stored only where Blender looks up command
  labels, and option and target-choice tooltips had no translation. All 52 such texts, and the option name
  "CSV File", now show Chinese.
- CSV import reads the CSV again when it runs without the pairs from its first step, as a repeated command (Repeat
  Last) does. Before, it could only report "No mappings available".
- A new name already used by another item of the same kind (object, mesh, material, or a bone of the same armature)
  no longer gets Blender's number added. The item is left as it was, and the report lists the names skipped. Before,
  for example, removing `.001` while `Body` existed left `Body.001` and still reported it as renamed.
- Sync Object Names skips an object whose new name another object uses, and reports it.
- CSV import skips a bone whose new name another bone uses, so a CSV that swaps two names changes neither. Before, a
  swap gave names such as `Spine.001`.

## 0.1.0

### Added
- Bone, Material and Mesh Renamer panels in the 3D Viewport sidebar tab "Renamer": Search & Replace (plain text or
  regex), Add Prefix, Add Suffix, Add Prefix & Suffix.
- Bone CSV import with a confirmation dialog or Silent Mode.
- Material option Include Unused; Mesh options Sync Object Names and Include Linked.
- Simplified Chinese interface.
