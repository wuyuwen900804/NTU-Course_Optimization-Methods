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

total_num = len(data_demand)
facility_num = 15
facility_select = []
cover_demand_final = 0

for i in range(facility_num):
    facility_cover = []

    for j in range(total_num):
        cover_demand = 0
        for k in range(total_num*j, total_num*(j+1)):
            if (data_dist[k] <= 25):
                cover_demand += data_demand[k%159]
        facility_cover.append(cover_demand)

    max_pos = facility_cover.index(max(facility_cover))
    facility_select.append(max_pos)
    cover_demand_final += max(facility_cover)

    for k in range(total_num*max_pos, total_num*(max_pos+1)):
        if (data_dist[k] <= 25):
            data_demand[k%159] = 0

facility_select = [x + 1 for x in facility_select]
print('Total Cover:', cover_demand_final)
print('Select:', facility_select)