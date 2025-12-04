import os
import uuid
import xml.etree.ElementTree as ET
from pathlib import Path

from infernal_engine.utils.hashing import string_to_uuid4
from infernal_engine.utils.parsing import convert_file, get_tree_from_lsx
from infernal_engine.utils.paths import construtct_animation_metadata_lsf_path
from infernal_engine.utils.settings import (
    get_animation_metadata_template_path,
    get_data_path,
    get_resource_path,
)


def construct_animation_metadata_tree(
    dialog_node_info,
    animation_guid,
) -> ET.ElementTree:
    animation_metadata_template_tree = get_tree_from_lsx(
        get_animation_metadata_template_path()
    )

    attributes = (
        animation_metadata_template_tree.find("region")
        .find("node")
        .find("children")
        .find("node")
        .findall("attribute")
    )

    animation_relative_path = (
        dialog_node_info["animation_path"].relative_to(get_data_path()).as_posix()
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


def write_animation(animation_info):
    animation_guid = string_to_uuid4(animation_info["handle"])

    animation_metadata_template_tree = construct_animation_metadata_tree(
        animation_info,
        animation_guid,
    )

    # Save the modified tree to a temporary lsx file
    os.makedirs(get_resource_path() / "temp", exist_ok=True)

    animation_metadata_lsx_path = (
        get_resource_path() / "temp" / Path(animation_guid + ".lsx")
    )

    animation_metadata_template_tree.write(str(animation_metadata_lsx_path))

    # Convert the lsx file to lsf and save it to the appropriate path
    animation_metadata_lsf_path = construtct_animation_metadata_lsf_path(
        animation_info,
        animation_guid,
    )

    convert_file(animation_metadata_lsx_path, animation_metadata_lsf_path)
