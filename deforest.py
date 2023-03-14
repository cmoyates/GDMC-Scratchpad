from gdpc import __url__, Editor, Block, geometry, Box, nbt_tools, lookup, Rect
import numpy as np
import cv2
import requests
from glm import ivec3, vec3, ivec2
import time
from nbt_parser import parse_nbt

TREE_STUFF = [
    "minecraft:oak_log",
    "minecraft:spruce_log",
    "minecraft:birch_log",
    "minecraft:jungle_log",
    "minecraft:dark_oak_log",
    "minecraft:acacia_log",
    "minecraft:mangrove_log",
    "minecraft:cactus",
    "minecraft:oak_leaves",
    "minecraft:spruce_leaves",
    "minecraft:birch_leaves",
    "minecraft:jungle_leaves",
    "minecraft:acacia_leaves",
    "minecraft:dark_oak_leaves",
    "minecraft:mangrove_leaves",
    "minecraft:azalea_leaves",
    "minecraft:flowering_azalea_leaves",
]


def deforest(editor: Editor):
    # see if a different build area was defined ingame
    buildArea = editor.getBuildArea()
    buildRect = buildArea.toRect()
    x1, z1 = buildRect.begin
    x2, z2 = buildRect.end

    # load the world data and extract the heightmap(s)
    worldSlice = editor.loadWorldSlice(buildRect)

    heightmap = np.array(worldSlice.heightmaps["MOTION_BLOCKING"], dtype=int)

    air_block = Block("air")

    editor.buffering = True
    editor.bufferLimit = 16384

    for x, z in buildRect.inner:
        # check up to 5 blocks below the heightmap
        for dy in range(30):
            # calculate absolute coordinates
            y = int(heightmap[(x - x1, z - z1)]) - dy
            # Get block
            block = worldSlice.getBlockGlobal((x, y, z))
            if block.id in TREE_STUFF:
                editor.placeBlockGlobal((x, y, z), air_block)
                block_below = worldSlice.getBlockGlobal((x, y - 1, z))
                if block_below.id in [
                    "minecraft:dirt",
                    "minecraft:sand",
                    "minecraft:grass_block",
                    "minecraft:stone",
                ]:
                    break

    editor.flushBuffer()
    editor.buffering = False


if __name__ == "__main__":
    deforest(Editor())
