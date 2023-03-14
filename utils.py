from glm import vec2, dot, cross, vec3
from gdpc.vector_tools import (
    length,
)


# Define constants
AREA = vec3(50, 200, 50)
SCREEN_HEIGHT = 100
MAX_DIST = 50
MIN_DIST = 5
LEAF_COUNT = 100
BRANCH_LENGTH = 3
STARTING_HEIGHT = 20


def dist_to_line(pos: vec2, line_start: vec2, line_end: vec2):
    ab = line_end - line_start
    ac = pos - line_start
    if dot(ac, ab) <= 0.0:
        return length(ac)
    bv = pos - line_end
    if dot(bv, ab) >= 0.0:
        return length(bv)
    return length(cross(ab, ac)) / length(ab)
