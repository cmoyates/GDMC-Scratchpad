#!/usr/bin/env python3

"""
Place and retrieve a single block in the world.
"""

import sys
import numpy as np
import random
import math
from glm import ivec2, ivec3
from gdpc import __url__, Editor, Block, geometry
from gdpc.exceptions import InterfaceConnectionError

from node import Node
from attractor import Attractor
from utils import SCREEN_HEIGHT, SCREEN_WIDTH

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

# Create the initial nodes and attractors
nodes = [Node(editor, ivec2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))]
attractors = [
    Attractor(
        editor,
        ivec2(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT)),
        random.randint(1, 5),
    )
    for i in range(20)
]
attractor_positions = [attractor.position for attractor in attractors]


# Update the positions of the nodes
for node in nodes:
    node.update_position(nodes, attractor_positions)

# Draw the nodes and attractors
for attractor in attractors:
    attractor.draw()
for node in nodes:
    node.draw()
