def get_character_guid(tree, speaker_index) -> str | None:
    nodes = tree.find("region").find("node").find("children").findall("node")

    speakers_list = (
        next(node for node in nodes if node.get("id") == "speakerlist")
        .find("children")
        .findall("node")
    )

    character_guid = next(
        (
            next(
                attribute.get("value")
                for attribute in speaker.findall("attribute")
                if attribute.get("id") == "list"
            )
            for speaker in speakers_list
            if next(
                attribute.get("value")
                for attribute in speaker.findall("attribute")
                if attribute.get("id") == "index"
            )
            == speaker_index
        ),
        None,
    )

    return character_guid
