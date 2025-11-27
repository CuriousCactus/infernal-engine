def get_character_guid(tree, speaker_index):
    nodes = tree.find("region").find("node").find("children").findall("node")

    speakers_list = (
        next(node for node in nodes if node.get("id") == "speakerlist")
        .find("children")
        .findall("node")
    )

    character_guid = next(
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
    )

    return character_guid
