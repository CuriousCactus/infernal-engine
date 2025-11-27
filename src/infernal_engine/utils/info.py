from infernal_engine.utils.settings import DIALOG_BINARIES_PATHS
from infernal_engine.utils.parsing import get_tree_from_lsf
from infernal_engine.utils.paths import (
    construct_animation_path,
    construct_mocap_path,
    construct_parsed_dialog_file_path,
    find_file_path,
)
from infernal_engine.utils.visuals import get_visuals_info
from infernal_engine.utils.dialog import (
    get_dialog_line,
    get_speaker_index,
    get_squashed_dialog_line,
)
from infernal_engine.utils.speakers import get_character_guid


def get_animation_info(
    handle: str,
    dialog_file: str,
) -> dict:
    dialog_file_path = find_file_path(dialog_file, DIALOG_BINARIES_PATHS)
    parsed_dialog_file_path = construct_parsed_dialog_file_path(dialog_file)

    animation_info = {}
    animation_info["handle"] = handle

    dialog_tree = get_tree_from_lsf(dialog_file_path, parsed_dialog_file_path)
    speaker_index = get_speaker_index(dialog_tree, handle)
    character_guid = get_character_guid(dialog_tree, speaker_index)
    dialog_line = get_dialog_line(handle)
    dialog_line_squashed = get_squashed_dialog_line(dialog_line)
    mocap_path = construct_mocap_path(character_guid, handle)

    animation_info["speaker_index"] = speaker_index
    animation_info["character_guid"] = character_guid
    animation_info["dialog_line"] = dialog_line
    animation_info["dialog_line_squashed"] = dialog_line_squashed
    animation_info["mocap_path"] = mocap_path

    visuals_info = get_visuals_info(
        dialog_file_path,
        character_guid,
        dialog_line_squashed,
    )

    animation_info["animation_path"] = construct_animation_path(visuals_info)

    animation_info = {**animation_info, **visuals_info}

    print(animation_info)

    return animation_info
