import os
from pathlib import Path

from infernal_engine.utils.handles import get_handles
from infernal_engine.utils.info import get_animation_info
from infernal_engine.utils.paths import copy_animation
from infernal_engine.utils.write_animation import write_animation


def convert_mocap(
    handle: str | None,
    dialog_file: str,
    prog_var=None,
    root=None,
):
    # Get all handles for all lines in the dialog file if no
    # specific one is passed
    if not handle:
        handles = get_handles(dialog_file)
    else:
        handles = [handle]

    # Store speaker info to avoid redundant lookups
    speakers: dict[str, dict[str, str | Path]] = {}
    for index, handle in enumerate(handles):
        animation_info = get_animation_info(
            handle,
            dialog_file,
            speakers,
        )

        if animation_info.get("animation_path"):
            copy_animation(animation_info)
            write_animation(animation_info)

        percent_done = (index + 1) * 100 / len(handles)

        if prog_var:
            prog_var.set(percent_done)
            root.update()


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
    convert_mocap(None, "CAMP_Night3_CRD_Astarion")
    convert_mocap(None, "LOW_HouseOfHope_Hope")
    convert_mocap(
        "hfd3d4e05gf322g4231ga27dga265b4fdc449",
        "WYR_GortashConfrontation_SoulConsumption",
    )
    convert_mocap("h00b3ac7dge537g488bg90b1g374567417c8b", "SHA_Raphael")
