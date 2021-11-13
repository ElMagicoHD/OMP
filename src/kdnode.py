import uuid


class KdNode(object):
    """
    This is a class to represent nodes in a k-d-Tree.

    Attributes:
        right (KdNode): right child
        left (KdNode): left child
        pos (tuple): (x coordinate, y coordinate)
        name (String or numpy.int64): name
        id (uuid.uuid4): unique id
        axis (int): axis on which the subnodes will be divided

    """

    def __init__(self, name, x_coord, y_coord):
        self.right = None
        self.left = None
        self.pos = (x_coord, y_coord)
        self.name = name
        self.id = uuid.uuid4()
        self.axis = None

    def __str__(self):
        return "{}: {}, {}".format(self.name, self.pos[0], self.pos[1])

    def __eq__(self, other):
        return self.id == other.id and self.pos == other.pos

    def __hash__(self):
        return self.id

    def is_leaf(self):
        return not self.right and not self.left
