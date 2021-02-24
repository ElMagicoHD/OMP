import uuid


# class for nodes with useful attributes and unique id using uuid4() maybe useful. Maybe not
class Node(object):

    def __init__(self, name, pos_x, pos_y):
        self.name = name
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.id = uuid.uuid4()
        self.edges = []
        self.left = None
        self.right = None
        

    def __eq__(self, other):
        return self.id == other.id and self.name == other.name

    def __str__(self):
        return "{}: {}, {}".format(self.name, self.pos_x, self.pos_y)

    def __hash__(self):
        return self.id

    def add_edge(self, edge):
        self.edges.append(edge)

    def get_edges(self):
        return self.edges

    def get_name(self):
        return self.name

    def get_pos(self):
        return self.pos_x, self.pos_y
