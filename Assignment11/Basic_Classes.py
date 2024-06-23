# -*- coding: utf-8 -*-
"""
Created on Thu Oct 13 21:41:39 2016

@author: yl17
"""
'''
Modified by James Chu
Nov. 11 2018
Apr. 17 2019
Apr. 30 2020 
Mar. 30 2022 (Python 3) 
'''
import math

class Entity():
    def __init__(self,clock):
        self.CreationTime = clock
        #more attributes can be added.

class CTStat():
    def __init__(self):
        self.Area = 0.0
        self.Tlast = 0.0
        self.TClear = 0.0
        self.Xlast = 0.0
        
    def Record(self,X,clock):
        self.Area = self.Area + self.Xlast * (clock - self.Tlast)
        self.Tlast = clock
        self.Xlast = X

    def Mean(self,clock):
        mean = 0.0
        if (clock - self.TClear) > 0.0:
           mean = (self.Area + self.Xlast * (clock - self.Tlast)) / (clock - self.TClear)
        return mean
    
    #this is used at the beginning of each simulation repetition
    def Clear(self,clock):
        self.Area = 0.0
        self.Tlast = clock
        self.TClear = clock
        self.Xlast = 0.0  #jameschu, 20200430

    #jameschu, 20200430
    #this is used within a simulation repetition
    def ClearWarmUp(self,clock):
        self.Area = 0.0
        self.Tlast = clock
        self.TClear = clock
        #self.Xlast is unchanged.

class DTStat():
    def __init__(self):
        self.Sum = 0.0
        self.SumSquared = 0.0
        self.NumberOfObservations = 0.0
        self.History=[]
    
    def Record(self,X):
        self.Sum = self.Sum + X
        self.SumSquared = self.SumSquared + X * X
        self.NumberOfObservations = self.NumberOfObservations + 1
        self.History.append(X)
        
    def Mean(self):
        mean = 0.0
        if self.NumberOfObservations > 0.0:
            mean = self.Sum / self.NumberOfObservations
        return mean

    def StdDev(self):
        stddev = 0.0
        if self.NumberOfObservations > 0.0:
            stddev = math.sqrt((self.SumSquared - self.Sum**2 / self.NumberOfObservations) / (self.NumberOfObservations - 1))
        return stddev
            
    def Len(self):
        return self.NumberOfObservations
    
    def Clear(self):
        self.Sum = 0.0
        self.SumSquared = 0.0
        self.NumberOfObservations = 0.0
        self.History=[]
        
        
class Resource():
    def __init__(self):
        self.Busy = 0
        self.NumberOfUnits = 0
        self.NumBusy = CTStat()
        
    def Seize(self, Units, clock):
        diff = self.NumberOfUnits - Units - self.Busy
        if diff >= 0:
            self.Busy = self.Busy + Units
            self.NumBusy.Record(float(self.Busy),clock)
            seize = True
        else:
            seize = False
        return seize
        
    def Free(self, Units, clock):
        diff = self.Busy - Units
        if diff < 0:
            free = False
        else:
            self.Busy = self.Busy - Units
            self.NumBusy.Record(float(self.Busy), clock)
            free = True
        return free
    
    def Mean(self,clock):
        return self.NumBusy.Mean(clock)
        
    def SetUnits(self, Units):
        self.NumberOfUnits = Units
        
        
class FIFOQueue():
    def __init__(self):
        self.WIP = CTStat()
        self.ThisQueue = []
        
    def Len(self):
        return len(self.ThisQueue)
        
    def Add(self,X,clock):
        self.ThisQueue.append(X)
        numqueue = self.Len()
        self.WIP.Record(float(numqueue),clock)    
    
    def Remove(self,clock):
        if len(self.ThisQueue) > 0:
            remove = self.ThisQueue[0]
            self.ThisQueue.remove(self.ThisQueue[0])
            self.WIP.Record(float(self.Len()),clock)   
            return remove
        
    def Mean(self,clock):
        return self.WIP.Mean(clock)
               

class PriorityQueue():
    def __init__(self):
        self.WIP = CTStat()
        self.ThisQueue = []
        
    def Len(self):
        return len(self.ThisQueue)
        
    def Add(self,X,clock):
        if len(self.ThisQueue) == 0:
            self.ThisQueue.append(X)
        else:
            if self.ThisQueue[-1].Priority >= X.Priority:
                self.ThisQueue.append(X)
            else:
                for rep in range(len(self.ThisQueue)):
                    if self.ThisQueue[rep].Priority < X.Priority:
                        break
                self.ThisQueue.insert(rep,X)
        numqueue = self.Len()
        self.WIP.Record(float(numqueue),clock)    
    
    def Remove(self,clock):
        if len(self.ThisQueue) > 0:
            remove = self.ThisQueue[0]
            self.ThisQueue.remove(self.ThisQueue[0])
            numqueue = self.Len()
            self.WIP.Record(float(numqueue),clock) 
            return remove      
        
    def Mean(self,clock):
        return self.WIP.Mean(clock)  
        
       
class EventNotice():
    EventTime = 0.0
    EventType = ""
    WhichObject = ()
        
        
class EventCalendar():
    def __init__(self):
        self.ThisCalendar = []
    
    def Schedule(self,addedEvent=EventNotice()):
        if len(self.ThisCalendar) == 0:
            self.ThisCalendar.append(addedEvent)
        elif self.ThisCalendar[-1].EventTime <= addedEvent.EventTime:
            self.ThisCalendar.append(addedEvent)
        else:
            for rep in range(0,len(self.ThisCalendar),1):
                if self.ThisCalendar[rep].EventTime > addedEvent.EventTime:
                    break
            self.ThisCalendar.insert(rep,addedEvent)
    
    def Remove(self):
        if len(self.ThisCalendar) > 0:
            remove = self.ThisCalendar[0]
            self.ThisCalendar.remove(self.ThisCalendar[0])
            return remove
        
    def N(self):
        return len(self.ThisCalendar)
        
    def test(self):
        print(self.ThisCalendar[-1].EventTime)
        

    
      