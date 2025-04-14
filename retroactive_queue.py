import modified_ost as ost
from datetime import datetime

class queue:
    def __init__(self, time: datetime, value): 
        self.adding = ost.node_insert(time, value) 
        self.deleting = None 
        self.consistency = ost.node_consistency(time, 1) 
        
    def push(self, time: datetime, value): 
        flag = self.consistency.search(time)
        if flag:
            print("Time already present")
            return
        
        aux_node = ost.node_insert(newdata=time, queue=value)
        
        self.consistency.add_node(ost.node_consistency(time, 1))
        return self.adding.add_node(aux_node)
    
    def pop(self, time: datetime): 
        if self.deleting is None:
            self.deleting = ost.node_delete(time) 
            self.consistency.add_node(ost.node_consistency(time, -1))
            return self.front(time)
        else:
            flag = self.consistency.add_node(ost.node_consistency(time, -1)) 
            if not flag:
                return "error, can't be made"
        
            self.deleting.add_node(ost.node_delete(newdata=time))

            return self.front(time)
    
    def size(self, time: datetime): 
        rank_last_push_before_time = self.adding.prev_or_curr_rank(time)
        rank_last_pop_before_time = self.deleting.prev_or_curr_rank(time)

        size = rank_last_push_before_time - rank_last_pop_before_time 

        return size + 1
    
    def front(self, time: datetime):
        rank_last_push_before_time = self.adding.prev_or_curr_rank(time) 
        rank_last_pop_before_time = self.deleting.prev_or_curr_rank(time)

        size_queue_at_time = rank_last_push_before_time - rank_last_pop_before_time
        rank_value = rank_last_push_before_time - size_queue_at_time
        return self.adding.return_value(rank_value)

    def print_in_order(self):
        print("adding: ")
        self.adding.print_in_order()
        print("\ndeleting: ")
        self.deleting.print_in_order()
        print("\nconsistency: ")
        self.consistency.print_in_order()
        print("\n")
    
    def print(self, time):
        rank_last_push_before_time = self.adding.prev_or_curr_rank(time)
        
        if self.deleting is None:
            rank_last_pop_before_time = -1
        else:
            if self.deleting.select(0) == 0:
                rank_last_pop_before_time = -1
            rank_last_pop_before_time = self.deleting.prev_or_curr_rank(time)
        
        size_queue_at_time = rank_last_push_before_time - rank_last_pop_before_time
        aux_list = [None] * (size_queue_at_time)
        for i in range(0, size_queue_at_time):
            rank_value = rank_last_push_before_time - i
            aux_list[i] = self.adding.return_value(rank_value)

        print("queue at time: ", time, " is: ", aux_list)
        return aux_list
    
    def undo(self, time: datetime):
        # 2 cases, undo a push or undo a pop
        if self.adding.search(time): # should add check_if_possible function
            if self.consistency.check_if_possible(time):
                time = time.value
                self.adding.delete(time)
                self.consistency.delete(time)
            else:
                print("Can't undo push")
            return
        elif self.deleting.search(time):
            self.deleting.delete(time)
            self.consistency.delete(time)
            return
        else:
            print("Time not found")
            return


class queue_linked(queue):
    def __init__(self, time: datetime, value): 
        self.adding = ost.node_insert(time, value) 
        self.deleting = None 
        self.consistency = ost.node_consistency_linked(time, 1) 
    
    def push(self, time: datetime, value): 
        flag = self.consistency.search(time)
        if flag:
            print("Time already present")
            return
        
        aux_node = ost.node_insert(newdata=time, queue=value)
        
        self.consistency.add_node(ost.node_consistency_linked(time, 1))
        return self.adding.add_node(aux_node)
    
    def pop(self, time: datetime): 
        if self.deleting is None:
            self.deleting = ost.node_delete(time) 
            self.consistency.add_node(ost.node_consistency_linked(time, -1))
            return self.front(time)
        else:
            flag = self.consistency.add_node(ost.node_consistency_linked(time, -1)) 
            if not flag:
                return "error, can't be made"
        
            self.deleting.add_node(ost.node_delete(newdata=time))

            return self.front(time)

def show_info(q , datetime_r, value):
    q.push(datetime_r, value)
    q.print(datetime_r)
    print("\n")

def show_pop(q, datetime_r):
    valor = q.pop(datetime_r)
    print("value: ", valor, ", pop at time: ", datetime_r)
    q.print(datetime_r)
    print("\n")


if __name__ == "__main__":
    q = queue(datetime(2023, 1, 1, 12, 0, 0), "a") # 0
    q.print(datetime(2023, 1, 1, 12, 0, 0))
    print("\n")

    show_info(q, datetime(2023, 1, 1, 12, 10, 0), "b") # 10
    show_info(q, datetime(2023, 1, 1, 12, 20, 0), "c") # 20

    show_pop(q, datetime(2023, 1, 1, 12, 30, 0)) # 30

    show_info(q, datetime(2023, 1, 1, 12, 40, 0), "d") # 30
    
    show_pop(q, datetime(2023, 1, 1, 12, 50, 0)) # 60

    show_pop(q, datetime(2023, 1, 1, 13, 0, 0)) # 0

    show_info(q, datetime(2023, 1, 1, 13, 20, 0), "e") # 70


    print("\n\nstart of time travel: ----------------------------\n\n")

    show_pop(q, datetime(2023, 1, 1, 12, 45, 0)) # 45

    print("not time travel:")
    show_pop(q, datetime(2023, 1, 1, 13, 30, 0)) # 90

    show_pop(q, datetime(2023, 1, 1, 13, 40, 0)) # 100
    show_pop(q, datetime(2023, 1, 1, 12, 35, 0)) # 55
    show_pop(q, datetime(2023, 1, 1, 12, 1, 0)) # 1
    show_pop(q, datetime(2023, 1, 1, 12, 15, 0)) # 15


    print("\n\nsame example with more inserts later ----------------------------\n\n")

    show_info(q, datetime(2023, 1, 1, 13, 50, 0), "f") # 110
    show_info(q, datetime(2023, 1, 1, 14, 0, 0), "g") # 120
    show_info(q, datetime(2023, 1, 1, 14, 10, 0), "h") # 130
    show_info(q, datetime(2023, 1, 1, 14, 20, 0), "i") # 140
    show_info(q, datetime(2023, 1, 1, 14, 30, 0), "j") # 150
    
    show_pop(q, datetime(2023, 1, 1, 13, 30, 0)) # 90
    show_pop(q, datetime(2023, 1, 1, 13, 40, 0)) # 100
    show_pop(q, datetime(2023, 1, 1, 12, 35, 0)) # 55
    show_pop(q, datetime(2023, 1, 1, 12, 1, 0)) # 1