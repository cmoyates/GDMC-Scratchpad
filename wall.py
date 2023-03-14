from gdpc import __url__, Editor, Block, geometry, Box
from glm import ivec3, vec3
import random
import math


def generate_wall(editor: Editor, base_pos: ivec3, width: int, height: int):
    print("wall")
    for x in range(width):
        for y in range(height):

            # block_names = [
            #     "calcite",
            #     "diorite",
            #     "cobblestone",
            #     "cobbled_deepslate",
            #     "deepslate",
            # ]
            # block_names.reverse()
            # height_percent = float(y) / height
            # block_index = math.floor(height_percent * 5)
            block_names = [
                "dead_bubble_coral_block",
                "dead_tube_coral_block",
                "dead_brain_coral_block",
                "dead_horn_coral_block",
                "dead_fire_coral_block",
            ]

            block_index = math.floor(random.random() * len(block_names))

            editor.placeBlock(
                ivec3(base_pos.x + x, base_pos.y + y, base_pos.z),
                Block(block_names[block_index]),
            )
