from gdpc import __url__, Editor, Block, geometry, Box
from glm import ivec3, mat4, radians, rotate, vec3, ivec2, vec2, vec4
import random
import math

from gdpc.vector_tools import (
    distance as get_distance,
    # length,
)


import math
from glm import ivec3, vec3


from typing import Tuple
from glm import ivec2
import math


def inverse_kinematics(
    foot_pos: vec2,
    base_pos: vec2,
    bone_length_1: int,
    bone_length_2: int,
) -> vec2:
    # Calculate the distance between the foot and base positions
    dist = get_distance(foot_pos, base_pos)

    # If the distance is greater than the sum of the two bone lengths, the foot is out of reach
    if dist > bone_length_1 + bone_length_2:
        raise ValueError("Foot position is out of reach")

    # Calculate the angles of the two bones using the law of cosines
    alpha = math.acos(
        (bone_length_1**2 + dist**2 - bone_length_2**2)
        / (2 * bone_length_1 * dist)
    )

    if foot_pos.x < base_pos.x:
        alpha *= -1

    # Calculate the coordinates of the joint
    joint_x = base_pos.x + bone_length_1 * math.cos(
        math.atan2(foot_pos.y - base_pos.y, foot_pos.x - base_pos.x) + alpha
    )
    joint_y = base_pos.y + bone_length_1 * math.sin(
        math.atan2(foot_pos.y - base_pos.y, foot_pos.x - base_pos.x) + alpha
    )

    return vec2(joint_x, joint_y)

    # Flips the joint if the x of the foot is beyond the x of the base
    # if foot_pos.x > base_pos.x:
    #     alpha *= -1


def ivec2_to_tuple(vec: ivec2):
    return (vec.x, vec.y)


def tuple_to_ivec2(tuple: Tuple[int, int]):
    return ivec2(tuple[0], tuple[1])


def rotate_vector(start: vec3, end: vec3, angle_radians: float) -> vec3:
    # Calculate the vector between the start and end points
    vec = end - start

    # Define the rotation matrix around the y-axis
    R = mat4(1)
    R = rotate(R, angle_radians, vec3(0, 1, 0))

    # Rotate the vector around the y-axis centered on the start point
    vec_rotated = vec4(vec.x, vec.y, vec.z, 1) * R
    end_rotated = vec3(start.x, start.y, start.z) + vec3(vec_rotated)

    # Return the new end point
    return end_rotated


def generate_leg(
    editor: Editor,
    foot_pos: ivec3,
    base_pos: ivec3,
    bone1_len: int,
    bone2_len: int,
    block: Block,
):
    print(block.id)

    joint_size = 1
    joint_size_vec = ivec3(joint_size, joint_size, joint_size)

    print("Bone 1", bone1_len)
    print("Bone 2", bone2_len)

    angle = math.atan2(foot_pos.z - base_pos.z, foot_pos.x - base_pos.x)
    print("Angle:", angle)

    y_delta = base_pos.y - foot_pos.y
    xz_delta = get_distance(
        ivec2(foot_pos.x, foot_pos.z), ivec2(base_pos.x, base_pos.z)
    )
    delta_vec = vec2(xz_delta, y_delta)

    print("XZ Delta:", xz_delta)
    print("Y Delta:", y_delta)

    geometry.placeCuboidWireframe(
        editor,
        (base_pos - joint_size_vec),
        (base_pos + joint_size_vec),
        Block("oxidized_copper"),
    )

    editor.placeBlock(foot_pos, block)
    editor.placeBlock(base_pos, block)
    joint_pos_vec2 = inverse_kinematics(
        vec2(0, 0),
        delta_vec,
        bone1_len,
        bone2_len,
    )

    print("Joint Pos vec2:", joint_pos_vec2)

    joint_pos_vec3 = vec3(
        joint_pos_vec2.x + base_pos.x, joint_pos_vec2.y + foot_pos.y, base_pos.z
    )

    print("Joint Pos vec3:", joint_pos_vec3)

    rotated_joint_pos = rotate_vector(
        vec3(base_pos.x, base_pos.y, base_pos.z), joint_pos_vec3, angle
    )

    print("Rotated Joint Pos:", rotated_joint_pos)

    joint_pos = ivec3(
        round(rotated_joint_pos.x),
        round(rotated_joint_pos.y),
        round(rotated_joint_pos.z),
    )

    print("Joint Pos:", joint_pos.to_list())

    editor.placeBlock(
        joint_pos,
        block,
    )

    geometry.placeCuboid(
        editor,
        (joint_pos - joint_size_vec),
        (joint_pos + joint_size_vec),
        Block("oxidized_copper"),
    )

    geometry.placeLine(editor, foot_pos, joint_pos, block, 2)
    geometry.placeLine(editor, base_pos, joint_pos, block, 2)

    geometry.placeCuboid(
        editor,
        (foot_pos - joint_size_vec),
        (foot_pos + joint_size_vec),
        Block("oxidized_copper"),
    )


def generate_spider(editor: Editor, pos: ivec3):
    base_height = 10
    plat_size = ivec3(10, 2, 10)
    plat_base = ivec3(
        pos.x - (plat_size.x / 2), pos.y + base_height, pos.z - (plat_size.z / 2)
    )

    bone_1_len = 10
    bone_2_len = 20
    dist_from_base = 10

    geometry.placeBox(editor, Box(plat_base, plat_size), Block("polished_blackstone"))
    generate_leg(
        editor,
        ivec3(plat_base.x - (dist_from_base), pos.y, plat_base.z - dist_from_base),
        ivec3(plat_base.x, pos.y + base_height, plat_base.z),
        bone_1_len,
        bone_2_len,
        Block("polished_blackstone"),
    )
    generate_leg(
        editor,
        ivec3(
            plat_base.x - (dist_from_base),
            pos.y,
            plat_base.z + plat_size.z - 1 + (dist_from_base),
        ),
        ivec3(plat_base.x, pos.y + base_height, plat_base.z + plat_size.z - 1),
        bone_1_len,
        bone_2_len,
        Block("polished_blackstone"),
    )
    generate_leg(
        editor,
        ivec3(
            plat_base.x + plat_size.x - 1 + (dist_from_base),
            pos.y,
            plat_base.z + plat_size.z - 1 + (dist_from_base),
        ),
        ivec3(
            plat_base.x + plat_size.x - 1,
            pos.y + base_height,
            plat_base.z + plat_size.z - 1,
        ),
        bone_1_len,
        bone_2_len,
        Block("polished_blackstone"),
    )
    generate_leg(
        editor,
        ivec3(
            plat_base.x + plat_size.x - 1 + (dist_from_base),
            pos.y,
            plat_base.z - (dist_from_base),
        ),
        ivec3(plat_base.x + plat_size.x - 1, pos.y + base_height, plat_base.z),
        bone_1_len,
        bone_2_len,
        Block("polished_blackstone"),
    )
