from datetime import datetime

class data:
    def __init__(self, value: datetime):  # value is the time
        self.value = value
        self.color = True  # Red is True, Black is False
        self.left = None
        self.right = None
        self.p = None  # Parent node
        self.size = 1  # Number of nodes in the subtree rooted at this node, by default 1


class RBT: # Red-Black Tree class augmented to ost
    def __init__(self):
        self.root = None

    def add_node(self, new_node):
        if self.root is None:
            new_node.color = False  # Root is always black
            self.root = new_node
        else:
            inserted_node = self._add_node_iterative(new_node)
            self._fix_tree(inserted_node)
    
    def _add_node_iterative(self, new_node):
        curr_node = self.root
        while True:
            curr_node.size += 1  # Increment size for each node in the path
            if new_node.value < curr_node.value:
                if curr_node.left is None:
                    curr_node.left = new_node
                    new_node.p = curr_node
                    break
                else:
                    curr_node = curr_node.left
            else:
                if curr_node.right is None:
                    curr_node.right = new_node
                    new_node.p = curr_node
                    break
                else:
                    curr_node = curr_node.right
        return new_node
    
    def _fix_tree(self, new_node):
        while new_node != self.root and new_node.p.color:
            if new_node.p == new_node.p.p.left:
                uncle = new_node.p.p.right
                if uncle and uncle.color:
                    new_node.p.color = uncle.color = False
                    new_node.p.p.color = True
                    new_node = new_node.p.p
                else:
                    if new_node == new_node.p.right:
                        new_node = new_node.p
                        self._left_rotate(new_node)
                    new_node.p.color = False
                    new_node.p.p.color = True
                    self._right_rotate(new_node.p.p)
            else:
                uncle = new_node.p.p.left
                if uncle and uncle.color:
                    new_node.p.color = uncle.color = False
                    new_node.p.p.color = True
                    new_node = new_node.p.p
                else:
                    if new_node == new_node.p.left:
                        new_node = new_node.p
                        self._right_rotate(new_node)
                    new_node.p.color = False
                    new_node.p.p.color = True
                    self._left_rotate(new_node.p.p)
        self.root.color = False
    
    def _left_rotate(self, x):
        y = x.right
        x.right = y.left
        if y.left:
            y.left.p = x
        y.p = x.p
        if x.p is None:
            self.root = y
        elif x == x.p.left:
            x.p.left = y
        else:
            x.p.right = y
        y.left = x
        x.p = y
    
        # Update sizes
        y.size = x.size
        x.size = 1 + (x.left.size if x.left else 0) + (x.right.size if x.right else 0)
    
    def _right_rotate(self, x):
        y = x.left
        x.left = y.right
        if y.right:
            y.right.p = x
        y.p = x.p
        if x.p is None:
            self.root = y
        elif x == x.p.right:
            x.p.right = y
        else:
            x.p.left = y
        y.right = x
        x.p = y
    
        # Update sizes
        y.size = x.size
        x.size = 1 + (x.left.size if x.left else 0) + (x.right.size if x.right else 0)

    def rank(self, value: datetime):
        curr_node = self.root
        rank = 0

        while curr_node:
            left_size = curr_node.left.size if curr_node.left else 0

            if value < curr_node.value:
                curr_node = curr_node.left
            elif value > curr_node.value:
                rank += 1 + left_size
                curr_node = curr_node.right
            elif value == curr_node.value:
                rank += left_size + 1
                break
            else:
                return False

        return rank - 1
    
    def previous_rank(self, value: datetime): 
        curr_node = self.root
        rank = 0
    
        while curr_node:
            left_size = curr_node.left.size if curr_node.left else 0
    
            if value <= curr_node.value:
                curr_node = curr_node.left
            else:
                rank += 1 + left_size
                curr_node = curr_node.right
    
        return rank - 1
    
    def previous_or_current_rank(self, value: datetime):
        curr_node = self.root
        rank = 0
    
        while curr_node:
            left_size = curr_node.left.size if curr_node.left else 0
    
            if value < curr_node.value:
                curr_node = curr_node.left
            elif value > curr_node.value:
                rank += 1 + left_size
                curr_node = curr_node.right
            elif value == curr_node.value:
                rank += left_size
                return rank
            else:
                rank += left_size
                return max(rank - 1, 0)
    
        return max(rank - 1, 0)
    
    def next_rank(self, value: datetime):
        curr_node = self.root
        rank = 0
    
        while curr_node:
            left_size = curr_node.left.size if curr_node.left else 0
    
            if value < curr_node.value:
                curr_node = curr_node.left
            elif value > curr_node.value:
                rank += 1 + left_size
                curr_node = curr_node.right
            else:  # value == curr_node.value
                rank += left_size
                return rank
    
        return rank

    def search(self, value: datetime):  # returns if it exists
        return self._search_recursive(self.root, value)

    def _search_recursive(self, curr_node, value: datetime):
        while curr_node:
            if value < curr_node.value:
                curr_node = curr_node.left
            elif value > curr_node.value:
                curr_node = curr_node.right
            else:
                return True
        return False

    def select(self, rank: int):  # returns the value at given rank
        curr_node = self.root
        while curr_node is not None:
            left_size = curr_node.left.size if curr_node.left else 0

            if rank < left_size:
                curr_node = curr_node.left
            elif rank > left_size:
                rank -= left_size + 1
                curr_node = curr_node.right
            else:
                return curr_node.value
        return None
    
    def delete(self, value: datetime):
        self._delete_recursive(self.root, value)    

    def _delete_recursive(self, curr_node, value: datetime):
        if curr_node is None:
            return curr_node
        
        if value < curr_node.value:
            curr_node.left = self._delete_recursive(curr_node.left, value)
        elif value > curr_node.value:
            curr_node.right = self._delete_recursive(curr_node.right, value)
        else:
            if curr_node.left is None:
                temp = curr_node.right
                curr_node = None
                return temp
            elif curr_node.right is None:
                temp = curr_node.left
                curr_node = None
                return temp
            temp = self._min_value_node(curr_node.right)
            curr_node.value = temp.value
            curr_node.right = self._delete_recursive(curr_node.right, temp.value)
        
        # Update size
        curr_node.size = 1 + (curr_node.left.size if curr_node.left else 0) + (curr_node.right.size if curr_node.right else 0)
        return curr_node
    
    def _min_value_node(self, node):
        curr_node = node
        while curr_node.left is not None:
            curr_node = curr_node.left
        return curr_node
    
    def print_inorder(self):
        self._print_inorder_recursive(self.root)
    
    def _print_inorder_recursive(self, curr_node):
        if curr_node:
            self._print_inorder_recursive(curr_node.left)
            print(curr_node.value, end=" ")
            self._print_inorder_recursive(curr_node.right)
    
    def delete(self, value):
        self._delete_recursive(self.root, value)    

    def _delete_recursive(self, curr_node, value):
        if curr_node is None:
            return curr_node
        
        if value < curr_node.value:
            curr_node.left = self._delete_recursive(curr_node.left, value)
        elif value > curr_node.value:
            curr_node.right = self._delete_recursive(curr_node.right, value)
        else:
            if curr_node.left is None:
                temp = curr_node.right
                curr_node = None
                return temp
            elif curr_node.right is None:
                temp = curr_node.left
                curr_node = None
                return temp
            temp = self._min_value_node(curr_node.right)
            curr_node.value = temp.value
            curr_node.right = self._delete_recursive(curr_node.right, temp.value)
        
        # Update size
        curr_node.size = 1 + (curr_node.left.size if curr_node.left else 0) + (curr_node.right.size if curr_node.right else 0)
        return curr_node


class node:
    def __init__(self, newdata: datetime):  # newdata is the time
        self.tree = RBT()
        if newdata is not None:
            self.tree.add_node(data(value=newdata))
 
    def add_node(self, new_node: 'node'):
        if new_node is not None and new_node.tree.root is not None:
            self.tree.add_node(data(value=new_node.tree.root.value))
 
    def select(self, k: int):
        return self.tree.select(k)

    def root_data(self):
        return self.tree.root.value if self.tree.root is not None else None

    def rank(self, data: datetime):
        return self.tree.rank(data)
    
    def prev_rank(self, data: datetime):
        return self.tree.previous_rank(data)
    
    def prev_or_curr_rank(self, data: datetime):
        return self.tree.previous_or_current_rank(data)
    
    def next_rank(self, data: datetime):
        return self.tree.next_rank(data)
 
    def print_in_order(self):
        self.tree.print_inorder()
    
    def search(self, value: datetime):
        return self.tree.search(value)

    def delete(self, value: datetime):
        self.tree.delete(value)
    
    def get_size(self):
        return self.tree.root.size if self.tree.root is not None else 0