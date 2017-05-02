# -*- coding: utf-8 -*-
import settings
import datetime as dt
import prettytable as pt
import operator

class Alarm:
    def __init__(self, alarm_id, event_id, equipment,system,subsystem,severity,description):
        self.alarm_id=alarm_id
        self.children=[]
        self.children.append(event_id)
        self.equipment=equipment
        self.system=system
        self.subsystem=subsystem
        self.severity=severity
        self.description=description
        
        self.loc=None
        self.min_time=None
        self.max_time=None
        self.total_time=None
        self.toggling_no=None
       
    def add_child(self, event_id):
        self.children.append(event_id)

    def valid(self):
        for event_id in self.children:
            status=settings.gocc[event_id]['eventtype']
            if (status=='ALARM_OPENED'):
                for event_id in self.children:
                    status=settings.gocc[event_id]['eventtype']
                    if(status=='ALARM_NORMALIZED'):
                        return True
        return False

    def truncate(self):
        eqm=self.equipment
        place=eqm.index('/')
        eqm=eqm[:place]
        return eqm
    
    def timeList(self):
        result=[]
        for event_id in self.children:
            status=settings.gocc[event_id]['eventtype']
            if (status=='ALARM_OPENED'):
                result.append([settings.gocc[event_id]['sourcetime'], 'O'])
            if (status=='ALARM_NORMALIZED'):
                result.append([settings.gocc[event_id]['sourcetime'], 'N'])
        result=sorted(result, key=operator.itemgetter(0))
        if result[0][1]=='N':
            result=result[1:]
        return result
    
    def totalTime(self, all_time):
        total=dt.timedelta(seconds=0)
        for item in all_time:
            total+=item[1]-item[0]
        self.total_time=total
        
    def initialize(self):  
        self.loc=self.truncate()
        memory_O=None
        memory_N=None
        if self.valid():
            
            time_list=self.timeList()
            #print 'timelist: ',time_list
            all_time=[]
            #print time_list
            
            for sublist in time_list:                    
                if sublist[1]=='O':
                    memory_O=sublist[0]
                    #print "memory_O assigned: ", memory_O
                if sublist[1]=='N':
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
                
                self.toggling_no=len(all_time)
                self.totalTime(all_time)
            except:
                pass

    def __str__(self):
        x=pt.PrettyTable(['Var', 'Value'])
        x.add_row(['Alarm ID', self.alarm_id])
        x.add_row(['Event count', len(self.children)])
        x.add_row(['Equipment', self.equipment])
        x.add_row(['Severity', self.severity])
        x.add_row(['Description', self.description])      
        x.add_row(['min_time', self.min_time])
        x.add_row(['max_time', self.max_time])
        x.add_row(['total_time', self.total_time])
        x.add_row(['toggling_no', self.toggling_no])
        return x.get_string()+"\n"
    
    def to_string(self):
        return self.__str__()
        
        