import kdnode
import pandas as pd


def euclidean_distance(px1, py1, px2, py2):
    tmp = (px2 - px1) ** 2
    tmp += (py2 - py1) ** 2
    return tmp


def closer_distance(pos, p1, p2):
    if not p1:
        return p2
    if not p2:
        return p2

    distance1 = euclidean_distance(pos[0], pos[1], p1.pos[0], p1.pos[1])
    distance2 = euclidean_distance(pos[0], pos[1], p2.pos[0], p2.pos[1])

    if distance1 < distance2:
        return p1
    else:
        return p2


class KdTree(object):

    def __init__(self):
        self.root = None
        self.depth = 0

    def build_tree(self, nodes_list):
        self._build_tree(nodes_list=nodes_list)

    def _build_tree(self, nodes_list: pd.DataFrame, depth: int = 0) -> None:
        if nodes_list.shape[1] <= 0 or nodes_list.shape[0] <= 0:
            self.depth = depth
            return None
        # sort nodes_list alternating by x and y axis
        splitting_axis = depth % 2
        sorted_nodes = nodes_list.sort_values(by=splitting_axis, axis=1)
        # middle of sorted list
        median = sorted_nodes.shape[1] // 2
        middle = sorted_nodes.iloc[:, median]
        self.root = kdnode.KdNode(name=middle.name, x_coord=middle[0], y_coord=middle[1])
        self.root.axis = splitting_axis
        # left part of sorted_nodes
        self.root.left = self.__build_tree(nodes_list=sorted_nodes.iloc[:, : median],
                                           depth=depth + 1)
        # right part of sorted_nodes
        self.root.right = self.__build_tree(nodes_list=sorted_nodes.iloc[:, median + 1:],
                                            depth=depth + 1)

    def __build_tree(self, nodes_list, depth: int = 1) -> kdnode.KdNode:
        if nodes_list.shape[1] <= 0 or nodes_list.shape[0] <= 0:
            self.depth = depth
            return None

        splitting_axis = depth % 2
        sorted_nodes = nodes_list.sort_values(by=splitting_axis, axis=1)
        #median_value = nodes_list.median(axis=1)[splitting_axis] could be used to improve build time further

        # middle of sorted list
        median = sorted_nodes.shape[1] // 2
        middle = sorted_nodes.iloc[:, median]

        middle_node = kdnode.KdNode(name=middle.name, x_coord=middle[0], y_coord=middle[1])
        middle_node.axis = splitting_axis
        # left part of sorted_nodes
        middle_node.left = self.__build_tree(nodes_list=sorted_nodes.iloc[:, : median], depth=depth + 1)
        # right part of sorted_nodes
        middle_node.right = self.__build_tree(nodes_list=sorted_nodes.iloc[:, median + 1:], depth=depth + 1)
        return middle_node

    def nearest_neighbor(self, pos):
        if self.root is None:
            return None
        if pos is None:
            return None
        else:
            return self._nearest_neighbor(pos, self.root)

    # help from https://github.com/tsoding/kdtree-in-python/blob/master/main.py
    def _nearest_neighbor(self, pos, node):

        # leaf case
        if pos is None:
            return node
        if node is None:
            return None

        else:
            splitting_axis = node.axis

            if pos[splitting_axis] < node.pos[splitting_axis]:
                main_node = node.left
                alternative_node = node.right
            else:
                main_node = node.right
                alternative_node = node.left

            nearest = closer_distance(pos, self._nearest_neighbor(pos=pos, node=main_node), node)

            if euclidean_distance(pos[0], pos[1], node.pos[0], node.pos[1]) > (
                    pos[splitting_axis] - node.pos[splitting_axis])**2:
                nearest = closer_distance(pos, self._nearest_neighbor(pos=pos, node=alternative_node), nearest)

            return nearest
