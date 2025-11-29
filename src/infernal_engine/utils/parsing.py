import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path

from infernal_engine.utils.settings import DIVINE_PATH


def convert_file(source_path: Path, target_path: Path):
    if source_path.suffix == ".loca":
        command = "convert-loca"
    else:
        command = "convert-resource"

    subprocess.run(
        [
            DIVINE_PATH,
            f"-a",
            command,
            "-s",
            str(source_path),
            "-d",
            str(target_path),
            "-g",
            "bg3",
        ]
    )


def get_tree_from_lsx(path: Path) -> ET.ElementTree:
    # Parse the lsx file
    parser = ET.XMLParser(target=ET.TreeBuilder(insert_comments=True))
    tree = ET.parse(path, parser)

    return tree


def get_tree_from_lsf(source_path: Path, target_path: Path) -> ET.ElementTree:
    # Convert the lsf to lsx
    convert_file(source_path, target_path)

    # Parse the lsx file
    tree = get_tree_from_lsx(target_path)

    return tree
