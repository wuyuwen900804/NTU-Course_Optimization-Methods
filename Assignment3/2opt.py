import numpy as np
from edge_list import *

edge_array = np.array(edge_list)
def SumDistance(route):
    total = 0
    for i in range(len(route)-1):
        mask = (
            ((edge_array[:,0] == route[i]) & (edge_array[:,1] == route[i+1])) |
            ((edge_array[:,0] == route[i+1]) & (edge_array[:,1] == route[i]))
        )
        total += np.sum(edge_array[mask, 2])
    return total

# temp_route = full_route = [26, 25, 28, 27, 29, 30, 31, 32, 33, 34, 36, 37, 38, 39, 41, 0, 40, 1, 14, 13, 12,
#                            11, 10, 20, 21, 22, 16, 15, 17, 18, 19, 35, 2, 3, 4, 5, 6, 7, 8, 9, 24, 23, 26]
temp_route = full_route = [0, 40, 41, 1, 39, 38, 37, 36, 34, 33, 30, 29, 31, 32, 28, 27, 26, 25, 24, 23, 9,
                           8, 7, 6, 5, 4, 3, 2, 35, 20, 21, 22, 16, 15, 17, 18, 19, 12, 13, 14, 11, 10, 0]
last_min, next_min = 0, SumDistance(full_route)
runs = len(full_route) - 2

while True:
    full_route = temp_route
    improved = False
    for run in range(1, runs):
        subruns = runs - run + 1
        for subrun in range(subruns - 1):
            begin = 1 + subrun
            end = 1 + begin + run
            first_part, second_part, third_part = full_route[:begin], full_route[begin:end], full_route[end:]
            second_part.reverse()
            reversed_route = first_part + second_part + third_part
            if (SumDistance(reversed_route) < next_min):
                improved = True
                last_min = next_min
                next_min = SumDistance(reversed_route)
                temp_route = reversed_route
    if (improved == True):
        break

print('Total Distance:', SumDistance(full_route))
print('Tour:', full_route)