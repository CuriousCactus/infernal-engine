from infernal_engine.utils.characters import get_character_info
from infernal_engine.utils.dialog import get_speaker_index
from infernal_engine.utils.parsing import get_tree_from_lsf
from infernal_engine.utils.paths import (
    construct_parsed_dialog_file_path,
    find_file_path,
)
from infernal_engine.utils.scene import get_scene_info
from infernal_engine.utils.settings import get_dialog_binaries_paths
from infernal_engine.utils.speakers import get_character_guid


def get_animation_info(
    handle: str,
    dialog_file: str,
    speakers: dict,
) -> dict:
    dialog_file_path = find_file_path(dialog_file, get_dialog_binaries_paths())
    parsed_dialog_file_path = construct_parsed_dialog_file_path(dialog_file)
    dialog_tree = get_tree_from_lsf(dialog_file_path, parsed_dialog_file_path)

    speaker_index = get_speaker_index(dialog_tree, handle)

    if speaker_index not in speakers:
        character_guid = get_character_guid(
            dialog_tree,
            speaker_index,
        )

        if character_guid is None:
            return {}

        character_info = get_character_info(character_guid)

        if character_info is None:
            return {}

        speakers[speaker_index] = character_info
    else:
        character_guid = speakers[speaker_index]["character_guid"]

    scene_info = get_scene_info(
        handle,
        dialog_file_path,
        speakers[speaker_index],
    )

    animation_info = {
        "handle": handle,
        "speaker_index": speaker_index,
        **speakers[speaker_index],
        **scene_info,
    }

    return animation_info
