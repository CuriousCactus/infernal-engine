import os

from infernal_engine.utils.parsing import convert_file, get_tree_from_lsx
from infernal_engine.utils.settings import (
    get_translations_output_path,
    get_translations_path,
)


def get_nodes_list(dialog_tree):
    nodes = dialog_tree.find("region").find("node").find("children").findall("node")

    # Get the nodes
    node_list = (
        next(node for node in nodes if node.get("id") == "nodes")
        .find("children")
        .findall("node")
    )

    return node_list


def get_dialog_line(handle):
    convert_file(get_translations_path(), get_translations_output_path())
    translations_tree = get_tree_from_lsx(get_translations_output_path())

    dialog_lines = translations_tree.findall("content")

    dialog_line = next(
        dialog_line.text
        for dialog_line in dialog_lines
        if dialog_line.get("contentuid") == handle
    )

    return dialog_line


def get_handle(node):
    children = node.find("children")
    if children is not None:
        property_nodes = children.findall("node")
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

                        handle = next(
                            (
                                attribute.get("handle")
                                for attribute in attributes
                                if attribute.get("id") == "TagText"
                            ),
                            None,
                        )

                        return handle


def node_matches_handle(node, handle: str) -> bool:
    current_handle = get_handle(node)

    if current_handle == handle:
        return True
    else:
        return False


def get_speaker_index(dialog_tree, handle: str) -> str:
    node_list = get_nodes_list(dialog_tree)

    for node in node_list:
        if node_matches_handle(node, handle):
            speaker_index = next(
                attribute.get("value")
                for attribute in node.findall("attribute")
                if attribute.get("id") == "speaker"
            )

            return speaker_index


def get_word_without_characters(word: str) -> str:
    word = word.replace("<i>", "")
    word = word.replace("</i>", "")
    return "".join(character for character in word if character.isalnum())


def get_squashed_dialog_line(dialog_line: str) -> str:
    dialog_line_sections = dialog_line.split(" ")

    first_five_sections = [
        get_word_without_characters(dialog_line_section)
        for dialog_line_section in dialog_line_sections[:5]
        if get_word_without_characters(dialog_line_section)
    ]

    dialog_line_squashed = "_".join(first_five_sections)

    return dialog_line_squashed
