import os
from pathlib import Path

from infernal_engine.utils.handles import get_handles
from infernal_engine.utils.info import get_animation_info
from infernal_engine.utils.paths import copy_animation
from infernal_engine.utils.write_animation import write_animation


def convert_mocap(handle: str | None, dialog_file: str):
    if not handle:
        handles = get_handles(dialog_file)
    else:
        handles = [handle]

    speakers: dict[str, dict[str, str | Path]] = {}
    for handle in handles:
        animation_info = get_animation_info(
            handle,
            dialog_file,
            speakers,
        )

        if animation_info.get("animation_path"):
            copy_animation(animation_info)
            write_animation(animation_info)


if __name__ == "__main__":
    os.environ["MOD_NAME"] = (
        "ReturnToTheHouseOfHope_295379f9-b5ee-119f-54c1-9f6bd887046b"
    )
    os.environ["DATA_PATH"] = (
        "C:/Program Files (x86)/Steam/steamapps/common/Baldurs Gate 3/Data"
    )
    os.environ["UNPACKED_DATA_PATH"] = (
        "C:/Users/Shadow/bg3-modders-multitool/UnpackedData"
    )
    os.environ["DIVINE_PATH"] = (
        "C:/Users/Shadow/ExportTool-v1.20-b3/Packed/Tools/Divine.exe"
    )

    convert_mocap(None, "WYR_SharessCaress_Taproom_Threeway_NymphDrunkFist")
    # convert_mocap(None, "LOW_HouseOfHope_Hope")
