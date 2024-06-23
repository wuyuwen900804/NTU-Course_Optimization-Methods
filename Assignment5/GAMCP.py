from pyevolve import G1DBinaryString
from pyevolve import GSimpleGA
from pyevolve import Selectors
from pyevolve import Mutators

# To run on Python 3.11
import collections
collections.Callable = collections.abc.Callable

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

def eval_func(chromosome):
    score = 0.0
    iter = 0
    facility_num = 0
    selected_facility = []
    for value in chromosome:
        if (value == 0 and facility_num < 15):
            score += 500000
        elif (value == 1):
            facility_num += 1
            selected_facility.append(iter)
        iter += 1
    score += SumCover(selected_facility)
    return score

def run_main():
    genome = G1DBinaryString.G1DBinaryString(159)
    genome.evaluator.set(eval_func)
    genome.mutator.set(Mutators.G1DBinaryStringMutatorFlip)

    ga = GSimpleGA.GSimpleGA(genome, 2024)
    ga.selector.set(Selectors.GTournamentSelector)
    ga.setGenerations(375)
    ga.evolve(freq_stats=100)

    selected = []
    ga_iter = 0
    ga_list = ga.bestIndividual().getInternalList()
    for i in ga_list:
        if (i==1):
            selected.append(ga_iter)
        ga_iter += 1
    print('Cover Demand:', SumCover(selected))
    print('Select:', selected)

if __name__ == "__main__":
    run_main()