from fastapi import FastAPI
import uvicorn
from gdpc import __url__, Editor, Block, geometry, Box, nbt_tools
import requests
from glm import ivec3, vec3
import math
import time
from threading import Thread
from spider import generate_spider
from heightmap import get_heightmap


app = FastAPI()
editor = Editor()


@app.get("/")
async def root():
    test_thread = Thread(target=test, args=(editor,))
    test_thread.start()
    return {"test": "test"}


@app.get("/heightmap")
async def heightmap():
    test_thread = Thread(target=get_heightmap, args=(editor,))
    test_thread.start()
    return {"test": "test"}


def test(editor: Editor):
    response = requests.get("http://localhost:9000/players")
    player_list = response.json()
    player = player_list[0]
    print(player["cameraRotation"])

    distance = 20

    # convert angle to radians
    angle_radians = math.radians(player["cameraRotation"]["y"]) + (math.pi / 2)

    # calculate x and y coordinates
    x = distance * math.cos(angle_radians)
    z = distance * math.sin(angle_radians)

    pos = ivec3(
        round(player["x"] + x),
        round(player["y"]),
        round(player["z"] + z),
    )

    generate_spider(editor, pos)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000, reload=True)
