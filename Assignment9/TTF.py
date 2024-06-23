from VBASim import *
import RNG 
from Basic_Classes import *

import random

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

for reps in range(500):
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

    print(f"TTF: {Clock}, AVG Functional Components: {ResourcesNum-UnderRepair.Mean(Clock):.2f}")