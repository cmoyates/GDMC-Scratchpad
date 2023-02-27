# Define the class for nodes
from utils import ATTRACTOR_RADIUS, MAX_CONNECTIONS, MIN_DISTANCE
from glm import normalize, vec2, ivec2
from gdpc import Editor, geometry, Block
from gdpc.vector_tools import (
    X,
    Y,
    Z,
    XZ,
    addY,
    dropY,
    loop2D,
    loop3D,
    perpendicular,
    toAxisVector2D,
    distance,
    length,
)


class Node:
    def __init__(self, editor: Editor, position: ivec2):
        self.position = position
        self.connections = []
        self.editor = editor

    # Add a connection to another node
    def add_connection(self, node):
        self.connections.append(node)

    # Remove a connection to another node
    def remove_connection(self, node):
        self.connections.remove(node)

    # Check if this node is close enough to an attractor
    def is_near_attractor(self, attractor_pos):
        return distance(self.position, attractor_pos) <= ATTRACTOR_RADIUS

    # Update the position of this node based on its connections and attractors
    def update_position(self, nodes, attractor_positions):
        # Find the average direction of all connections
        avg_dir = vec2(0, 0)
        for connection in self.connections:
            avg_dir += connection.position - self.position
        if len(self.connections) > 0:
            avg_dir /= len(self.connections)

        # Find the direction to each attractor and add it to the average direction
        for attractor_pos in attractor_positions:
            if self.is_near_attractor(attractor_pos):
                direction = attractor_pos - self.position
                if length(direction) > 0:
                    avg_dir += normalize(vec2(direction.x, direction.y)) * (
                        1 - length(direction) / ATTRACTOR_RADIUS
                    )

        # Limit the number of connections
        if len(self.connections) >= MAX_CONNECTIONS:
            return

        # Add a new node if the spacing condition is met
        if (
            length(avg_dir) > 0
            and distance(self.position, nodes[0].position) > MIN_DISTANCE
        ):
            new_pos: vec2 = self.position + normalize(avg_dir) * MIN_DISTANCE
            new_node = Node(new_pos)
            nodes.append(new_node)
            self.add_connection(new_node)
            # place_line(self.position, new_pos)
            # geometry.placeLine(
            #     self.editor, addY(self.position, 41), addY(new_pos, 41), Block("stone")
            # )

    # Draw the node and its connections
    def draw(self):
        # for connection in self.connections:
        #     # place_line(self.position, connection.position)
        #     geometry.placeLine(
        #         self.editor,
        #         addY(self.position, 41),
        #         addY(connection.position, 41),
        #         Block("stone"),
        #     )
        # place(self.position)
        self.editor.placeBlock((self.position.x, 41, self.position.y), Block("stone"))
