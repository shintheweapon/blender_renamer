"""Addon UI translations."""
from __future__ import annotations

from bpy.app.translations import register as _register
from bpy.app.translations import unregister as _unregister

TRANSLATION_DOMAIN = (__package__ or "blender_renamer").split(".")[0]


def _build_ui_map(translations: dict[str, str]) -> dict[tuple[str, str], str]:
    """Build UI context map with both UI and * contexts."""
    mapped: dict[tuple[str, str], str] = {}
    for source, target in translations.items():
        mapped[("UI", source)] = target
        mapped[("*", source)] = target
    return mapped


def _build_operator_map(translations: dict[str, str]) -> dict[tuple[str, str], str]:
    """Build the map for command texts: labels are looked up in the Operator
    context, tooltips in the default * context, so add both."""
    mapped: dict[tuple[str, str], str] = {}
    for source, target in translations.items():
        mapped[("Operator", source)] = target
        mapped[("*", source)] = target
    return mapped


_UI_TRANSLATIONS_ZH_CN = {
    "Bone Renamer": "骨骼重命名",
    "Material Renamer": "材质重命名",
    "Mesh Renamer": "网格重命名",
    "Object Renamer": "物体重命名",
    "Target": "目标",
    "Search & Replace:": "搜索并替换：",
    "Prefix & Suffix:": "前缀与后缀：",
    "Tips:": "提示：",
    "Options:": "选项：",
    "CSV Import:": "CSV 批量导入：",
    "Import & Rename": "批量导入并重命名",
    "Format: Custom_Bones,FS_Bones": "CSV格式：Custom_Bones,FS_Bones（第一列将被重命名为第二列）",
    "Switch to Edit Mode": "切换到编辑模式",
    "Total materials in file": "文件中的材质总数",
    "Total meshes in file": "文件中的网格总数",
    "Total objects in file": "文件中的物体总数",
    "Enable regex for patterns like ^(.*)$": "启用正则表达式以使用如 ^(.*)$ 的模式",
    "Use \\1, \\2 for regex groups": "使用 \\1、\\2 引用正则表达式分组",
    "Operations support undo (Ctrl+Z)": "操作支持撤销（Ctrl+Z）",
    "CSV: Empty Custom_Bones cells are skipped": "CSV：空的 Custom_Bones 将被跳过",
    "Are you sure to mass rename bones?": "确定要批量重命名骨骼吗？",
    "Rename {count} bone(s)": "重命名 {count} 个骨骼",
    "This operation can be undone with Ctrl+Z": "此操作可通过 Ctrl+Z 撤销",
    "Use Regex": "使用正则表达式",
    "All Meshes": "所有网格",
    "All Materials": "所有材质",
    "All Objects": "所有物体",
    "Include Unused": "包含未使用的",
    # Option and target-choice tooltips
    "CSV File": "CSV 文件",
    "Also rename the parent object to match the mesh name": "同时将物体重命名为与网格相同的名称",
    "Enable regular expression pattern matching": "启用正则表达式匹配",
    "Include materials with no users (0 users)": "包含没有用户（0 个用户）的材质",
    "Make search case-sensitive (only for non-regex)": "搜索时区分大小写（仅用于非正则表达式）",
    "Path to CSV file with bone rename mappings (Custom_Bones,FS_Bones)": "骨骼重命名映射 CSV 文件的路径（Custom_Bones,FS_Bones）",
    "Skip confirmation dialog and apply CSV renames immediately": "跳过确认对话框，立即按 CSV 重命名",
    "Text to replace with": "用于替换的文本",
    "Text to search for in bone names": "要在骨骼名称中搜索的文本",
    "Text to add before bone names": "添加在骨骼名称之前的文本",
    "Text to add after bone names": "添加在骨骼名称之后的文本",
    "Text to search for in material names": "要在材质名称中搜索的文本",
    "Text to add before material names": "添加在材质名称之前的文本",
    "Text to add after material names": "添加在材质名称之后的文本",
    "Text to search for in mesh names": "要在网格名称中搜索的文本",
    "Text to add before mesh names": "添加在网格名称之前的文本",
    "Text to add after mesh names": "添加在网格名称之后的文本",
    "Text to search for in object names": "要在物体名称中搜索的文本",
    "Text to add before object names": "添加在物体名称之前的文本",
    "Text to add after object names": "添加在物体名称之后的文本",
    "Which bones to rename": "要重命名哪些骨骼",
    "Which materials to rename": "要重命名哪些材质",
    "Which objects to rename": "要重命名哪些物体",
    "Which mesh datablocks to rename": "要重命名哪些网格数据块",
    "Rename all bones in the armature": "重命名骨架中的所有骨骼",
    "Rename only selected bones": "只重命名选定的骨骼",
    "Rename all materials in the file": "重命名文件中的所有材质",
    "Rename materials on selected objects": "重命名选定物体上的材质",
    "Rename materials on the active object only": "只重命名活动物体上的材质",
    "Rename all mesh datablocks in the file": "重命名文件中的所有网格数据块",
    "Rename meshes of selected objects": "重命名选定物体的网格",
    "Rename mesh of the active object only": "只重命名活动物体的网格",
    "Rename all objects in the file": "重命名文件中的所有物体",
    "Rename selected objects": "重命名选定的物体",
    "Rename the active object only": "只重命名活动物体",
    "All Bones": "所有骨骼",
    "Selected Bones": "选定的骨骼",
    "Silent Mode": "静默模式（不显示确认提示）",
    "Sync Object Names (mesh is the green delta, object is the orange delta)": "同步物体名称（网格是绿色三角，物体是橙色三角）",
}

