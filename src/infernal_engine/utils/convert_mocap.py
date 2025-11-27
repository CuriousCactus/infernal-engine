from infernal_engine.utils.info import get_animation_info
from infernal_engine.utils.paths import copy_animation
from infernal_engine.utils.write_animation import write_animation


def convert_mocap(handle: str, dialog_file: str):
    animation_info = get_animation_info(
        handle,
        dialog_file,
    )

    copy_animation(animation_info)
    write_animation(animation_info)
