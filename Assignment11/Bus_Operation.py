from VBASim import *
import RNG 
from Basic_Classes import *
import numpy as np
import matplotlib.pyplot as plt

ZRNG = RNG.InitializeRNSeed()
Calendar = EventCalendar()

TheQueues = []
DepotQueue = FIFOQueue()
RunningQueue = FIFOQueue()
RefuelQueue = FIFOQueue()
DelayQueue = FIFOQueue()
TheQueues.append(DepotQueue)
TheQueues.append(RunningQueue)
TheQueues.append(RefuelQueue)
TheQueues.append(DelayQueue)

TheResources = []
FuelDispenser = Resource()
FuelDispenser.SetUnits(1)
TheResources.append(FuelDispenser)

TheDTStats = []
DelayTime = DTStat()
DispatchedNum = DTStat()
TheDTStats.append(DelayTime)
TheDTStats.append(DispatchedNum)

TheCTStats = []

##########parameters###########
StartClock = 0.0
DispatchTotal = 12    # N
Headway = 60          # H
FleetSize = 3         # F
MeanRunTime = 35      # R
VarianceRunTime = 5   # V
MeanRefuel = 35       # G
###############################

def Dispatch():
    if DepotQueue.Len() == 0:
        DelayDispatch = Entity(Clock)
        DelayQueue.Add(DelayDispatch, Clock)
    else:
        DelayTime.Record(0)
        Bus = DepotQueue.Remove(Clock)
        RunningQueue.Add(Bus, Clock)
        ScheduleEvent(Calendar,"Return",RNG.Normal(MeanRunTime, VarianceRunTime, 1),Clock)
        DispatchedNum.Record(1)
        if DispatchedNum.Len() == DispatchTotal:
            ScheduleEvent(Calendar,"EndSimulation",0,Clock)
    ScheduleEvent(Calendar,"Dispatch",Headway,Clock)

def Return():
    Bus = RunningQueue.Remove(Clock)
    RefuelQueue.Add(Bus, Clock)
    if FuelDispenser.Busy == 0:
        FuelDispenser.Seize(1, Clock)
        ScheduleEvent(Calendar,"Refueled",RNG.Expon(MeanRefuel, 2),Clock)

def Refueled():
    Bus = RefuelQueue.Remove(Clock)
    if DelayQueue.Len() > 0:
        DelayDispatch = DelayQueue.Remove(Clock)
        DelayTime.Record(Clock-DelayDispatch.CreationTime)
        RunningQueue.Add(Bus, Clock)
        ScheduleEvent(Calendar,"Return",RNG.Normal(MeanRunTime, VarianceRunTime, 1),Clock)
        DispatchedNum.Record(1)
        if DispatchedNum.Len() == DispatchTotal:
            ScheduleEvent(Calendar,"EndSimulation",0,Clock)
    else:
        DepotQueue.Add(Bus, Clock)
    if RefuelQueue.Len() > 0:
        ScheduleEvent(Calendar,"Refueled",RNG.Expon(MeanRefuel, 2),Clock)
    else:
        FuelDispenser.Free(1, Clock)

runs = 1000
delay_record = []
for reps in range(runs):
    Clock = StartClock
    VBASimInit(Calendar,TheQueues,TheCTStats,TheDTStats,TheResources,Clock)
    ScheduleEvent(Calendar,"Dispatch",Headway,Clock)
    for i in range(FleetSize):
        Bus = Entity(Clock)
        DepotQueue.Add(Bus, Clock)
    while True:
        NextEvent = getNextEvent(Calendar)
        Clock = NextEvent.EventTime
        if NextEvent.EventType == "Dispatch":
            Dispatch()
        elif NextEvent.EventType == "Return":
            Return()
        elif NextEvent.EventType == "Refueled":
            Refueled()
        elif NextEvent.EventType == "EndSimulation":
            break
    delay_record.append(DelayTime.Mean())

Z = 1.96 # alpha = 0.05
delayMean, delayStd = round(np.mean(delay_record),2), round(np.std(delay_record, ddof = 1),2)
delayLB, delayUB = delayMean - Z*delayStd/(np.sqrt(runs)), delayMean + Z*delayStd/(np.sqrt(runs))
print(f"Runs: {runs}")
print(f"Mean of estimate delay time: {delayMean}")
print(f"Std  of estimate delay time: {delayStd}")
print(f"95% confidence interval: [{round(delayLB,2)}, {round(delayUB,2)}]")

# FleetSize range(1, 11)
# MeanRunTime range(30, 61)
# VarianceRunTime range(0, 46)
# MeanRefuel range(30, 61)
# X, Y = [i for i in range(30, 61)], []
# for G in X:
#     MeanRefuel = G
#     estimate_delay = []
#     for reps in range(1000):
#         Clock = StartClock
#         VBASimInit(Calendar,TheQueues,TheCTStats,TheDTStats,TheResources,Clock)
#         ScheduleEvent(Calendar,"Dispatch",Headway,Clock)
#         for i in range(FleetSize):
#             Bus = Entity(Clock)
#             DepotQueue.Add(Bus, Clock)
#         while True:
#             NextEvent = getNextEvent(Calendar)
#             Clock = NextEvent.EventTime
#             if NextEvent.EventType == "Dispatch":
#                 Dispatch()
#             elif NextEvent.EventType == "Return":
#                 Return()
#             elif NextEvent.EventType == "Refueled":
#                 Refueled()
#             elif NextEvent.EventType == "EndSimulation":
#                 break
#         estimate_delay.append(DelayTime.Mean())
#     Y.append(round(np.mean(estimate_delay),2))

# plt.plot(X, Y)
# plt.xlabel('Mean Refuel Time')
# plt.ylabel('Mean Delay Time')
# plt.title('Mean Refuel Time & Mean Delay Time')
# plt.show()