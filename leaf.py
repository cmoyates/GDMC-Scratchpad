from glm import ivec3, vec3, round
import random
from utils import STARTING_HEIGHT, AREA
from gdpc import Editor, Block, geometry
from gdpc.vector_tools import (
    addY,
)


class Leaf:
    def __init__(self) -> None:
        self.pos = vec3(
            random.randint(0, AREA.x - 1),
            random.randint(STARTING_HEIGHT, AREA.y - 1),
            random.randint(0, AREA.z - 1),
        )
        self.reached = False

    def show(self, editor: Editor):
        int_pos = ivec3(round(self.pos))
        geometry.placeLine(editor, int_pos, int_pos, Block("red_concrete"), 3)
