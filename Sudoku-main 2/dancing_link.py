import numpy as np

class DancingLinkNode:
    """Nodes in a Dancing Links data structure. Each node stores the pointer to the node above it, 
    below it, on its left and on its right. For this project, we only need to store the row and column 
    indexes of these nodes.
    """

    def __init__(self, row: int, col: int, head: 'DancingLinkNode' = None) -> None:
        """Create a new Dancing Links node at given row and column. The row index of
        column head node are -1, and the row and column index of root node are both -1.

        The rows and columns of Dancing Links are all circular linked lists, so for all new Nodes
        its all four pointers initially point to itself.

        Args:
            row (int): the row index
            col (int): the column index
            head (DancingLinkNode): the head of the column this node in. If this node itself is the head
            or root then leave this None
        """
        self.__left: 'DancingLinkNode' = self
        self.__right: 'DancingLinkNode' = self
        self.__above: 'DancingLinkNode' = self
        self.__below: 'DancingLinkNode' = self

        if head != None:
            self.__head = head
        else : 
            self.__head: 'DancingLinkNode' = self
        self.__loc = (row, col)

    def get_left(self) -> 'DancingLinkNode':
        """
        Returns:
            DancingLinkNode: the node on the left of this node.
        """
        return self.__left
    
    def get_right(self) -> 'DancingLinkNode':
        """
        Returns:
            DancingLinkNode: the node on the right of this node.
        """
        return self.__right
    
    def get_above(self) -> 'DancingLinkNode':
        """
        Returns:
            DancingLinkNode: the node above this node.
        """
        return self.__above
    
    def get_below(self) -> 'DancingLinkNode':
        """
        Returns:
            DancingLinkNode: the node below this node.
        """
        return self.__below
    
    def get_head(self) -> 'DancingLinkNode':
        """
        Returns:
            DancingLinkNode: the head node of the column this node in 
        """
        return self.__head

    def set_left(self, node: 'DancingLinkNode'):
        """Set the node on the left of this node.
        """
        self.__left = node

    def set_right(self, node: 'DancingLinkNode'):
        """Set the node on the left of this node.
        """
        self.__right = node

    def set_above(self, node: 'DancingLinkNode'):
        """Set the node on the left of this node.
        """
        self.__above = node

    def set_below(self, node: 'DancingLinkNode'):
        """Set the node on the left of this node.
        """
        self.__below = node

    def get_loc(self) -> tuple[int, int]:
        """
        Returns:
            tuple[int, int]: the (row, col) tuple of this node. 
            The row index of head Nodes are -1, and the row and column index of root node are both -1.
        """
        return self.__loc
    
