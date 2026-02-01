import os
from pathlib import Path

from infernal_engine.utils.dialog import (
    get_dialog_line,
    get_squashed_dialog_line,
)
from infernal_engine.utils.paths import (
    construct_animation_path,
    find_folder_path,
)
from infernal_engine.utils.settings import get_unpacked_cinematic_anims_paths


def get_act(
    dialog_file: str,
    dialog_file_path_sections: list[str],
) -> str:
    unpacked_cinematic_anims_path = find_folder_path(
        dialog_file,
        get_unpacked_cinematic_anims_paths(),
    )

    if unpacked_cinematic_anims_path:
        unpacked_cinematic_anims_path_sections = os.path.normpath(
            unpacked_cinematic_anims_path
        ).split(os.sep)
    else:
        unpacked_cinematic_anims_path_sections = None

    path_sections = (
        unpacked_cinematic_anims_path_sections or dialog_file_path_sections
    )

    act = None
    for i in [-3, -4, -5]:
        if "Act" in path_sections[i]:
            if unpacked_cinematic_anims_path_sections:
                act = path_sections[i]
            else:
                act = dialog_file_path_sections[i].replace("Act", "Act0")

    # Fallback: try to get act from dialog file name
    if act is None:
        for section in dialog_file.split("_"):
            if "Act" in section:
                act = section

    if act is None:
        raise ValueError("Act not found.")

    return act


def get_scene_info(
    handle: str,
    dialog_file: str,
    dialog_file_path: Path,
    speaker: dict,
) -> dict:
    if speaker.get("base_visual") is None:
        return {}

    dialog_file_path_sections = os.path.normpath(dialog_file_path).split(os.sep)

    act = get_act(dialog_file, dialog_file_path_sections)
    scene = dialog_file_path_sections[-1].split(".")[0]
    area = scene.split("_")[0]

    dialog_line = get_dialog_line(handle)
    dialog_line_squashed = get_squashed_dialog_line(dialog_line)

    scene_info: dict[str, str | Path] = {
        "act": act,
        "area": area,
        "scene": scene,
        "action": dialog_line_squashed,
        "dialog_line": dialog_line,
        "dialog_line_squashed": dialog_line_squashed,
        "mocap_path": speaker["mocap_path"],
    }

    scene_info["animation_path"] = construct_animation_path(scene_info, speaker)

    return scene_info
