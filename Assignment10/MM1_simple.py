from VBASim import *
import RNG 
from Basic_Classes import *
import numpy as np

ZRNG = RNG.InitializeRNSeed()
Calendar = EventCalendar()

TheQueues = []
QueueInLine = FIFOQueue()
QueueOnServer = FIFOQueue()
QueueInSystem = FIFOQueue()
TheQueues.append(QueueInLine)
TheQueues.append(QueueOnServer)
TheQueues.append(QueueInSystem)

TheResources = []
Server = Resource()
Server.SetUnits(1)
TheResources.append(Server)

TheDTStats = []
CustLineTime = DTStat()
CustServerTime = DTStat()
CustSystemTime = DTStat()
TheDTStats.append(CustLineTime)
TheDTStats.append(CustServerTime)
TheDTStats.append(CustSystemTime)

TheCTStats = []

##########parameters###########
StartClock = 0.0
MeanInterarrival = 6
MeanService = 4
RunLength = 55000.0
###############################

# print("Rep\tQueue Time\tAvg Queue Len\tServer Util\tFinal Queue Len")
# print(f"{'Rep':5}", f"{'Avg Queue Num':20}", f"{'Avg Server Num':20}", f"{'Avg System Num':20}",
#       f"{'Avg Queue Time':20}", f"{'Avg Server Time':20}", f"{'Avg System Time':20}", f"{'Busy Proportion':20}")

def Arrival():
    ScheduleEvent(Calendar,"Arrival",RNG.Expon(MeanInterarrival, 1),Clock)

    CustomerInSystem = Entity(Clock)
    CustomerInSystem.ArrivalTime = Clock
    QueueInSystem.Add(CustomerInSystem, Clock)

    CustomerInLine = Entity(Clock)
    CustomerInLine.ArrivalTime = Clock
    
    if Server.Busy == 1:
        QueueInLine.Add(CustomerInLine, Clock)
    elif Server.Busy == 0:
        CustomerOnServer = Entity(Clock)
        CustomerOnServer.ArrivalTime = Clock
        QueueOnServer.Add(CustomerOnServer, Clock)

        Server.Seize(1, Clock)
        CustLineTime.Record(0)  #no waiting
        ScheduleEvent(Calendar,"Departure",RNG.Expon(MeanService, 2),Clock)
        
def Departure():
    CustomerOnServer = QueueOnServer.Remove(Clock)
    CustServerTime.Record(Clock-CustomerOnServer.ArrivalTime)

    if QueueInLine.Len() == 0:
        Server.Free(1, Clock)
    else:
        Customer = QueueInLine.Remove(Clock)
        CustLineTime.Record(Clock-Customer.ArrivalTime)  #the waiting time of the first customer in line
        ScheduleEvent(Calendar,"Departure",RNG.Expon(MeanService, 2),Clock)

        CustomerOnServer = Entity(Clock)
        CustomerOnServer.ArrivalTime = Clock
        QueueOnServer.Add(CustomerOnServer, Clock)
    
    CustomerInSystem = QueueInSystem.Remove(Clock)
    CustSystemTime.Record(Clock-CustomerInSystem.ArrivalTime)

