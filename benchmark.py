import random
from time import perf_counter
import datetime
import retroactive_queue


# not the best way to generate random datetime objects, but we aren't measuring this
def generate_random_test_data(n_elements):
    list_datetime = [0]*n_elements
    list_string = [0]*n_elements
    # generate n random datetime objects

    for i in range(n_elements):
        year = random.randint(2000, 2020)
        month = random.randint(1, 12)
        day = random.randint(1, 28)
        hour = random.randint(0, 23)
        minute = random.randint(0, 59)
        second = random.randint(0, 59)
        microsecond = random.randint(0, 999999)

        list_datetime[i] = datetime.datetime(year, month, day, hour, minute, second, microsecond)
    
    # generate n random strings
    for i in range(n_elements):
        list_string[i] = random.randint(0, 1000000)
    
    # merge so [time, value]
    for i in range(n_elements):
        list_datetime[i] = [list_datetime[i], list_string[i]]

    return list_datetime



def evaluate_add_performance(n):
    
    start = perf_counter()

    # add(random datetime, any value)
    for i in range(4): 
        queue = retroactive_queue.queue(datetime.datetime(2023, 1, 1, 12, 0, 0), "a")
        
        # add n elements
        for j in range(n):
            queue.add(mother_list[j][0], mother_list[j][1])
        
        # reset queue
        queue = None
    
    end = perf_counter()
    
    return end - start




mother_list = generate_random_test_data(100000)

for i in range(10):
    print(mother_list[i])