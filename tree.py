from leaf import Leaf
from branch import Branch
from glm import normalize, vec3
from utils import MAX_DIST, MIN_DIST, LEAF_COUNT, AREA
from gdpc.vector_tools import (
    distance,
    length,
)
from gdpc import Editor


class Tree:
    def __init__(self, floor_height: int) -> None:
        self.leaves: list[Leaf] = []
        self.branches: list[Branch] = []

        for i in range(LEAF_COUNT):
            self.leaves.append(Leaf())
        pos = vec3(AREA.x / 2, floor_height, AREA.z / 2)
        dir = vec3(0, 1, 0)
        root = Branch(None, pos, dir)
        self.branches.append(root)
        current = root
        found = False
        while not found:
            for leaf in self.leaves:
                d = distance(current.pos, leaf.pos)
                if d < MAX_DIST:
                    found = True
            if not found:
                branch = current.next()
                current = branch
                self.branches.append(current)

    def grow(self):
        for leaf in self.leaves:
            closest_branch = None
            record = MAX_DIST
            for branch in self.branches:
                d = distance(leaf.pos, branch.pos)
                if d < MIN_DIST:
                    leaf.reached = True
                    closest_branch = None
                    break
                elif d < record:
                    closest_branch = branch
                    record = d

            if closest_branch is not None:
                new_dir = leaf.pos - closest_branch.pos
                new_dir = normalize(new_dir)
                closest_branch.dir += new_dir
                closest_branch.count += 1

        for i in range(len(self.leaves) - 1, -1, -1):
            if self.leaves[i].reached:
                self.leaves.pop(i)

        for i in range(len(self.branches) - 1, -1, -1):
            branch = self.branches[i]
            if branch.count > 0 and not branch.last:
                branch.dir /= branch.count + 1
                self.branches.append(branch.next())
                branch.reset()

    def show(self, editor: Editor):
        for leaf in self.leaves:
            leaf.show(editor)

        for branch in self.branches:
            branch.show(editor)
