from infernal_engine.utils.paths import find_mocap_file_path


def get_character_guid(handle: str) -> str | None:
    mocap_file_path = find_mocap_file_path(handle)

    if mocap_file_path:
        character_guid_no_dashes = mocap_file_path.name.split("_")[1][1:]

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
    else:
        return None
