from pathlib import Path

MOD_NAME = "ReturnToTheHouseOfHope_295379f9-b5ee-119f-54c1-9f6bd887046b"

DATA_PATH = Path("C:/Program Files (x86)/Steam/steamapps/common/Baldurs Gate 3/Data")
UNPACKED_DATA_PATH = Path("C:/Users/Shadow/bg3-modders-multitool/UnpackedData")

DIALOG_BINARIES_PATHS = [
    Path(UNPACKED_DATA_PATH / "Gustav/Mods/GustavDev/Story/DialogsBinary")
]

TRANSLATIONS_PATH = Path(
    UNPACKED_DATA_PATH / "English/Localization/English/english.loca"
)

MOCAPS_PATH = Path(
    UNPACKED_DATA_PATH / "English_Animations/Mods/Gustav/Localization/English/Animation"
)

CHARACTER_VISUALS_PATH = Path(
    UNPACKED_DATA_PATH
    / "Gustav/Public/GustavDev/Content/[PAK]_CharacterVisuals/_merged.lsf"
)

BASE_BODY_PATH = Path(
    UNPACKED_DATA_PATH / "Shared/Public/Shared/Content/Assets/Characters"
)


BASE_OUTPUT_PATH = Path(DATA_PATH / "Helpers")

TRANSLATIONS_OUTPUT_PATH = Path(BASE_OUTPUT_PATH / "parsed" / "english.xml")

ANIMATION_METADATA_TEMPLATE_PATH = Path(
    BASE_OUTPUT_PATH / "template_files" / "animation_template.lsx"
)

CINEMATIC_ANIMS_PATH = Path(
    DATA_PATH / f"Public/{MOD_NAME}/Assets/Characters/_Anims/_Cinematic"
)

ANIMATION_METADATA_PATH = Path(
    DATA_PATH / f"Public/{MOD_NAME}/Content/Assets/Characters"
)
