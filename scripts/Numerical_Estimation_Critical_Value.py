import numpy as np
import loky
from loky import as_completed
import random
import operator
'''
attemps         :      The total number of contact processes that are tried.
thres           :      The total number of infections required to declare survival
max_dimension   :      The largest dimension for which we will determine the critical probability.
'''

attempts = 25
thres = 500
max_dimension = 20
max_steps = np.inf
neighbour_offset = []
'''
Node object to represent each node in the contact process
Each node has an infected status and a count of uninfected neighbours
'''
class Node:
    def __init__(self, infected = True, uninfected_neighbours=2):
        self.infected = infected
        self.uninfected_neighbours = uninfected_neighbours
    def __repr__(self):
        return f"Node(infected={self.infected}, uninfected_neighbours={self.uninfected_neighbours})"
'''
Runs one timestep of the contact process
total_infections    :    Total number of infections in the system
total_rate          :    Total rate of infection in the system
key_list            :    List of keys representing the current state of the system
contact_process     :    Dictionary representing the current state of the system
rate                :    The rate of infection
Returns the updated list of keys, contact process, total infections, and total rate
'''
def time_step(total_infections, total_rate, key_list, contact_process, rate):
    infection = np.random.uniform(0, 1) < total_rate / (total_infections + total_rate)
    if(not infection):
        index = np.random.randint(0, len(key_list))
        toheal = key_list[index]
        contact_process[toheal].infected = False
        total_rate -= contact_process[key_list[index]].uninfected_neighbours * rate
        total_infections -= 1
        for offset in neighbour_offset:
            neighbour_key = tuple(map(operator.add, key_list[index], offset))
            contact_process[neighbour_key].uninfected_neighbours += 1 
            if contact_process[neighbour_key].infected:
                total_rate += rate
        key_list[index] = key_list[-1]
        key_list.pop()
    elif(infection):
        options = []
        infect = random.choices(key_list, weights=[contact_process[key].uninfected_neighbours for key in key_list], k=1)[0]
        for offset in neighbour_offset:
            neighbour_key = tuple(map(operator.add, infect, offset))
            if neighbour_key in contact_process and not contact_process[neighbour_key].infected:
                options.append(neighbour_key)

        new = np.random.randint(0,len(options))
        contact_process[options[new]].infected = True
        total_rate += contact_process[options[new]].uninfected_neighbours * rate
        total_infections += 1
        key_list.append(options[new])
        for offset in neighbour_offset:
            neighbour_key = tuple(map(operator.add, options[new], offset))
            if neighbour_key not in contact_process:
                contact_process[neighbour_key] = Node(False, 2*dimension - 1)
            else:
                contact_process[neighbour_key].uninfected_neighbours -= 1
                if contact_process[neighbour_key].infected:
                    total_rate -= rate
    return total_infections, total_rate, key_list, contact_process

''' 
Threshold   :    The threshold for the number of infections
dimension   :    Dimension of the graph Z^d
Run one iteration of the contact process until the number of infections is greater than 100 or smaller or equal to 0
Returns True if the number of infections is greater than or equal to the threshold, False otherwise
'''
ti = 0
tr = 0
def run_contact_process(rate, dimension):
    akeys_lst = []
    akeys_lst.append(tuple((0 for _ in range(dimension))))
    cprocess = {tuple([0 for _ in range(dimension)]): Node(True, 2*dimension)}
    for i in range(dimension):
        for offset in [1, -1]:
            neighbour_key = tuple(tuple((0 for _ in range(dimension)))[j] + (offset if j == i else 0) for j in range(dimension))
            cprocess[neighbour_key] = Node(False, 2*dimension - 1)
    ti = 1
    tr = 2 * rate * dimension
    steps = 0
    while ti < thres and ti > 0 and steps < max_steps:
        steps += 1
        ti, tr, akeys_lst, cprocess = time_step(ti,tr,akeys_lst, cprocess, rate)
    if ti >= thres:
        return True 
    return False

'''' 
low         :    The lower bound for the critical value
high        :    The upper bound for the critical value 
attempts    :    The number of attempts to run the contact process
epsilon     :    The tolerance for the bisection method
dimension   :    Dimension of the graph Z^d
Given a lower and upper bound, estimate the critical value using bisection method.
Returns lower and upper estimate for the critical value
'''
def crit_value_bisection(low, high, attempts, epsilon, dimension):
    with loky.get_reusable_executor(max_workers=14) as executor:
        while high - low > epsilon:
            found_true = False
            tasks_completed = 0
            mid = (low + high) / 2
            futures = set()
            for _ in range(attempts):
                future = executor.submit(run_contact_process, mid, dimension)
                futures.add(future)
            for future in as_completed(futures): 
                tasks_completed += 1
                result = future.result()
                if result:
                    found_true = True
                if found_true:
                    break
            if found_true:
                high = mid
            else:
                low = mid
            print(f"The critical value is likely between {low:.6f} and {high:.6f}.")
    return high, low

'''
Determine the critical value in for various dimensions.
'''
for dimension in range(1, max_dimension + 1):
    neighbour_offset = []
    for i in range(dimension):
        for offset in [1, -1]:
            neighbour_offset.append([offset if j == i else 0 for j in range(dimension)])
    rate_low = 1/(2*dimension - 1)
    rate_high = 2/(dimension)
    rate_high, rate_low = crit_value_bisection(rate_low, rate_high, attempts, 0.001, dimension)
    print(f"The critical value in dimension {dimension} is likely between {rate_low:.6f} and {rate_high:.6f}.") 