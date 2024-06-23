from VBASim import *
import RNG 
from Basic_Classes import *

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
print(f"{'Rep':5}", f"{'Avg Queue Num':20}", f"{'Avg Server Num':20}", f"{'Avg System Num':20}",
      f"{'Avg Queue Time':20}", f"{'Avg Server Time':20}", f"{'Avg System Time':20}", f"{'Busy Proportion':20}")

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

for reps in range(5):
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
    print(f"{reps+1:<5}",
          f"{QueueInLine.Mean(Clock):<20.15f}", f"{QueueOnServer.Mean(Clock):<20.15f}", f"{QueueInSystem.Mean(Clock):<20.15f}",
          f"{CustLineTime.Mean():<20.15f}", f"{CustServerTime.Mean():<20.15f}", f"{CustSystemTime.Mean():<20.15f}",
          f"{Server.Mean(Clock):<.15f}")