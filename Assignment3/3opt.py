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

def ReverseList(route, begin, end):
    first_part, second_part, third_part = route[:begin], route[begin:end], route[end:]
    second_part.reverse()
    reversed_route = first_part + second_part + third_part
    return reversed_route

temp_route = full_route = [26, 25, 8, 7, 6, 5, 4, 3, 2, 1, 0, 41, 40, 39, 38, 37, 36, 35, 34, 33, 32, 31, 30,
                           29, 28, 27, 20, 21, 22, 16, 19, 18, 17, 15, 14, 13, 12, 11, 10, 9, 24, 23, 26]
# temp_route = full_route =  [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 17, 18, 19, 16, 22, 21, 20,
#                             28, 27, 26, 23, 24, 25, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 0]
last_min, next_min = 0, SumDistance(full_route)
runs = len(full_route) - 2

while True:
    i = 0
    full_route = temp_route
    improved = False
    for run_1 in range(1, runs):
        subruns_1 = runs - run_1 + 1
        for subrun_1 in range(subruns_1 - 1):
            begin_1 = 1 + subrun_1
            end_1 = 1 + begin_1 + run_1
            reversed_1 = ReverseList(full_route, begin_1, end_1)
            for run_2 in range(1, runs):
                subruns_2 = runs - run_2 + 1
                for subrun_2 in range(subruns_2 - 1):
                    begin_2 = 1 + subrun_2
                    end_2 = 1 + begin_2 + run_2
                    reversed_2 = ReverseList(reversed_1, begin_2, end_2)
                    if (SumDistance(reversed_2) < next_min):
                        improved = True
                        last_min = next_min
                        next_min = SumDistance(reversed_2)
                        temp_route = reversed_2
                        print('Recent Total Distance:', SumDistance(reversed_2))
                        print('Recent Tour:', temp_route)
    if (improved == True):
        break

print('Final Total Distance:', SumDistance(full_route))
print('Final Tour:', full_route)
# Final Total Distance: 704
# Final Tour: [26, 23, 10, 11, 22, 21, 16, 12, 13, 14, 15, 17, 18, 19, 20, 27, 28, 29, 30, 31,
#              32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 24, 25, 26]
# Final Total Distance: 704
# Final Tour: [0, 41, 40, 39, 38, 37, 36, 35, 34, 33, 32, 31, 30, 29, 28, 27, 20, 19, 18, 17,
#              15, 14, 13, 12, 16, 21, 22, 11, 10, 23, 26, 25, 24, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0]