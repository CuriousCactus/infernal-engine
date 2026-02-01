from pathlib import Path


def get_character_guid(mocap_path: Path) -> str:
    character_guid_no_dashes = mocap_path.name.split("_")[1][1:]

    character_guid = (
        character_guid_no_dashes[:8]
        + "-"
        + character_guid_no_dashes[8:12]
        + "-"
        + character_guid_no_dashes[12:16]
        + "-"
        + character_guid_no_dashes[16:20]
        + "-"
        + character_guid_no_dashes[20:]
    )

    return character_guid
