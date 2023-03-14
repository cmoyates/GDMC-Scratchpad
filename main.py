#!/usr/bin/env python3

"""
Place and retrieve a single block in the world.
"""

import sys
import numpy as np
import random
import math
from glm import ivec3, vec3
from gdpc import __url__, Editor, Block, geometry, Box, nbt_tools
from gdpc.exceptions import InterfaceConnectionError
from tree import Tree
import argparse
from utils import AREA
from wall import generate_wall
from spider import generate_leg
import requests
import json
import nbtlib
from deforest import deforest
import time

# Create an editor object.
# The Editor class provides a high-level interface to interact with the Minecraft world.
editor = Editor()


# Check if the editor can connect to the GDMC HTTP interface.
try:
    editor.checkConnection()
except InterfaceConnectionError:
    print(
        f"Error: Could not connect to the GDMC HTTP interface at {editor.host}!\n"
        'To use GDPC, you need to use a "backend" that provides the GDMC HTTP interface.\n'
        "For example, by running Minecraft with the GDMC HTTP mod installed.\n"
        f"See {__url__}/README.md for more information."
    )
    sys.exit(1)


# # Place a block of red concrete at (0,80,0)!
# editor.placeBlock((0, 80, 0), Block("red_concrete"))


# # Retrieve the block at (0,80,0) and print it.
# block = editor.getBlock((0, 80, 0))
# print(f"Block at (0,80,0): {block}")

floor_height = 40


def main():
    start_time = time.time()
    # deforest(Editor())
    requests.get("http://localhost:9000/deforest")
    print(time.time() - start_time)


if __name__ == "__main__":
    main()
