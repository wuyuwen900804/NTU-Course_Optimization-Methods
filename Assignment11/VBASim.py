# -*- coding: utf-8 -*-
"""
Created on Sat Oct 15 18:08:03 2016

@author: yl17
"""
'''
Modified by James Chu
Nov. 11. 2018
'''
import Basic_Classes

def VBASimInit(calendar,queues,ctstats,dtstats,resources,clock):

    while (calendar.N() > 0):
        EV = calendar.Remove()
            
    for Q in queues:
        Q.WIP.Clear(clock)        
        while Q.Len() > 0:
            En = Q.Remove(clock)
            
    for Re in resources:
        Re.Busy = 0

        Re.NumBusy.Clear(clock)
        
    for CT in ctstats:
        CT.Clear(clock)
        
    for DT in dtstats:
        DT.Clear()

def ScheduleEvent(calendar,EventType, EventTime, clock):
    addedEvent = Basic_Classes.EventNotice()
    addedEvent.EventType = EventType
    addedEvent.EventTime = clock + EventTime
    calendar.Schedule(addedEvent)

def getNextEvent(calendar):
    if len(calendar.ThisCalendar) > 0:
            remove = calendar.ThisCalendar.pop(0)
            return remove
        
def ClearStats(queues,ctstats,dtstats,resources, clock):
    for CT in ctstats:
        CT.Clear(clock)
    for Q in queues:
        Q.WIP.Clear(clock)
    for Re in resources:
        Re.NumBusy.Clear(clock)
    for DT in dtstats:
        DT.Clear()