import os
import sys
from pathlib import Path


def get_divine_path() -> Path:
    divine_path = os.getenv("DIVINE_PATH")

    if divine_path is None:
        raise OSError("DIVINE_PATH environment variable is not set.")

    return Path(divine_path)


def get_mod_name() -> str:
    mod_name = os.getenv("MOD_NAME")

    if mod_name is None:
        raise OSError("MOD_NAME environment variable is not set.")

    return mod_name


def get_unpacked_data_path() -> Path:
    unpacked_data_path = os.getenv("UNPACKED_DATA_PATH")

    if unpacked_data_path is None:
        raise OSError("UNPACKED_DATA_PATH environment variable is not set.")

    return Path(unpacked_data_path)


def get_data_path() -> Path:
    data_path = os.getenv("DATA_PATH")

    if data_path is None:
        raise OSError("DATA_PATH environment variable is not set.")

    return Path(data_path)


def get_dialog_binaries_paths() -> list[Path]:
    return [
        Path(
            get_unpacked_data_path()
            / "Gustav/Mods/GustavDev/Story/DialogsBinary"
        ),
        Path(
            get_unpacked_data_path() / "Gustav/Mods/Gustav/Story/DialogsBinary"
        ),
    ]


def get_translations_path() -> Path:
    return Path(
        get_unpacked_data_path() / "English/Localization/English/english.loca"
    )


def get_mocaps_path() -> Path:
    return Path(
        get_unpacked_data_path()
        / "English_Animations/Mods/Gustav/Localization/English/Animation"
    )


def get_character_visuals_paths() -> list[Path]:
    return [
        Path(
            get_unpacked_data_path()
            / "Gustav/Public/GustavDev/Content"
            / "[PAK]_CharacterVisuals/_merged.lsf"
        ),
        Path(
            get_unpacked_data_path()
            / "Gustav/Public/Gustav/Content"
            / "[PAK]_CharacterVisuals/_merged.lsf"
        ),
    ]


def get_base_body_path() -> Path:
    return Path(
        get_unpacked_data_path()
        / "Shared/Public/Shared/Content/Assets/Characters"
    )


def get_unpacked_cinematic_anims_paths():
    return [
        Path(
            get_unpacked_data_path()
            / "Models/Public/Shared/Assets/Characters/_Anims/_Cinematic"
        ),
        Path(
            get_unpacked_data_path()
            / "Models/Public/SharedDev/Assets/Characters/_Anims/_Cinematic"
        ),
    ]


def get_resource_path(relative_path=""):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return Path(os.path.join(base_path, relative_path))


def get_translations_output_path() -> Path:
    return Path(get_resource_path() / "parsed" / "english.xml")


def get_animation_metadata_template_path() -> Path:
    return Path(
        get_resource_path() / "template_files" / "animation_template.lsx"
    )


def get_cinematic_anims_path() -> Path:
    return Path(
        get_data_path()
        / f"Public/{get_mod_name()}/Assets/Characters/_Anims/_Cinematic"
    )


def get_animation_metadata_path() -> Path:
    return Path(
        get_data_path() / f"Public/{get_mod_name()}/Content/Assets/Characters"
    )
