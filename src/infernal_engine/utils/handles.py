from infernal_engine.utils.dialog import get_handle, get_nodes_list
from infernal_engine.utils.parsing import get_tree_from_lsf
from infernal_engine.utils.paths import (
    construct_parsed_dialog_file_path,
    find_file_path,
)
from infernal_engine.utils.settings import get_dialog_binaries_paths


def get_handles(dialog_file: str) -> list[str]:
    dialog_file_path = find_file_path(dialog_file, get_dialog_binaries_paths())
    parsed_dialog_file_path = construct_parsed_dialog_file_path(dialog_file)
    dialog_tree = get_tree_from_lsf(dialog_file_path, parsed_dialog_file_path)
    node_list = get_nodes_list(dialog_tree)

    handles = []
    for node in node_list:
        handle = get_handle(node)
        if handle is not None:
            handles.append(handle)

    return handles
