from edge_list import *

edge_list = sorted(edge_list, key=lambda x: x[2])
check = [[i] for i in range(42)]
degree = [0]*42
line_list = []
total = 0

for i in range(len(edge_list)):
    p1_deg = degree[edge_list[i][0]]
    p2_deg = degree[edge_list[i][1]]

    p1_pos = 0
    p2_pos = 0
    for index, sublist in enumerate(check):
        if edge_list[i][0] in sublist:
            p1_pos = index
        if edge_list[i][1] in sublist:
            p2_pos = index
   
    if (p1_deg < 2) and (p2_deg < 2) and (p1_pos != p2_pos):
        total += edge_list[i][2]
        for p in check[p2_pos]:
            check[p1_pos].append(p)
        del check[p2_pos]
        degree[edge_list[i][0]] += 1
        degree[edge_list[i][1]] += 1
        line_list.append([edge_list[i][0],edge_list[i][1]])
        
indices = [index for index, value in enumerate(degree) if value == 1]
line_list.append(indices)
for edge in edge_list:
    if (edge[0]==indices[0] and edge[1]==indices[1]) or (edge[1]==indices[0] and edge[0]==indices[1]):
        total += edge[2]

tour = []
line = line_list[0]
tour.extend(line)
initial, connect = line[0], line[1]

while connect != initial:
    for sublist in line_list:
        if (connect in sublist) and (sublist != line):
            connect = [p for p in sublist if p != connect][0]
            tour.append(connect)
            line = sublist
            break

print('Total Distance:', total)
print('Tour:', tour)