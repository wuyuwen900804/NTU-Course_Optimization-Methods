import numpy as np
from edge_list import *
from pyevolve import G1DList
from pyevolve import Mutators, Crossovers
from pyevolve import Consts, GSimpleGA
from pyevolve import DBAdapters
from random import shuffle

# To run on Python 3.11
import collections
collections.Callable = collections.abc.Callable

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

CITY_NUM = 42

def tour_eval(genome):
    ga_list = genome.genomeList.copy()
    ga_list.append(ga_list[0])
    return SumDistance(ga_list)

def tour_init(genome, **kwargs):
    genome.genomeList = list(range(0, CITY_NUM))
    shuffle(genome.genomeList)

def run_main():
    genome = G1DList.G1DList(CITY_NUM)
    genome.setParams(bestrawscore=CITY_NUM, rounddecimal=2)
    genome.initializator.set(tour_init)
    genome.mutator.set(Mutators.G1DListMutatorSwap)
    genome.crossover.set(Crossovers.G1DListCrossoverCutCrossfill)
    genome.evaluator.set(tour_eval)

    ga = GSimpleGA.GSimpleGA(genome, 2024)
    ga.terminationCriteria.set(GSimpleGA.RawScoreCriteria)
    ga.setMinimax(Consts.minimaxType["minimize"])

    ga.setPopulationSize(100)
    ga.setGenerations(500)
    ga.setMutationRate(0.02)
    ga.setCrossoverRate(1.0)
    ga.evolve(freq_stats=100)

    best = ga.bestIndividual()
    print('Total Distance:', best.getRawScore())
    print('Tour:', best.genomeList+[best.genomeList[0]])

if __name__ == "__main__":
    run_main()