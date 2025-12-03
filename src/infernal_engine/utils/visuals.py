import glob
import os
from enum import Enum
from pathlib import Path

from infernal_engine.utils.parsing import get_tree_from_lsf
from infernal_engine.utils.paths import construct_animation_path
from infernal_engine.utils.settings import (
    get_base_body_path,
    get_character_visuals_path,
    get_resource_path,
)


class Race(Enum):
    DGB = "Dragonborn"
    DWR = "Dwarves"
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


def get_character_base_visual_guid(character_guid: str) -> str | None:
    character_visuals_tree = get_tree_from_lsf(
        get_character_visuals_path(),
        get_resource_path() / "parsed" / "character_visuals.lsx",
    )

    resources = (
        character_visuals_tree.find("region")
        .find("node")
        .find("children")
        .findall("node")
    )

    character_base_visual_guid = next(
        (
            next(
                attribute.get("value")
                for attribute in node.findall("attribute")
                if attribute.get("id") == "BaseVisual"
            )
            for node in resources
            if len(
                [
                    x
                    for x in (node.findall("attribute"))
                    if character_guid in x.get("value")
                ]
            )
            > 0
        ),
        None,
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


def get_act(dialog_file_path_sections: list[str]) -> str:
    for i in [-3, -4]:
        if "Act" in dialog_file_path_sections[i]:
            act = dialog_file_path_sections[i].replace("Act", "Act0")

    if act is None:
        raise ValueError("Act not found in dialog file path sections.")

    return act


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
        str(get_base_body_path()) + "/*/[[]PAK[]]*Body/_merged.lsf",
        recursive=True,
    )

    for body_path in body_paths:
        body_path_sections = body_path.split(os.sep)

        race_long = body_path_sections[-3]

        body_type_long = (
            body_path_sections[-2].replace("[PAK]_", "").replace("_Body", "")
        )

        body_tree = get_tree_from_lsf(
            Path(body_path),
            get_resource_path()
            / f"parsed/bodies/{race_long}_{body_type_long}_body.lsx",
        )

        base_visual = get_base_visual(body_tree, character_base_visual_guid)

        if base_visual:
            break

    if base_visual is None:
        return {}

    race = base_visual.split("_")[0]
    body_type = base_visual.split("_")[1]
    body = base_visual.replace("_Base", "")
    rig = base_visual.replace("_Base", "_Rig")
    action = dialog_line_squashed

    preview_visual_guid = get_preview_visual_guid(body_tree, body)
    skeleton_guid = get_skeleton_guid(body_tree, body)

    dialog_file_path_sections = str(dialog_file_path).split(os.sep)

    act = get_act(dialog_file_path_sections)
    scene = dialog_file_path_sections[-1].split(".")[0]
    area = scene.split("_")[0]

    visuals_info = {
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

    visuals_info["animation_path"] = construct_animation_path(visuals_info)

    return visuals_info
