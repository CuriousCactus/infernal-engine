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
        for root, dirs, files in os.walk(dialog_binaries_path):
            for name in files:
                if name.replace(".lsf", "") == file_name:
                    return Path(os.path.abspath(os.path.join(root, name)))


def construct_parsed_dialog_file_path(dialog_file: str) -> Path:
    parsed_dialog_file_path = (
        get_resource_path() / "parsed" / "dialogs" / f"{dialog_file}.lsx"
    )

    return parsed_dialog_file_path


def construct_mocap_path(character_guid: str, handle: str) -> Path:
    return Path(
        get_mocaps_path() / "MC_v"
        f"{character_guid.replace('-', '')}"
        "_"
        f"{handle}"
        ".GR2"
    )


def construct_animation_path(
    visuals_info: dict,
) -> Path:

    filename = f"{visuals_info['rig']}_SCENE_{visuals_info['scene']}_{visuals_info['action']}.GR2"

    return Path(
        get_cinematic_anims_path()
        / visuals_info["act"]
        / visuals_info["area"]
        / visuals_info["scene"]
        / visuals_info["rig"]
        / filename
    )


def construtct_animation_metadata_lsf_path(
    dialog_node_info: dict,
    animation_guid: str,
) -> Path:
    animation_metadata_lsf_path = Path(
        get_animation_metadata_path()
        / dialog_node_info["race_long"]
        / f"[PAK]_{dialog_node_info['body_type_long']}_Cine"
        / f"{animation_guid}.lsf"
    )

    return animation_metadata_lsf_path


# https://www.howtogeek.com/266621/how-to-make-windows-10-accept-file-paths-over-260-characters/


def copy_animation(dialog_node_info):
    os.makedirs(os.path.dirname(dialog_node_info["animation_path"]), exist_ok=True)
    shutil.copyfile(
        dialog_node_info["mocap_path"],
        dialog_node_info["animation_path"],
    )
