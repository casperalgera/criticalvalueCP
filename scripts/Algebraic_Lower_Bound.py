import sympy as sp
'''' 
First initialise key variables.  The variable initial is a dictionary that has all frontiers in a step, 
with the associated probability. In this dictionary, zeroes denote infected sites, crosses healthy ones.
The max number of iterations the program will run is stored in d. For the sympy algebra we define a 
symbol lambda.
'''
initial = { "xox" : 1}
d = 12
λ = sp.Symbol('λ')
'''
state   :   String that represents a frontier state.
Finds total rate of events that change the frontier.
'''
def getTotalRate(state):
    rate = 2*λ
    for i in range(1, len(state) - 1):
        rate += 1 if state[i] == 'o' else λ * (int(state[i - 1] == 'o') + int(state[i + 1] == 'o'))
    return rate
'''
string      :   String to change
insert      :   The value to insert into string
position    :   Position at which we will insert string
Returns string with insert inserted at position.
'''
def stringReplace(string, insert, position):
    return string[:position] + insert + string[position + 1:] 
'''
heal        :   A bool that indicates whether or not the event is a recovery
i           :   The current index in state
totalRate   :   The total rate of infection/healing in state
state       :   A string that indicates currect state of the frontier
probability :   The probability of reaching state
next        :   The dictionary of possible states with probabilities after one more event
Returns updated next with the events at i accounted for.
'''
def event(heal, i, totalRate, state, probability, next):
    if(heal):
        st = stringReplace(state, 'x', i)
        while st[1] == 'x' and st != 'xx':
            st = st[1:]
        while st[len(st) - 2] == 'x' and st != 'xx':
            st = st[:len(st) - 1]
        prob = probability * 1/totalRate
    else:
        st = stringReplace(state, 'xo' if i == 0 else 'ox' if i == len(state) - 1 else 'o', i)
        prob = probability * 1/totalRate * λ
    next[st] = next.get(st, 0) + prob
    return next
'''
state_dict  :   Dictionary with frontier states and associated probabilities
Returns the expected number of children with the frontier distribution state_dict.
'''
def expectation(state_dict):
    return sum(prob * state.count('o') for state, prob in state_dict.items())

'''
Using the event function, this snippet of code determine and prints the expect number
of infections after d frontier events. We loop through all states, and to all nodes
in these states, appending the result of every possible event with the associated
probability to next.
'''
next_state = initial
for index in range(d+1):
    next = {}
    for state in next_state:
        probability = next_state[state]
        totalRate = getTotalRate(state)
        if(state == "xx" ):
            if (state in next):
                next[state] += probability
            else:
                next.update({ state :  probability} )  
        elif(state != "xx" ):
            next = event(False, 0, totalRate, state, probability, next)
            next = event(False, len(state) - 1, totalRate, state, probability, next)
            for i in range(1, len(state) - 1):
                if state[i] == 'o':
                    next = event(True, i, totalRate, state, probability, next)
                else:
                    if state[i - 1] == 'o':
                        next = event(False, i, totalRate, state, probability, next)
                    if state[i + 1] == 'o':
                        next = event(False, i, totalRate, state, probability, next)
    next_state = next
    print(f"iteration {index}: λ = {sp.nsolve(expectation(next_state) - 1, λ, 1)}")
'''
We finally plot the solution to show how the expected value develops.
'''
p1 = sp.plot(expectation(next_state), xlim = (0, 3), ylim = (0,2), show=False)
p1.show()