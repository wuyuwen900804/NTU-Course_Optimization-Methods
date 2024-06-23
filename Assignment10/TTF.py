from VBASim import *
import RNG 
from Basic_Classes import *

import random
import numpy as np
random.seed(0)

ZRNG = RNG.InitializeRNSeed()
Calendar = EventCalendar()

TheQueues = []

ResourcesNum = 2
TheResources = []
UnderRepair = Resource()
UnderRepair.SetUnits(ResourcesNum)
TheResources.append(UnderRepair)

TheDTStats = []

TheCTStats = []

##########parameters###########
StartClock = 0.0
###############################

def Failure():
    UnderRepair.Seize(1, Clock)
    if UnderRepair.Busy <= 1:
        ScheduleEvent(Calendar,"Failure",random.randint(1,6),Clock)
    ScheduleEvent(Calendar,"RepairCompletion",2.5,Clock)
    pass
 
def RepairCompletion():
    UnderRepair.Free(1, Clock)
    pass

runs = 5000
TTF, Functional = [], []
for reps in range(runs):
    Clock = StartClock
    VBASimInit(Calendar,TheQueues,TheCTStats,TheDTStats,TheResources,Clock)

    ScheduleEvent(Calendar,"Failure", random.randint(1,6), Clock)

    while UnderRepair.Busy!=ResourcesNum:
        NextEvent = getNextEvent(Calendar)
        Clock = NextEvent.EventTime
        if NextEvent.EventType == "Failure":
            Failure()
        elif NextEvent.EventType == "RepairCompletion":
            RepairCompletion()
    
    TTF.append(Clock)
    Functional.append(round(ResourcesNum-UnderRepair.Mean(Clock),2))
    # print(f"TTF: {Clock}, AVG Functional Components: {ResourcesNum-UnderRepair.Mean(Clock):.2f}")s

Z = 1.96 # alpha = 0.05
print(f"Num of repetitions = {runs}, alpha = 0.05")
print("------------------------------------------------")
TTFMean, TTFStd = round(np.mean(TTF),2), round(np.std(TTF, ddof = 1),2)
print(f"Mean of estimate TTF: {TTFMean}")
print(f"Std  of estimate TTF: {TTFStd}")
TTFLB, TTFUB = TTFMean - Z*TTFStd/(np.sqrt(runs)), TTFMean + Z*TTFStd/(np.sqrt(runs))
print(f"95% confidence interval: [{round(TTFLB,2)}, {round(TTFUB,2)}]")
print("------------------------------------------------")
AFCMean, AFCStd = round(np.mean(Functional),2), round(np.std(Functional, ddof = 1),2)
print(f"Mean of estimate AVG Functional Components: {AFCMean}")
print(f"Std of estimate AVG Functional Components : {AFCStd}")
AFCLB, AFCUB = AFCMean - Z*AFCStd/(np.sqrt(runs)), AFCMean + Z*AFCStd/(np.sqrt(runs))
print(f"95% confidence interval: [{round(AFCLB,2)}, {round(AFCUB,2)}]")