import glob
import os
from enum import Enum
from logging import warning
from pathlib import Path

from infernal_engine.utils.parsing import get_tree_from_lsf
from infernal_engine.utils.settings import (
    get_base_body_path,
    get_character_visuals_paths,
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
    character_visuals_paths = get_character_visuals_paths()
    for character_visuals_path in character_visuals_paths:
        mod = os.path.normpath(character_visuals_path).split(os.sep)[-4]
        character_visuals_tree = get_tree_from_lsf(
            character_visuals_path,
            get_resource_path() / "parsed" / f"character_visuals_{mod}.lsx",
        )

        resources = (
            character_visuals_tree.find("region")  # type: ignore
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

        if character_base_visual_guid:
            return character_base_visual_guid

    return None


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
    character: str | None,
) -> str | None:
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

    preview_visual_name = (
        f"{body_type}_NKD_Body{'_' + character if character else ''}"
    )

    preview_visual_guid = next(
        (
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
                    if preview_visual_name in x.get("value")
                ]
            )
            > 0
        ),
        None,
    )

    if preview_visual_guid is None:
        warning(f"preview_visual_guid not found for {preview_visual_name}")

    return preview_visual_guid


def get_skeleton_guid(
    body_tree,
    body_type: str,
) -> str | None:
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

    skeleton_name = f"{body_type}_Base"

    skeleton_guid = next(
        (
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
                    if skeleton_name in x.get("value")
                ]
            )
            > 0
        ),
        None,
    )

    if skeleton_guid is None:
        warning(f"skeleton_guid not found for {skeleton_name}")

    return skeleton_guid


def get_character_info(
    character_guid: str,
) -> dict | None:
    character_info: dict[str, str | None] = {}
    character_info["character_guid"] = character_guid

    character_base_visual_guid = get_character_base_visual_guid(character_guid)

    if character_base_visual_guid is None:
        return character_info

    character_info["character_base_visual_guid"] = character_base_visual_guid

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
        return character_info

    base_visual_sections = base_visual.split("_")
    race = base_visual_sections[0]
    body_type = base_visual_sections[1]
    body = "_".join(base_visual_sections[0:2])
    character = (
        base_visual_sections[2].title()
        if len(base_visual_sections) > 2 and base_visual_sections[2] != "Base"
        else None
    )
    rig = body + "_Rig"

    preview_visual_guid = get_preview_visual_guid(body_tree, body, character)
    skeleton_guid = get_skeleton_guid(body_tree, body)

    character_info["base_visual"] = base_visual
    character_info["race"] = race
    character_info["race_long"] = race_long
    character_info["body_type"] = body_type
    character_info["body_type_long"] = body_type_long
    character_info["body"] = body
    character_info["character"] = character
    character_info["rig"] = rig
    character_info["preview_visual_guid"] = preview_visual_guid
    character_info["skeleton_guid"] = skeleton_guid

    return character_info