total_runs = 100
AvgSystemNum, AvgSystemTime, AvgQueueNum, AvgQueueTime = [], [], [], []
for reps in range(total_runs):
    Clock = StartClock
    VBASimInit(Calendar,TheQueues,TheCTStats,TheDTStats,TheResources,Clock)
    ScheduleEvent(Calendar,"Arrival",RNG.Expon(MeanInterarrival, 1),Clock)
    ScheduleEvent(Calendar,"EndSimulation",RunLength,Clock)

    while True:
        NextEvent = getNextEvent(Calendar)
        Clock = NextEvent.EventTime
        if NextEvent.EventType == "Arrival":
            Arrival()
        elif NextEvent.EventType == "Departure":
            Departure()
        elif NextEvent.EventType == "EndSimulation":
            break
    
    # print(reps+1,'\t', CustLineTime.Mean(),'\t',LineQueue.Mean(Clock),'\t',Server.Mean(Clock),'\t',LineQueue.Len())
    # print(f"{reps+1:<5}",
    #       f"{QueueInLine.Mean(Clock):<20.15f}", f"{QueueOnServer.Mean(Clock):<20.15f}", f"{QueueInSystem.Mean(Clock):<20.15f}",
    #       f"{CustLineTime.Mean():<20.15f}", f"{CustServerTime.Mean():<20.15f}", f"{CustSystemTime.Mean():<20.15f}",
    #       f"{Server.Mean(Clock):<.15f}")

    AvgSystemNum.append(round(QueueInSystem.Mean(Clock), 2))
    AvgSystemTime.append(round(CustSystemTime.Mean(), 2))
    AvgQueueNum.append(round(QueueInLine.Mean(Clock), 2))
    AvgQueueTime.append(round(CustLineTime.Mean(), 2))

Lambda, Mu = 1/MeanInterarrival, 1/MeanService
P = Lambda / Mu

Z = 1.96
ASNMean, ASNStd = np.mean(AvgSystemNum) , np.std(AvgSystemNum , ddof = 1)
ASNLB, ASNUB = ASNMean - Z*ASNStd/(np.sqrt(total_runs)), ASNMean + Z*ASNStd/(np.sqrt(total_runs))
ASTMean, ASTStd = np.mean(AvgSystemTime), np.std(AvgSystemTime, ddof = 1)
ASTLB, ASTUB = ASTMean - Z*ASTStd/(np.sqrt(total_runs)), ASTMean + Z*ASTStd/(np.sqrt(total_runs))
AQNMean, AQNStd = np.mean(AvgQueueNum)  , np.std(AvgQueueNum  , ddof = 1)
AQNLB, AQNUB = AQNMean - Z*AQNStd/(np.sqrt(total_runs)), AQNMean + Z*AQNStd/(np.sqrt(total_runs))
AQTMean, AQTStd = np.mean(AvgQueueTime) , np.std(AvgQueueTime , ddof = 1)
AQTLB, AQTUB = AQTMean - Z*AQTStd/(np.sqrt(total_runs)), AQTMean + Z*AQTStd/(np.sqrt(total_runs))

print("----------------------------------------------------------")
print(f"MeanInterarrival = {MeanInterarrival}, MeanService = {MeanService}")
print("----------------------------------------------------------")
print("(Theory Results)")
print(f"Avg System Num  : {P/(1-P):>5.2f}")
print(f"Avg System Time : {1/(Mu-Lambda):>5.2f}")
print(f"Avg Queue Num   : {(P**2)/(1-P):>5.2f}")
print(f"Avg Queue Time  : {P/(Mu-Lambda):>5.2f}")
print("----------------------------------------------------------")
print(f"Num of repetitions = {total_runs}, alpha = 0.05")
print("----------------------------------------------------------")
print("(Simulation Results)")
print(f"Avg System Num  : mean {ASNMean:>5.2f}",
      f"| std {ASNStd:>4.2f}",
      f"| 95% confidence interval [{round(ASNLB, 2):>5.2f}, {round(ASNUB, 2):>5.2f}]")
print(f"Avg System Time : mean {ASTMean:>5.2f}",
      f"| std {ASTStd:>4.2f}",
      f"| 95% confidence interval [{round(ASTLB, 2):>5.2f}, {round(ASTUB, 2):>5.2f}]")
print(f"Avg Queue Num   : mean {AQNMean:>5.2f}",
      f"| std {AQNStd:>4.2f}",
      f"| 95% confidence interval [{round(AQNLB, 2):>5.2f}, {round(AQNUB, 2):>5.2f}]")
print(f"Avg Queue Time  : mean {AQTMean:>5.2f}",
      f"| std {AQTStd:>4.2f}",
      f"| 95% confidence interval [{round(AQTLB, 2):>5.2f}, {round(AQTUB, 2):>5.2f}]")