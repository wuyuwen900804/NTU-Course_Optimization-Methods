with open('2010_ga_data.grt', 'r') as file:
    lines = file.readlines()

data = []
for line in lines:
    fields = line.split()
    if len(fields) != 0:
        data.append(fields)

data_demand = []
for i in range(len(data)):
    data_demand.append(int(data[i][4]))

with open('2010_ga_data_distance.grd', 'r') as file:
    lines = file.readlines()
data_dist = [int(line.strip()) for line in lines]

# Calculate the total coverage of the stations in the list
def SumCover(selected):
    copy_data_demand = data_demand.copy()
    total_num = len(data_demand)
    cover_demand_final = 0
    for i in selected:
        cover_demand = 0
        for k in range(total_num*i, total_num*(i+1)):
            if (data_dist[k] <= 25):
                cover_demand += copy_data_demand[k%159]
        cover_demand_final += cover_demand
        for k in range(total_num*i, total_num*(i+1)):
            if (data_dist[k] <= 25):
                copy_data_demand[k%159] = 0
    return cover_demand_final

# Add the station that can increase the coverage by the n-th largest amount to the temp list.
def Greedy(temp, maxorder):
    check_demand = []
    for i in range(len(data_demand)):
        check_demand.append(SumCover(temp+[i]))
    append_demand = check_demand.index(sorted(check_demand, reverse=True)[maxorder])
    temp.append(append_demand)
    return temp

facility_num = 15
final_select = []
for run in range(facility_num//3):
    select_list = final_select
    for i in range(6):
        for j in range(6):
            temp_list = final_select.copy()
            temp_list = Greedy(temp_list, i)
            temp_list = Greedy(temp_list, j)
            temp_list = Greedy(temp_list, 0)
            if (SumCover(select_list) < SumCover(temp_list)):
                select_list = temp_list
    final_select = select_list

print('Total Cover:', final_select) # 8600752
print('Select:', SumCover(final_select)) # [30, 68, 7, 14, 103, 10, 120, 71, 22, 36, 134, 20, 58, 21, 2]