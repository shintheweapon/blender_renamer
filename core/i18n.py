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
    """Build Operator context map."""
    return {("Operator", source): target for source, target in translations.items()}


_UI_TRANSLATIONS_ZH_CN = {
    "Bone Renamer": "骨骼重命名",
    "Material Renamer": "材质重命名",
    "Mesh Renamer": "网格重命名",
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
    "Include Unused": "包含未使用的",
    "All Bones": "所有骨骼",
    "Selected Bones": "选定的骨骼",
    "Silent Mode": "静默模式（不显示确认提示）",
    "Sync Object Names (mesh is the green delta, object is the orange delta)": "同步对象名称（网格是绿色三角，对象是橙色三角）",
    "Include Linked": "包含链接的",
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
    "All Meshes": "所有网格",
    "All Materials": "所有材质",
    "Include Unused": "包含未使用的",
    "Sync Object Names (mesh is the green delta, object is the orange delta)": "同步对象名称（网格是绿色三角，对象是橙色三角）",
    "Include Linked": "包含链接的",

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
