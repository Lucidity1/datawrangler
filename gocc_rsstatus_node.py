# -*- coding: utf-8 -*-
import settings
import prettytable as pt
import operator
import datetime as dt

class RSStatus:
    def __init__(self, status_id, event_id,loc):
        self.status_id=status_id
        self.children=[]
        self.children.append(event_id)
        self.loc=loc
        
        self.min_time=None
        self.max_time=None        
        self.total_time=None
        self.toggling_no=None
        self.all_time=None
        
        self.tampered=False
        
    def add_child(self, event_id):
        self.children.append(event_id)
            
    
    def request(self, time):
        if self.all_time==None or time==None:
            return False
        for item in self.all_time:
            if item[0]<=time<=item[1]:
                return True
        return False
        
    def __str__(self):
        x=pt.PrettyTable(["RS no.", "time", "value"])
        for child in self.children:
            x.add_row([self.loc,settings.gocc[child]['sourcetime'],settings.gocc[child]['value']])
        return x.get_string(sortby="time")#+'\n'+str([self.all_time,self.tampered])



    def valid(self):
        for event_id in self.children:
            status=settings.gocc[event_id]['value']
            if (status=='MAINLINE SERVICE'):
                for event_id in self.children:
                    status=settings.gocc[event_id]['value']
                    if(status=='MAINLINE OFF SERV'):
                        return True
        return False

    def timeList(self):
        result=[]
        started=False
        for event_id in sorted(self.children):
            status=settings.gocc[event_id]['value']
            if (status=='MAINLINE SERVICE' and started==False):
                result.append([settings.gocc[event_id]['sourcetime'], 'ON'])
                started=True
            if (status=='MAINLINE OFF SERV' and started==True):
                result.append([settings.gocc[event_id]['sourcetime'], 'OFF'])
                started=False
        result=sorted(result, key=operator.itemgetter(0))
        
        try:
            if result[0][1]=='OFF':
                result=result[1:]
                self.tampered=True
            if result[-1][1]=='ON':
                result=result[:-1]
                self.tampered=True
        except:
            pass
            
        return result
    
    def totalTime(self, all_time):
        total=dt.timedelta(seconds=0)
        for item in all_time:
            total+=item[1]-item[0]
        self.total_time=total
        
    def initialize(self):   
        memory_O=None
        memory_N=None
        if self.valid():
            
            time_list=self.timeList()
            #print 'timelist: ',time_list
            all_time=[]
            #print time_list
            
            for sublist in time_list:                    
                if sublist[1]=='ON':
                    memory_O=sublist[0]
                    #print "memory_O assigned: ", memory_O
                if sublist[1]=='OFF':
                    memory_N=sublist[0]
                    #print "memory_N assigned: ", memory_N
                if memory_O != None and memory_N != None:
                    all_time.append([memory_O,memory_N])
                    #print 'Appending memory: ',[memory_O,memory_N]
                    memory_O=None
                    memory_N=None
            #print 'all_time: ',all_time
            try:
                self.min_time=min(sublist[0] for sublist in all_time)     
                self.max_time=max(sublist[1] for sublist in all_time)
                
                self.all_time=all_time
                self.toggling_no=len(all_time)
                self.totalTime(all_time)
            except:
                pass
            

    def to_string(self, date):
        x=pt.PrettyTable(["RS no.", "time", "value"])
        for child in self.children:
            if settings.gocc[child]['sourcetime'].date()==date:
                x.add_row([self.loc,settings.gocc[child]['sourcetime'],settings.gocc[child]['value']])
        return x.get_string(sortby="time")

