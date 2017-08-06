class Node:
    """ Describes a node in a graph, and the edges connected
        to that node."""
    def __repr__(self):
        return "{} {}".format(self.id, self.data.name)
    def __init__(self, ID, neighbors, data, truth=None, file_path=None):
        """ Parameters
            ----------
            ID : int
                A unique identifier for this node. Should be a
                value in [0, N-1], if there are N nodes in total.

            neighbors : Dictionary
                Neighbor-ID: Edge weight

            data : Profile
                Profile of Node

            truth : Optional[str]
                If you have truth data, for checking your clustering algorithm,
                you can include the label to check your clusters at the end.

                If this node corresponds to a picture of Ryan, this truth
                value can just be "Ryan"

            file_path : Optional[str]
                The file path of the image corresponding to this node, so
                that you can sort the photos after you run your clustering
                algorithm

            """
        self.id = ID

        # The node's label is initialized with the node's ID value at first,
        # this label is then updated during the whispers algorithm
        self.label = ID

        # (n1_ID, n2_ID, ...)
        # The IDs of this nodes neighbors. Empty if no neighbors
        self.neighbors = neighbors
        self.data = data

        self.truth = truth
        self.file_path = file_path