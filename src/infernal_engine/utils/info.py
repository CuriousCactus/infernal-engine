import xml.etree.ElementTree as ET
from pathlib import Path

from infernal_engine.utils.characters import get_character_info
from infernal_engine.utils.dialog import (
    get_dialog_line,
    get_speaker_index,
    get_squashed_dialog_line,
)
from infernal_engine.utils.parsing import get_tree_from_lsf
from infernal_engine.utils.paths import (
    construct_mocap_path,
    construct_parsed_dialog_file_path,
    find_file_path,
)
from infernal_engine.utils.scene import get_scene_info
from infernal_engine.utils.settings import get_dialog_binaries_paths
from infernal_engine.utils.speakers import get_character_guid


def get_animation_info(
    handle: str,
    dialog_file: str,
    characters: dict,
) -> dict:
    dialog_file_path = find_file_path(dialog_file, get_dialog_binaries_paths())
    parsed_dialog_file_path = construct_parsed_dialog_file_path(dialog_file)
    dialog_tree = get_tree_from_lsf(dialog_file_path, parsed_dialog_file_path)

    animation_info: dict[str, str | Path] = {}
    animation_info["handle"] = handle

    speaker_index = get_speaker_index(dialog_tree, handle)

    character_guid = characters.get(handle, {}).get(
        "character_guid"
    ) or get_character_guid(
        dialog_tree,
        speaker_index,
    )

    if character_guid is None:
        return {}

    dialog_line = get_dialog_line(handle)
    dialog_line_squashed = get_squashed_dialog_line(dialog_line)
    mocap_path = construct_mocap_path(character_guid, handle)

    animation_info["speaker_index"] = speaker_index
    animation_info["character_guid"] = character_guid
    animation_info["dialog_line"] = dialog_line
    animation_info["dialog_line_squashed"] = dialog_line_squashed
    animation_info["mocap_path"] = mocap_path

    if character_guid not in characters:
        character_info = get_character_info(character_guid)

        if not character_info:
            return {}

        characters[character_guid] = character_info

    scene_info = get_scene_info(
        dialog_file_path,
        characters[character_guid],
        dialog_line_squashed,
    )

    animation_info = {**animation_info, **scene_info, **characters[character_guid]}

    return animation_info
