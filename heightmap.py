from gdpc import __url__, Editor, Block, geometry, Box, nbt_tools, lookup, Rect
import numpy as np
import cv2
import requests
from glm import ivec3, vec3, ivec2


def get_heightmap(editor: Editor):

    response = requests.get("http://localhost:9000/players")
    player_list = response.json()
    print("Players:", player_list)
    player = player_list[0]
    player_pos = ivec3(player["x"], player["y"], player["z"])
    print("Player Pos:", player_pos)

    build_area_size = ivec3(512, 320, 512)
    editor.setBuildArea(
        Box(
            ivec3(
                player_pos.x - (build_area_size.x / 2),
                -64,
                player_pos.z - (build_area_size.z / 2),
            ),
            build_area_size,
        )
    )

    # see if a different build area was defined ingame
    buildArea = editor.getBuildArea()
    buildRect = buildArea.toRect()
    x1, z1 = buildRect.begin
    x2, z2 = buildRect.end

    # load the world data and extract the heightmap(s)
    worldSlice = editor.loadWorldSlice(buildRect)

    heightmap = np.array(worldSlice.heightmaps["MOTION_BLOCKING_NO_LEAVES"], dtype=int)
    print(heightmap)

    # calculate the gradient (steepness)
    decrementor = np.vectorize(lambda a: a - 1)
    cvheightmap = np.clip(decrementor(heightmap), 0, 255).astype(np.uint8)
    gradientX = cv2.Scharr(cvheightmap, cv2.CV_16S, 1, 0)
    gradientY = cv2.Scharr(cvheightmap, cv2.CV_16S, 0, 1)

    unknownBlocks = set()

    for x, z in buildRect.inner:
        # check up to 5 blocks below the heightmap
        for dy in range(5):
            # calculate absolute coordinates
            y = int(heightmap[(x - x1, z - z1)]) - dy

            block = worldSlice.getBlockGlobal((x, y, z))
            if block.id in lookup.MAP_TRANSPARENT:
                # transparent blocks are ignored
                continue

    cv2.imwrite("sdfsdf.jpg", cvheightmap)


if __name__ == "__main__":
    get_heightmap(Editor())
