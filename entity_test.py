from glm import ivec3, vec3
from gdpc import __url__, Editor, Block
import requests
import math
import nbtlib


def place_at_armor_stands(editor: Editor):
    url_params = {
        "x": -256,
        "y": -128,
        "z": -256,
        "dx": 512,
        "dy": 512,
        "dz": 512,
        "includeData": True,
    }

    test = requests.get("http://localhost:9000/entities", params=url_params)
    entities = test.json()
    armor_stand_positions = []
    for entity in entities:
        data_str = entity["data"]
        parsed_data = nbtlib.parse_nbt(data_str)
        parsed_dict = dict(parsed_data)
        if parsed_dict["id"] == "minecraft:armor_stand":
            pos_list = parsed_dict["Pos"]
            armor_stand_positions.append(
                ivec3(
                    math.floor(pos_list[0]),
                    math.floor(pos_list[1]),
                    math.floor(pos_list[2]),
                )
            )
    print(armor_stand_positions)
    for pos in armor_stand_positions:
        editor.placeBlock(pos, Block("stone"))
