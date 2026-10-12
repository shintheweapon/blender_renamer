# Blender Renamer

**Batch rename bones, materials, meshes, and objects with regex and CSV support**

[![Version](https://img.shields.io/badge/version-0.2.0-blue.svg)](https://github.com/theweapon/blender_renamer)
[![Blender](https://img.shields.io/badge/blender-4.2.0+-orange.svg)](https://www.blender.org/)
[![License](https://img.shields.io/badge/license-GPL--3.0-green.svg)](LICENSE)

Blender Renamer is a blender addon that provides unified batch renaming functionality for bones, materials, mesh datablocks, and objects.

## Features

### Core Renaming Operations

All four renamers (Bones, Materials, Meshes, Objects) provide:
- **Search & Replace**: Find and replace text with optional regex patterns
- **Add Prefix**: Prepend text to names
- **Add Suffix**: Append text to names
- **Add Prefix & Suffix**: Apply both simultaneously
- **Regex Support**: Pattern matching with capture groups (`\1`, `\2`, etc.)
- **Undo Support**: All operations work with Ctrl+Z

<!-- ### Specialized Renamers -->

**Bone Renamer**
- Unique feature: CSV bulk import for mapping files (Custom_Bones →
  FS_Bones) with optional slient mode
- Target: All Bones or Selected Bones (for none CSV rename)
- Requirements: Armature in Edit Mode

**Material Renamer**
- Unique: Include Unused option to process materials with 0 users
- Target: All Materials, Selected Objects, or Active Object

**Mesh Renamer**
- Renames the mesh data (the green triangle in the Outliner), not the object; for object names use the Object Renamer
- Unique: Sync Object Names, Include Linked mesh handling
- Target: All Meshes, Selected Objects, or Active Object

**Object Renamer**
- Renames objects (the orange triangle in the Outliner)
- Target: All Objects, Selected Objects, or Active Object
- Linked (library) objects are skipped, because Blender cannot rename them

**Internationalisation**
- English
- 简体中文

## Requirements

- **Blender Version**: Recommend 4.2.0 or later (legacy support for 3.0.0+)

## Quick Start

1. Select your armature, objects, or materials
2. Press `N` to open the sidebar → Navigate to **Renamer** tab
3. Choose your target renamer panel (Bone/Material/Mesh/Object, Bone renaming
   only available in Edit mode   )
4. Select operation type and configure options
5. Click the operation button to apply changes

## CSV Import (Bones Only)

The CSV import feature allows bulk renaming of bones using a mapping file, designed for standardised rig naming conventions.

### Format Specification

Two-column CSV with header row:

```csv
Custom_Bones,FS_Bones
Bip001-Spine,Spine
Bip001-L-UpperArm,L_UpperArm
Bip001-R-UpperArm,R_UpperArm
Bip001-Neck,Neck
```

- **Column 1**: Current bone name (Custom_Bones)
- **Column 2**: New bone name (FS_Bones)
- **Header Row**: Required (first row is skipped)
- **Empty Cells**: Automatically skipped during processing

### Encoding Support

The parser automatically detects and handles multiple encodings:

- UTF-8 (with/without BOM)
- UTF-16 LE/BE (Excel export format)
- Windows CP1252
- Latin-1

### Usage

1. Prepare your CSV file following the format above
2. Select armature in Edit Mode
3. Open Bone Renamer panel
4. Click file picker and select your CSV file
5. Optional: Enable **Silent Mode** to skip confirmation dialog
6. Click **Import & Rename**

The addon validates bone existence before renaming and displays a confirmation dialog showing the number of bones to be renamed.
A bone whose new name another bone already uses is skipped and reported (see [Names already in use](#names-already-in-use)), so a CSV that swaps two names changes neither.

## Names already in use

Blender lets each name exist only once per kind: one object `Body`, one mesh `Body`, one bone `Arm` per armature.
When a new name is already used by another item of the same kind, the renamer leaves that item as it was and reports
it, for example `Renamed 2 mesh(s); 1 skipped, name already used: 'Body.001'`. No other item is changed. Rename or
remove the other item first, then run the rename again.

### Example Bone CSV File

See [example_bone_dict.csv](example_bone_dict.csv) for an example reference with 85 bone mappings.

## Regex Patterns

All Search & Replace operations support Python regular expressions when
**Use Regex** is enabled.


### Example: Regex Pattern Renaming

Convert bone suffixes from `_R`/`_L` to `.R`/`.L` notation:

1. Select armature in Edit Mode
2. Open Bone Renamer panel
3. Enable **Use Regex** checkbox
4. **Search**: `^(.*)_([LR])$`
5. **Replace**: `\1.\2`
6. Click **Search & Replace**

Result: `bone_R` → `bone.R`, `bone_L` → `bone.L`

### Common Patterns

**Remove prefix/suffix**:
- Pattern: `^prefix_(.*)$` → Replace: `\1` (removes "prefix_")
- Pattern: `^(.*)_suffix$` → Replace: `\1` (removes "_suffix")

**Swap sides**:
- Pattern: `^L_(.*)$` → Replace: `R_\1` (change L_ to R_)

**Add separators**:
- Pattern: `^([A-Z]+)(\d+)$` → Replace: `\1_\2` (ARM01 → ARM_01)

**Capture groups**:
- Use `\1`, `\2`, `\3`, etc. to reference captured groups in parentheses

### Tips

- Test patterns on a few selected items first
- Enable regex only when needed (plain text search is faster)
- Use case-insensitive mode for flexible matching
- All operations support undo (Ctrl+Z) if results are unexpected