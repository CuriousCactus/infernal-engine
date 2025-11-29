import os

from infernal_engine.utils.parsing import convert_file, get_tree_from_lsx
from infernal_engine.utils.settings import (
    get_translations_output_path,
    get_translations_path,
)


def get_dialog_line(handle):
    print(get_translations_path(), get_translations_output_path())
    convert_file(get_translations_path(), get_translations_output_path())
    os.makedirs(os.path.dirname(get_translations_output_path()), exist_ok=True)
    translations_tree = get_tree_from_lsx(get_translations_output_path())

    dialog_lines = translations_tree.findall("content")

    dialog_line = next(
        dialog_line.text
        for dialog_line in dialog_lines
        if dialog_line.get("contentuid") == handle
    )

    return dialog_line


def node_matches_handle(node, handle: str) -> bool:
    property_nodes = node.find("children").findall("node")
    for property_node in property_nodes:
        property_node_children = property_node.find("children")
        if property_node_children is not None:
            for property in property_node_children.findall("node"):
                if property.get("id") == "TaggedText":
                    attributes = (
                        property.find("children")
                        .find("node")
                        .find("children")
                        .find("node")
                        .findall("attribute")
                    )

                    attribute = next(
                        (
                            attribute
                            for attribute in attributes
                            if attribute.get("id") == "TagText"
                            and attribute.get("handle") == handle
                        ),
                        None,
                    )

                    if attribute is not None:
                        return True
    return False


def get_speaker_index(dialog_tree, handle: str) -> str:
    nodes = dialog_tree.find("region").find("node").find("children").findall("node")

    # Get the nodes
    node_list = (
        next(node for node in nodes if node.get("id") == "nodes")
        .find("children")
        .findall("node")
    )

    for node in node_list:
        if node_matches_handle(node, handle):
            speaker_index = next(
                attribute.get("value")
                for attribute in node.findall("attribute")
                if attribute.get("id") == "speaker"
            )

            return speaker_index


def get_squashed_dialog_line(dialog_line: str) -> str:
    dialog_line_sections = dialog_line.split(" ")

    first_five_sections = [
        "".join(e for e in x if e.isalnum()) for x in dialog_line_sections[:5]
    ]

    dialog_line_squashed = "_".join(first_five_sections)

    return dialog_line_squashed
