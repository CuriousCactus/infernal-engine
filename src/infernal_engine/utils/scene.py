import os
from pathlib import Path

from infernal_engine.utils.dialog import get_dialog_line, get_squashed_dialog_line
from infernal_engine.utils.paths import construct_animation_path, construct_mocap_path


def get_act(dialog_file_path_sections: list[str]) -> str:
    for i in [-3, -4]:
        if "Act" in dialog_file_path_sections[i]:
            act = dialog_file_path_sections[i].replace("Act", "Act0")

    if act is None:
        raise ValueError("Act not found in dialog file path sections.")

    return act


def get_scene_info(
    handle: str,
    character_guid: str,
    dialog_file_path: Path,
    character: dict,
) -> dict:
    if character.get("base_visual") == None:
        return {}

    dialog_file_path_sections = str(dialog_file_path).split(os.sep)

    act = get_act(dialog_file_path_sections)
    scene = dialog_file_path_sections[-1].split(".")[0]
    area = scene.split("_")[0]

    dialog_line = get_dialog_line(handle)
    dialog_line_squashed = get_squashed_dialog_line(dialog_line)
    mocap_path = construct_mocap_path(character_guid, handle)

    scene_info: dict[str, str | Path] = {
        "act": act,
        "area": area,
        "scene": scene,
        "action": dialog_line_squashed,
        "dialog_line": dialog_line,
        "dialog_line_squashed": dialog_line_squashed,
        "mocap_path": mocap_path,
    }

    scene_info["animation_path"] = construct_animation_path(scene_info, character)

    return scene_info
