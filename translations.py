# FIXME: translations are only loaded after a restart, or at least after a
# reload of the addon.
from bpy.app.translations import locale

# I don't know how to have Blender copy a JSON file when installing the addon,
# so we'll have to include this in here.
translations = {
    "en_US": {
        "panel-label": "Pseudo Vertical Writing",
        "to-vertical-label": "To pseudo vertical",
        "to-vertical-description": "Convert to vertical writing",
        "to-horizontal-label": "Back to horizontal",
        "to-horizontal-description": "Convert back to horizontal writing, when editing can actually be done",
    },
    "zh_TW": {
        "panel-label": "偽直書",
        "to-vertical-label": "轉換成直書",
        "to-vertical-description": "在對的地方換行，模擬直書",
        "to-horizontal-label": "恢復成橫書",
        "to-horizontal-description": "恢復成橫書方便編輯",
    },
    "ja_JP": {
        "panel-label": "縦書き変換",
        "to-vertical-label": "縦書き（仮）に",
        "to-vertical-description": "改行することで縦書きを擬態する",
        "to-horizontal-label": "横書きに",
        "to-horizontal-description": "編集するため横書きに戻す",
    },
}


def t(strid):
    """Return translation for `strid`.

    Falls back to English if the translation is not found."""
    try:
        return translations[locale][strid]
    except KeyError:
        return translations["en_US"][strid]
