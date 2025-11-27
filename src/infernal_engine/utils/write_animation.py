import os
import uuid
import xml.etree.ElementTree as ET
from pathlib import Path

from infernal_engine.utils.parsing import convert_file, get_tree_from_lsx
from infernal_engine.utils.paths import construtct_animation_metadata_lsf_path
from infernal_engine.utils.settings import (
    ANIMATION_METADATA_TEMPLATE_PATH,
    BASE_OUTPUT_PATH,
    DATA_PATH,
)


def construct_animation_metadata_tree(
    dialog_node_info,
    animation_guid,
) -> ET.ElementTree:
    animation_metadata_template_tree = get_tree_from_lsx(
        ANIMATION_METADATA_TEMPLATE_PATH
    )

    attributes = (
        animation_metadata_template_tree.find("region")
        .find("node")
        .find("children")
        .find("node")
        .findall("attribute")
    )

    animation_relative_path = (
        dialog_node_info["animation_path"].relative_to(DATA_PATH).as_posix()
    )

    for attribute in attributes:
        if attribute.get("id") == "ID":
            attribute.set("value", animation_guid)
        elif attribute.get("id") == "Name":
            attribute.set("value", Path(animation_relative_path).stem)
        elif attribute.get("id") == "SourceFile":
            attribute.set("value", str(animation_relative_path))
        elif attribute.get("id") == "Template":
            attribute.set(
                "value",
                str(animation_relative_path).replace(".GR2", ".Anim.0"),
            )
        elif attribute.get("id") == "PreviewVisualResource":
            attribute.set("value", dialog_node_info["preview_visual_guid"])
        elif attribute.get("id") == "SkeletonResource":
            attribute.set("value", dialog_node_info["skeleton_guid"])

    return animation_metadata_template_tree


def write_animation(dialog_node_info):
    animation_guid = str(uuid.uuid4())

    animation_metadata_template_tree = construct_animation_metadata_tree(
        dialog_node_info,
        animation_guid,
    )

    # Save the modified tree to a temporary lsx file
    os.makedirs(BASE_OUTPUT_PATH / "temp", exist_ok=True)

    animation_metadata_lsx_path = (
        BASE_OUTPUT_PATH / "temp" / Path(animation_guid + ".lsx")
    )

    animation_metadata_template_tree.write(str(animation_metadata_lsx_path))

    # Convert the lsx file to lsf and save it to the appropriate path
    animation_metadata_lsf_path = construtct_animation_metadata_lsf_path(
        dialog_node_info,
        animation_guid,
    )

    os.makedirs(animation_metadata_lsf_path.parent, exist_ok=True)
    convert_file(animation_metadata_lsx_path, animation_metadata_lsf_path)