_OPERATOR_TRANSLATIONS_ZH_CN = {
    "Search & Replace": "搜索并替换",
    "Use Regex": "使用正则表达式",
    "Search and replace text in bone names": "在骨骼名称中搜索并替换文本",
    "Add Prefix": "添加前缀",
    "Add prefix to bone names": "为骨骼名称添加前缀",
    "Add Suffix": "添加后缀",
    "Add suffix to bone names": "为骨骼名称添加后缀",
    "Add Prefix & Suffix": "添加前缀与后缀",
    "Add both prefix and suffix to bone names": "为骨骼名称同时添加前缀与后缀",
    "Import CSV Renames": "导入 CSV 批量重命名",
    "Rename bones using CSV mapping file (Custom_Bones -> FS_Bones)": "使用 CSV 映射文件重命名骨骼（Custom_Bones -> FS_Bones）",
    "Search and replace text in material names": "在材质名称中搜索并替换文本",
    "Add prefix to material names": "为材质名称添加前缀",
    "Add suffix to material names": "为材质名称添加后缀",
    "Add both prefix and suffix to material names": "为材质名称同时添加前缀与后缀",
    "Search and replace text in mesh datablock names": "在网格数据块名称中搜索并替换文本",
    "Add prefix to mesh datablock names": "为网格数据块名称添加前缀",
    "Add suffix to mesh datablock names": "为网格数据块名称添加后缀",
    "Add both prefix and suffix to mesh datablock names": "为网格数据块名称同时添加前缀与后缀",
    "Search and replace text in object names": "在物体名称中搜索并替换文本",
    "Add prefix to object names": "为物体名称添加前缀",
    "Add suffix to object names": "为物体名称添加后缀",
    "Add both prefix and suffix to object names": "为物体名称同时添加前缀与后缀",
    "All Objects": "所有物体",
    "All Meshes": "所有网格",
    "All Materials": "所有材质",
    "Include Unused": "包含未使用的",
    "Sync Object Names (mesh is the green delta, object is the orange delta)": "同步物体名称（网格是绿色三角，物体是橙色三角）",

}

_zh_hans_translations = {
    **_build_ui_map(_UI_TRANSLATIONS_ZH_CN),
    **_build_operator_map(_OPERATOR_TRANSLATIONS_ZH_CN),
}

TRANSLATIONS = {
    "zh_HANS": _zh_hans_translations,
    "zh_CN": _zh_hans_translations,
}


def register() -> None:
    """Register translation dictionary with Blender."""
    _register(TRANSLATION_DOMAIN, TRANSLATIONS)


def unregister() -> None:
    """Unregister translation dictionary."""
    _unregister(TRANSLATION_DOMAIN)
