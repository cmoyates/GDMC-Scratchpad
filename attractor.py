from gdpc import Editor, Block
from glm import ivec2

# Define the class for attractors
class Attractor:
    def __init__(self, editor: Editor, position: ivec2, weight):
        self.position = position
        self.weight = weight
        self.editor = editor

    # Draw the attractor
    def draw(self):
        print("Place")
        self.editor.placeBlock(
            (self.position.x, 41, self.position.y), Block("red_concrete")
        )
