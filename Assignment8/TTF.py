from VBASim import *
import RNG 
from Basic_Classes import *

import random

ZRNG = RNG.InitializeRNSeed()
Calendar = EventCalendar()

TheQueues = []

TheResources = []

TheDTStats = []

TheCTStats = []

##########parameters###########
StartClock = 0.0
###############################

def Failure():
    global num_functional_components
    num_functional_components -= 1
    if num_functional_components >= 1:
        ScheduleEvent(Calendar,"Failure",random.randint(1,6),Clock)
    ScheduleEvent(Calendar,"RepairCompletion",2.5,Clock)
    pass
 
def RepairCompletion():
    global num_functional_components
    num_functional_components += 1
    pass

for reps in range(1):
    Clock = StartClock
    VBASimInit(Calendar,TheQueues,TheCTStats,TheDTStats,TheResources,Clock)

    num_functional_components=2
    ScheduleEvent(Calendar,"Failure",random.randint(1,6),Clock)

    while num_functional_components!=0:
        NextEvent = getNextEvent(Calendar)
        Clock = NextEvent.EventTime
        if NextEvent.EventType == "Failure":
            Failure()
        elif NextEvent.EventType == "RepairCompletion":
            RepairCompletion()
    
    print("TTF",Clock)