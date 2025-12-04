import os
import shutil
from pathlib import Path

from infernal_engine.utils.settings import (
    get_animation_metadata_path,
    get_cinematic_anims_path,
    get_mocaps_path,
    get_resource_path,
)


def find_file_path(file_name, paths) -> Path:
    for dialog_binaries_path in paths:
        for root, _, files in os.walk(dialog_binaries_path):
            for name in files:
                if name.replace(".lsf", "") == file_name:
                    file_path = Path(os.path.abspath(os.path.join(root, name)))

    if not file_path:
        raise OSError(f"Could not find file: {file_name}")

    return file_path


def construct_parsed_dialog_file_path(dialog_file: str) -> Path:
    parsed_dialog_file_path = (
        get_resource_path() / "parsed" / "dialogs" / f"{dialog_file}.lsx"
    )

    return parsed_dialog_file_path


def construct_mocap_path(speaker, handle) -> Path:
    return Path(
        get_mocaps_path() / "MC_v"
        f"{speaker['character_guid'].replace('-', '')}"
        "_"
        f"{handle}"
        ".GR2"
    )


def construct_animation_path(
    scene_info: dict,
    character: dict,
) -> Path:
    filename = (
        f"{character['rig']}_SCENE_{scene_info['scene']}"
        f"_{scene_info['action']}.GR2"
    )

    return Path(
        get_cinematic_anims_path()
        / scene_info["act"]
        / scene_info["area"]
        / scene_info["scene"]
        / character["rig"]
        / filename
    )


def construtct_animation_metadata_lsf_path(
    animation_info: dict,
    animation_guid: str,
) -> Path:
    animation_metadata_lsf_path = Path(
        get_animation_metadata_path()
        / animation_info["race_long"]
        / f"[PAK]_{animation_info['body_type_long']}_Cine"
        / f"{animation_guid}.lsf"
    )

    return animation_metadata_lsf_path


# https://www.howtogeek.com/266621/how-to-make-windows-10-accept-file-paths-over-260-characters/


def copy_animation(animation_info):
    os.makedirs(
        os.path.dirname(animation_info["animation_path"]), exist_ok=True
    )
    shutil.copyfile(
        animation_info["mocap_path"],
        animation_info["animation_path"],
    )
