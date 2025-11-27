import os
from pathlib import Path
import glob
from enum import Enum

from infernal_engine.utils.parsing import get_tree_from_lsf
from infernal_engine.utils.settings import (
    BASE_BODY_PATH,
    CHARACTER_VISUALS_PATH,
    BASE_OUTPUT_PATH,
)


class Race(Enum):
    DGB = "Dragonborn"
    DWR = "Dwarfs"
    ELF = "Elves"
    GNO = "Gnomes"
    GTY = "Githyanki"
    HEL = "HalfElves"
    HFL = "Halflings"
    HRC = "HalfOrcs"
    HUM = "Humans"
    MFLP = "Mindflayer_Player"
    TIF = "Tieflings"


class BodyType(Enum):
    F = "Female"
    FS = "FemaleStrong"
    M = "Male"
    MS = "MaleStrong"


def get_character_base_visual_guid(character_guid: str) -> str:
    character_visuals_tree = get_tree_from_lsf(
        CHARACTER_VISUALS_PATH, BASE_OUTPUT_PATH / "parsed" / "character_visuals.lsx"
    )

    character_base_visual_guid = next(
        next(
            attribute.get("value")
            for attribute in node.findall("attribute")
            if attribute.get("id") == "BaseVisual"
        )
        for node in character_visuals_tree.findall(".//node")
        if len(
            [x for x in (node.findall("attribute")) if character_guid in x.get("value")]
        )
        > 0
    )

    return character_base_visual_guid


def get_base_visual(
    body_tree,
    character_base_visual_guid,
):
    visual_bank = next(
        (
            region
            for region in body_tree.findall("region")
            if region.get("id") == "VisualBank"
        ),
        None,
    )
    if visual_bank is None:
        return None

    visuals = visual_bank.find("node").find("children").findall("node")

    base_visual = next(
        (
            next(
                attribute.get("value")
                for attribute in node.findall("attribute")
                if attribute.get("id") == "Name"
            )
            for node in visuals
            if len(
                [
                    x
                    for x in (node.findall("attribute"))
                    if character_base_visual_guid == x.get("value")
                ]
            )
            > 0
        ),
        None,
    )

    return base_visual


def get_preview_visual_guid(
    body_tree,
    body_type: str,
) -> str:
    visuals = (
        next(
            region
            for region in body_tree.findall("region")
            if region.get("id") == "VisualBank"
        )
        .find("node")
        .find("children")
        .findall("node")
    )

    preview_visual_guid = next(
        next(
            attribute.get("value")
            for attribute in node.findall("attribute")
            if attribute.get("id") == "ID"
        )
        for node in visuals
        if len(
            [
                x
                for x in (node.findall("attribute"))
                if f"{body_type}_NKD_Body_A" == x.get("value")
            ]
        )
        > 0
    )

    return preview_visual_guid


def get_skeleton_guid(
    body_tree,
    body_type: str,
) -> str:
    visuals = (
        next(
            region
            for region in body_tree.findall("region")
            if region.get("id") == "SkeletonBank"
        )
        .find("node")
        .find("children")
        .findall("node")
    )

    skeleton_guid = next(
        next(
            attribute.get("value")
            for attribute in node.findall("attribute")
            if attribute.get("id") == "ID"
        )
        for node in visuals
        if len(
            [
                x
                for x in (node.findall("attribute"))
                if f"{body_type}_Base" == x.get("value")
            ]
        )
        > 0
    )

    return skeleton_guid


def get_visuals_info(
    dialog_file_path: Path,
    character_guid: str,
    dialog_line_squashed: str,
) -> dict:
    character_base_visual_guid = get_character_base_visual_guid(character_guid)
    body_paths = glob.glob(
        BASE_BODY_PATH.as_posix() + "/*/[[]PAK[]]*Body/_merged.lsf", recursive=True
    )

    for body_path in body_paths:
        body_tree = get_tree_from_lsf(
            Path(body_path), BASE_OUTPUT_PATH / "parsed" / "body.lsx"
        )

        base_visual = get_base_visual(body_tree, character_base_visual_guid)

        if base_visual:
            break

    race = base_visual.split("_")[0]
    race_long = Race[race].value
    body_type = base_visual.split("_")[1]
    body_type_long = BodyType[body_type].value
    body = base_visual.replace("_Base", "")
    rig = base_visual.replace("_Base", "_Rig")
    action = dialog_line_squashed

    preview_visual_guid = get_preview_visual_guid(body_tree, body)
    skeleton_guid = get_skeleton_guid(body_tree, body)

    sections = str(dialog_file_path).split(os.sep)

    act = sections[-3].replace("Act", "Act0")
    scene = sections[-1].split(".")[0]
    area = scene.split("_")[0]

    return {
        "character_base_visual_guid": character_base_visual_guid,
        "act": act,
        "area": area,
        "scene": scene,
        "race": race,
        "race_long": race_long,
        "body_type": body_type,
        "body_type_long": body_type_long,
        "body": body,
        "rig": rig,
        "base_visual": base_visual,
        "action": action,
        "preview_visual_guid": preview_visual_guid,
        "skeleton_guid": skeleton_guid,
    }
