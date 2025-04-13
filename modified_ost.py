from base_rbt_ost import *

class data_for_inserts(data):
    def __init__(self, value: datetime, queue=None):  # value is the time, queue is the value
        super().__init__(value)
        self.queue = queue
        self.id = self
    
    def get_id(self):
        return self.id

class data_consistency(data):
    def __init__(self, value: datetime, prefix=int):  # value is the time, queue is the value
        super().__init__(value)
        self.prefix = prefix
        # prefix is a value of -1, 0 or 1, -1 for deletion, 0 for inserts that are currently in the queue, 1 for inserts that are no more in the queue

class RBT_inserts(RBT):
    def return_queue(self, rank: int):
        curr_node = self.root
        while curr_node is not None:
            left_size = curr_node.left.size if curr_node.left else 0

            if rank < left_size:
                curr_node = curr_node.left
            elif rank > left_size:
                rank -= left_size + 1
                curr_node = curr_node.right
            else:
                return curr_node.queue
        return None

class RBT_consistency(RBT):
    def check_if_possible(self, node): 
        # returns if it's possible to delete the node
        curr_node = self.root        
        stack = []
        curr_sum = 0
        last_node_value = None
        
        while stack or curr_node:
            while curr_node:
                stack.append(curr_node)
                curr_node = curr_node.left
            curr_node = stack.pop()
            curr_sum += curr_node.prefix
            last_node_value = curr_node.value
            if curr_sum <= 0 and curr_node.value >= node.value:
                return False
            curr_node = curr_node.right
        
        # If there's no "bridge" found, then return true
        if curr_sum == 0 and node.value > last_node_value:
            # if we already make all the inorder and node value stills be bigger, we are at curr time
            return False
        return True
    
    def _print_inorder_recursive(self, curr_node):
        if curr_node:
            self._print_inorder_recursive(curr_node.left)
            print("(", curr_node.value, ",", curr_node.prefix, ")" ,end = " ; ")
            self._print_inorder_recursive(curr_node.right)

class node_insert(node):
    def __init__(self, newdata: datetime, queue=None):  # newdata is the time, queue is the value
        self.tree = RBT_inserts()
        if newdata is not None:
            self.tree.add_node(data_for_inserts(value=newdata, queue=queue))

    def add_node(self, new_node: 'node_insert'):
        if new_node is not None and new_node.tree.root is not None:
            aux_node = data_for_inserts(value=new_node.tree.root.value, queue=new_node.tree.root.queue)
            self.tree.add_node(aux_node)
            return aux_node.get_id()
    
    def return_value(self, rank: int):
        return self.tree.return_queue(rank)

class node_delete(node):
    def __init__(self, newdata: datetime):  # newdata is the time
        self.tree = RBT()
        if newdata is not None:
            self.tree.add_node(data(value=newdata))
 
    def add_node(self, new_node: 'node_delete'):
        if new_node is not None and new_node.tree.root is not None:
            self.tree.add_node(data(value=new_node.tree.root.value))

class node_consistency(node):
    def __init__(self, newdata: datetime, prefix: int):  # newdata is the time
        self.tree = RBT_consistency()
        if newdata is not None:
            self.tree.add_node(data_consistency(value=newdata, prefix=prefix))

    def add_node(self, new_node: 'node_consistency'):
        if new_node is not None and new_node.tree.root is not None:
            if new_node.tree.root.prefix >= 0:  # if insert, just add
                self.tree.add_node(data_consistency(value=new_node.tree.root.value, prefix=new_node.tree.root.prefix))
                return True
            else:  # if delete, check if it's possible before
                aux = self.tree.check_if_possible(new_node.tree.root)
                if aux:
                    self.tree.add_node(data_consistency(value=new_node.tree.root.value, prefix=new_node.tree.root.prefix))
                    return True
                return False
    
    def check_if_possible(self, node):
        return self.tree.check_if_possible(node)
    
    def delete(self, value: datetime, prefix: int):
        if prefix == 1: # should check for consistency, is like adding a deletion
            aux = self.tree.check_if_possible(data_consistency(value, -1))
            if aux:
                self.tree.delete(value)
                return True
            else:
                print("Error, can't be made")
                return False
            
        elif prefix == -1:
            self.tree.delete(value)
            return True
        else:
            print("Error, prefix must be 1 or -1")
            return False