class DancingLinks:
    """The Dancing Links data structure.
    """

    def __init__(self, row: int, col: int) -> None:
        """Create a new Dancing Links with give rows and columns.

        Args:
            row (int): number of rows in this Dancing Links (except heads)
            col (int): number of columns in this Dancing Links.
        """
        self.__shape = (row, col)
        self.__root = DancingLinkNode(-1, -1)
        self.__build()
        self.__col_nodes_count = np.zeros(col, int)
        self.__row_count = 0

    def __build(self):
        """Build this Dancing Links, generate the root node and all column heads
        """
        prev = self.__root
        for c in range(self.__shape[1]):
            node = DancingLinkNode(-1, c)
            prev.set_right(node)
            node.set_left(prev)
            prev = node
        # connect the last column head node back to the root
        prev.set_right(self.__root)
        self.__root.set_left(prev)

    def append_row(self, col_indexes: list[int], row_index = -1):
        """Append a new row to this Dancing Links

        Args:
            col_indexes (list[int]): the list of column indexes of Nodes in this row
            row_index (int): the index of the row to insert. If not specified then the row will be 
            appended at the end
        """
        if row_index == -1:
            row_index = self.__row_count
        row_first = None
        for col_index in col_indexes:
            # search the column to the new node located in
            head = self.__root.get_right()
            while head != self.__root:
                if head.get_loc()[1] == col_index:
                    # create new node at given location
                    node = DancingLinkNode(row_index, col_index, head)
                    # append new nodes at the bottom of their column
                    head.get_above().set_below(node)
                    node.set_above(head.get_above())
                    head.set_above(node)
                    node.set_below(head)
                    # add 1 to node count of current column
                    self.__col_nodes_count[head.get_loc()[1]] += 1
                    if row_first == None:
                        row_first = node
                    # connect those nodes in that new row
                    row_first.get_left().set_right(node)
                    node.set_left(row_first.get_left())
                    row_first.set_left(node)
                    node.set_right(row_first)
                    break
                head = head.get_right()
        self.__row_count += 1

    def remove_index(self, col_index: int) -> DancingLinkNode:
        """Remove the column at given index and all the rows that share Nodes with this column

        Args:
            col_index (int): the index of the column to be remove
    
        Returns:
            DancingLinkNode: the head of the removed column
        """
        head = self.__root.get_right()
        while head != self.__root:
            if head.get_loc()[1] == col_index:
                head.get_left().set_right(head.get_right())
                head.get_right().set_left(head.get_left())
                current = head.get_below()
                while current != head:
                    node = current.get_right()
                    while node != current:
                        node.get_above().set_below(node.get_below())
                        node.get_below().set_above(node.get_above())
                        node = node.get_right()
                    current = current.get_below()
                    # minus 1 to node count of current column
                    self.__col_nodes_count[head.get_loc()[1]] -= 1
                return head
            head = head.get_right()
        else:
            #print('column not found')
            return None

    def remove(self, head: DancingLinkNode):
        """Remove the column of given head node and all the rows that share Nodes with this column

        Args:
            head (DancingLinkNode): head node of the column to remove
        """
        # disconnect the head node from the head row
        head.get_left().set_right(head.get_right())
        head.get_right().set_left(head.get_left())
        # go through all the nodes in this column
        current = head.get_below()
        while current != head:
            # go through all the nodes in the same row as current node
            node = current.get_right()
            while node != current:
                # discnnect these nodes from their columns
                node.get_above().set_below(node.get_below())
                node.get_below().set_above(node.get_above())
                node = node.get_right()
            current = current.get_below()
        # minus 1 to node count of current column
        self.__col_nodes_count[head.get_loc()[1]] -= 1
        #print('remove col ', head.get_loc()[1])
        #print(self)


    def recover(self, head: DancingLinkNode):
        """Recover the column and related rows removed with the given head node

        Args:
            head (DancingLinkNode): head node of the head to recover
        """
        # connect the head node back to the head row
        head.get_left().set_right(head)
        head.get_right().set_left(head)
        # go through all the nodes in this column
        current = head.get_below()
        while current != head:
            # go through all the nodes in the same row as the current node
            node = current.get_right()
            while node != current:
                # connect these nodes back to their column
                node.get_above().set_below(node)
                node.get_below().set_above(node)
                node = node.get_right()
            current = current.get_below()
        # add 1 to node count of current column
        self.__col_nodes_count[head.get_loc()[1]] += 1
        #print('recover col ', head.get_loc()[1])
        #print(self)
        

    def dancing(self, ans_list: list[set], ans_count: int = 1, ans: list[int] = None):
        """Solve the Exact Cover Problem, record the indexes of subsets in the given list

        Args:
            ans_list(list[set]): list to record current sulotions
            ans_count: expected count of solutions, default value is 1
            ans (list[int]): list to record a possible answer, default value is an empty list

        Returns:
            bool: whether enough answers are found
        """
        #print(ans)
        if ans == None:
            ans = []
        # check whether there are still head nodes in head row. If not, then the node
        # at the right of the root node will be the root node itself, and at this time
        # the whole Dancing Links is empty, meaning an answer is found.
        if self.__root.get_right() == self.__root:
            ans_set = set(ans.copy())
            if ans_set not in ans_list:
                ans_list.append(ans_set)
            else:
                print('repeat')
            #print('empty!', len(ans_list))
            return len(ans_list) == ans_count
        
        # if there are still head nodes in head row, check whether all remaining columns
        # still contain at least one node in them. If one column does not, then the node
        # below the head of that column will be the head itself. This means this column 
        # is not covered and the current answer must be wrong.
        head = self.__root.get_right()
        min_head = head
        while head != self.__root:
            if head.get_below() == head:
                #print('not covered', head.get_loc()[1])
                return False
            # sort the heads based on the number of nodes in their columns
            if self.__col_nodes_count[min_head.get_loc()[1]] > self.__col_nodes_count[head.get_loc()[1]]:
                min_head = head

            head = head.get_right()
        ## keep removing columns and rows and call this function recursively
        # remove the column with the fewest nodes
        head = min_head
        #print('remove col head', head.get_loc()[1])
        self.remove(head)
        # go through nodes in the removed column
        current = head.get_below()
        while current != head:
            # choose the row this node in as part of the answer
            ans.append(current.get_loc()[0])
            removed = [] # record the removed column head
            node = current.get_right()
            # remove all columns that share node with this row
            #print('remove row', current.get_loc()[0])
            while node != current:
                removed.append(node.get_head())
                self.remove(node.get_head())
                node = node.get_right()
            # call this function recursively, check whether an answer is found. If do,
            # stop recursion and return True, or keep checking other possible answers
            if self.dancing(ans_list, ans_count = ans_count, ans = ans):
                return True
            # recover those removed rows and columns
            #print('recover row', current.get_loc()[0])
            while len(removed) > 0:
                self.recover(removed.pop())
            ans.pop()
            current = current.get_below()
        # recover this removed head
        #print('recover col head', head.get_loc()[1])
        self.recover(head)
        return False

    def to_array(self) -> np.ndarray:
        arr = np.zeros((self.__shape[0] + 1, self.__shape[1]), int)
        for c in range(self.__shape[1]):
            arr[0, c] = -1
        head = self.__root.get_right()
        while head != self.__root:
            arr[head.get_loc()[0] + 1, head.get_loc()[1]] = head.get_loc()[1]
            current = head.get_below()
            while current != head:
                arr[current.get_loc()[0] + 1, current.get_loc()[1]] = 1
                current = current.get_below()
            head = head.get_right()
        return arr


    def __str__(self) -> str:
        np.set_printoptions(threshold=np.inf, linewidth=np.inf)
        out = str(self.to_array())
        return out[:out.index('\n')].replace('-1', ' _') + out[out.index('\n'):].replace('0', '.')
 
'''s3 = [5, 9, 17]
s2 = [1, 8, 119]
s1 = [3, 5, 17]
s4 = [1, 8]
s5 = [3, 119]
s6 = [3]
x = [1, 3, 5, 8, 9, 17, 119]
s = [s1, s2, s3, s4, s5, s6]

dl = DancingLinks(len(s), len(x))
print(dl)
for i in s:
    dl.append_row(x.index(e) for e in i)
print(dl) 
ans = []
dl.dancing(ans, 3)
print(ans)'''
