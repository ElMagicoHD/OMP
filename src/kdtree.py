import kdnode
import pandas as pd


class KdTree(object):

    def __init__(self):
        self.root = None
        self.depth = 0

    def build_tree(self, nodes_list):
        self._build_tree(nodes_list=nodes_list)

    def _build_tree(self, nodes_list: pd.DataFrame, depth: int = 0) -> None:
        if nodes_list.shape[1] <= 0 or nodes_list.shape[0] <= 0:
            return None
        # sort nodes_list alternating by x and y axis

        sorted_nodes = nodes_list.sort_values(by=[depth % 2], axis=1)
        # middle of sorted list
        middle = sorted_nodes.iloc[:, sorted_nodes.shape[1] // 2]

        self.root = kdnode.KdNode(name=middle.name, x_coord=middle[0], y_coord=middle[1])
        # left part of sorted_nodes
        self.root.left = self.__build_tree(nodes_list=sorted_nodes.iloc[:, : sorted_nodes.shape[1] // 2],
                                           depth=depth + 1)
        # right part of sorted_nodes
        self.root.right = self.__build_tree(nodes_list=sorted_nodes.iloc[:, (sorted_nodes.shape[1] // 2) + 1:],
                                            depth=depth + 1)

    def __build_tree(self, nodes_list, depth=1):
        if nodes_list.shape[1] <= 0 or nodes_list.shape[0] <= 0:
            self.depth = depth
            return None

        sorted_nodes = nodes_list.sort_values(by=[depth % 2], axis=1)

        # middle of sorted list
        middle = sorted_nodes.iloc[:, sorted_nodes.shape[1] // 2]

        middle_node = kdnode.KdNode(name=middle.name, x_coord=middle[0], y_coord=middle[1])
        # left part of sorted_nodes
        middle_node.left = self.__build_tree(nodes_list=sorted_nodes.iloc[:, : sorted_nodes.shape[1] // 2],
                                             depth=depth + 1)
        # right part of sorted_nodes
        middle_node.right = self.__build_tree(nodes_list=sorted_nodes.iloc[:, : sorted_nodes.shape[1] // 2],
                                              depth=depth + 1)
        return middle_node
