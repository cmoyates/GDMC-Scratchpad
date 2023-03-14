from glm import ivec3, vec3, round, clamp
from gdpc import Editor, Block, geometry
from gdpc.vector_tools import addY, distance
from utils import BRANCH_LENGTH, AREA


class Branch:
    def __init__(self, parent, pos: vec3, dir: vec3, last: bool = False) -> None:
        self.pos = pos
        self.parent = parent
        self.dir = dir
        self.origDir = vec3(self.dir.x, self.dir.y, self.dir.z)
        self.count = 0
        self.len = BRANCH_LENGTH
        self.last = last

    def reset(self):
        self.dir = vec3(self.origDir.x, self.origDir.y, self.origDir.z)
        self.count = 0

    def next(self):
        next_dir = self.dir * self.len
        next_pos = self.pos + next_dir
        clamp_pos = clamp(next_pos, vec3(0, 0, 0), AREA)
        print()
        print(next_pos)
        print(clamp_pos)
        print(distance(clamp_pos, next_pos))
        print()
        next_branch = Branch(
            self, clamp_pos, next_dir, last=(distance(clamp_pos, next_pos) > 1)
        )
        return next_branch

    def show(self, editor: Editor):
        print("Place Branch")
        if self.parent != None:
            geometry.placeLine(
                editor,
                self.pos,
                self.parent.pos,
                Block("brown_concrete"),
                3,
            )

        # int_pos = ivec3(round(self.pos))
        # geometry.placeCylinder(editor, int_pos, 5, 1, Block("green_concrete"))
