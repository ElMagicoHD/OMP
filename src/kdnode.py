import uuid


class KdNode(object):

    def __init__(self, name, x_coord, y_coord):
        self.right = None
        self.left = None
        self.pos_x = x_coord
        self.pos_y = y_coord
        self.name = name
        self.id = uuid.uuid4()

    def __str__(self):
        return "{}: {}, {}".format(self.name, self.pos_x, self.pos_y)

    def __eq__(self, other):
        return self.id == other.id and self.pos_x == other.pos_x and self.pos_y == other.pos_y

    def __hash__(self):
        return self.id

    def is_leaf(self):
        return not self.right and not self.left
