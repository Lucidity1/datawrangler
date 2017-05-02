# -*- coding: utf-8 -*-
import settings
import gocc_alarm_node
import gocc_rsstatus_node
import gocc_dwell_node
import print_progress as pp 
from collections import defaultdict
import gocc_skip_node
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def identify():
    total=len(settings.gocc)
    stabalizer=int(total/100)
    alarm_index=[]
    readiness_index=[]
    schedule_index=[]
    skip_index=[]
    count=0
    for key, value in settings.gocc.iteritems():
        if 'ALARM' in value['eventtype']:
            alarm_index.append(key)
        if 'DIAG_IRdyStTranSucc[1]' in value['eventtype']:
            readiness_index.append(key)
        if (('ALARM_OPENED' in value['eventtype'] or 'ALARM_NORMALIZED' in value['eventtype']) and value['description']=='Door Interlock Loop' or ('DIAG_ITailLight[1..2]'in value['eventtype'] and value['description']=='Tail Lights') or 'DIAG_IRdyStTranSucc[1]' in value['eventtype']):
            schedule_index.append(key)
        if 'DIAG_ISkipStOdrRecAto' in value['eventtype']:
            skip_index.append(key)
        count+=1
        if(count%stabalizer==0 or count/total>0.98):
            pp.printProgress(count,total, prefix='Identifying:', suffix='Complete', barLength=10)
    return alarm_index, readiness_index,schedule_index, skip_index

def create(alarm_index):
    total=len(alarm_index)
    stabalizer=int(total/150)
    count=0

    for index in alarm_index:
        tracker=locAlarm(index)

        if tracker != False:   
            tracker.add_child(index)
        else:
            alarm_id=settings.gocc[index]['alarm']
            system=settings.gocc[index]['system']
            subsystem=settings.gocc[index]['subsystem']
            node=gocc_alarm_node.Alarm(alarm_id,index, settings.gocc[index]['equipment'], system, subsystem, settings.gocc[index]['severity'], settings.gocc[index]['description'])
            settings.alarm[alarm_id]=node
        count+=1
        if(count%stabalizer==0 or count/total>0.98):
            pp.printProgress(count,total, prefix='Sorting alarms:', suffix='Complete', barLength=10)

def create_rsstatus(readiness_index):
    total=len(readiness_index)
    stabalizer=int(total/30)
    count=0
    
    for index in readiness_index:
        tracker=locRSState(index)

        if tracker != False:   
            tracker.add_child(index)
        else:
            date=settings.gocc[index]['sourcetime'].date()
            loc=settings.gocc[index]['location']
            status_id=loc
            node=gocc_rsstatus_node.RSStatus(status_id,index,loc)
            settings.rsstatus[status_id]=node
        count+=1
        
        if(count%stabalizer==0 or count/total>0.98):
            pp.printProgress(count,total, prefix='Sorting RSState:', suffix='Complete', barLength=10)

def truncate(string):
    place=string.index('/')
    return string[:place]
        
def create_schedule(schedule_index):
    holder=defaultdict(lambda:None)
    for index in schedule_index:
        loc=truncate(settings.gocc[index]['equipment'])[:-1]
        day=settings.gocc[index]['sourcetime'].date()
        
        
        while(True):
            if holder[loc]!=None:
                if holder[loc][day]!=None:
                    holder[loc][day].append(index)
                    break
                else:
                    holder[loc][day]=[]
            else: 
                holder[loc]=defaultdict(lambda:None)
    
        holder[loc][day]=sorted(holder[loc][day])
    iterate(holder)
    
    #re-tidy
    iterateFirst(settings.rsschedule)
        
    print 'Train schedule sorted.'
    #printAll()

def iterateFirst(holder):
    for k,v in holder.iteritems():
        if isinstance(v,dict):
            iterateFirst(v)
        else:
            if len(v[0])<=18:
                if v[0][0].direction=="XB":
                    count=18
                    for dwell in reversed(v[0]):                    
                        dwell.station=count
                        count-=1
                if v[0][0].direction=="BB":
                    count=len(v[0])  
                    for dwell in v[0]:                    
                        dwell.station=count
                        count-=1



def iterate(holder):
    service=defaultdict(lambda:'OFF')
    for k, v in holder.iteritems():
        if isinstance(v, dict):
            iterate(v)
        else:                           
            changeDir=False
            line=[]
            previous_station=None
            station=None
            direction=None
            for key, index in enumerate(v):
                #print index
                loc=truncate(settings.gocc[index]['equipment'])[:-1]
                day=settings.gocc[index]['sourcetime'].date()
                light=truncate(settings.gocc[index]['equipment'])[-1:]
                
                if settings.gocc[index]['value']=='MAINLINE SERVICE':
                    service[loc]='ON'
                    #print 'Train ',loc,' assigned ON'
                if settings.gocc[index]['value']=='MAINLINE OFF SERV':
                    service[loc]='OFF'
                    #print 'Train ',loc,' assigned OFF'
                    
                    if  line!=[]:
                    #save old line
                        #print 'attempting to save line ',line
                        while(True):
                            if settings.rsschedule[loc]!=None:
                                if settings.rsschedule[loc][day]!=None:
                                    settings.rsschedule[loc][day].append(line)
                                    #print 'appending line ',line
                                    break
                                else:
                                    settings.rsschedule[loc][day]=[]
                            else: 
                                settings.rsschedule[loc]=defaultdict(lambda:None)                

                    changeDir=False
                    line=[]
                    previous_station=None
                    station=None
                    direction=None    

                if settings.gocc[index]['value']=='ON' and light=='1':
                    direction='XB'
                    changeDir=True
                    if previous_station==None:
                        previous_station=0
                    else:
                        previous_station= station
                if settings.gocc[index]['value']=='ON' and light=='3':
                    direction='BB'
                    changeDir=True
                    if previous_station==None or previous_station==0:
                        previous_station=19
                    else:
                        previous_station= station
                
                if service[loc]=='ON':
       
                    if (changeDir==True):
                        if  line!=[]:
                        #save old line
                            #print 'attempting to save line ',line
                            while(True):
                                if settings.rsschedule[loc]!=None:
                                    if settings.rsschedule[loc][day]!=None:
                                        settings.rsschedule[loc][day].append(line)
                                        if len(line)<=17:
                                            if direction=='XB':
                                                previous_station=1
                                            if direction=='BB':
                                                previous_station=18
                                        #print 'appending line ',line
                                        break
                                    else:
                                        settings.rsschedule[loc][day]=[]
                                else: 
                                    settings.rsschedule[loc]=defaultdict(lambda:None)                
                        #create newline
                        line=[]
                        changeDir=False
                    else:
                        if settings.gocc[index]['value']=='OPEN' and direction!=None:
                            #determine dwell station
                            try:
                                if direction=='XB':
                                    station=previous_station+1
                                if direction=='BB':
                                    station=previous_station-1
                                previous_station=station
                            except:
                                pass
                                
                            #determine dwell time_start
                            time_start=settings.gocc[index]['sourcetime']
                            #determine dwell time_end
                            time_end=returnClosed(v,key)
                        
                            #create dwell
                            dwell=gocc_dwell_node.Dwell(loc, direction, station,time_start,time_end)
                            dwell.calDwellTime()
                            #safe dwell into existing line
                            line.append(dwell)                  

def returnClosed(v, key):
    for i in range(key, len(v)):
        if settings.gocc[v[i]]['value']=='CLOSED':
            return settings.gocc[v[i]]['sourcetime']
 
def exist(search):
    if any(search==alarm.alarm_id for alarm in settings.alarm):
        return True
    else:
        return False
        
def locRSState(index):
    loc=settings.gocc[index]['location']
    rsstate_key=loc
    
    if rsstate_key not in settings.rsstatus:
        return False
    
    return settings.rsstatus[rsstate_key] 

def locAlarm(index):
    #normal search
    alarm_key=settings.gocc[index]['alarm']
    
    if alarm_key not in settings.alarm:
        return False
    
    return settings.alarm[alarm_key]   
    
    
def initialize_rsstatus():
    total=len(settings.rsstatus)  
    stabalizer=int(total/30)
    count=0
    for k,v in settings.rsstatus.iteritems():
        v.initialize()
        count+=1
        if(count%stabalizer==0 or count/total>0.98):
            pp.printProgress(count,total, prefix='Initializing alarms:', suffix='Complete', barLength=10)

    
def initialize_alarms():
    total=len(settings.alarm)  
    stabalizer=int(total/30)
    count=0
    for k,v in settings.alarm.iteritems():
        v.initialize()
        count+=1
        if(count%stabalizer==0 or count/total>0.98):
            pp.printProgress(count,total, prefix='Initializing alarms:', suffix='Complete', barLength=10)

def identifySkip(skip_index):
    holder=[]
    for index in skip_index:
        loc=truncate(settings.gocc[index]['equipment'])[:-1]
        sourcetime=settings.gocc[index]['sourcetime']
        try:
            rack=settings.rsschedule[loc][sourcetime.date()]
            for row_index, row in enumerate(rack):
                if sourcetime>=row[0].time_start and sourcetime<=row[-1].time_start:
                    settings.skip[loc]=gocc_skip_node.Skip(loc,sourcetime,row_index)
                    break
        except:
            pass
    print "Station skipping sorted."
    return holder

def simpleSort(alarm_index):
    compiled_list={}
    for key in alarm_index:
        day=settings.gocc[key]['sourcetime'].date()
        loc=settings.gocc[key]['equipment']

        if day in compiled_list:
            if loc in compiled_list[day]:
                compiled_list[day][loc]+=1
            else:
                compiled_list[day][loc]=1
        else:
            compiled_list[day]={}
    
    coords_y1=[]
    coords_y2=[]
    coords_x=[]
    
    for k, v in compiled_list.iteritems():
        total=0
        asset_no=len(v)
        for key, value in v.iteritems():
            total+=value
        coords_x.append(k)
        coords_y1.append(asset_no)
        coords_y2.append(total)

    print coords_x
    print coords_y1
    print coords_y2
    fig=plt.figure(1, figsize=(20,10))
    ax=fig.add_subplot(111)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))       
    ax.set_xlim(xmin=dt.datetime(2016,9,1), xmax=dt.datetime(2016,9,30))     
    ax.set_xticks(coords_x)
    ax.plot_date(coords_x, coords_y2, marker='o',markersize=10, linewidth=1.0, color=settings.color_code[0])
    ax.plot_date(coords_x, coords_y1, marker='o',markersize=10, linewidth=1.0, color=settings.color_code[1])
    plt.rcParams.update({'font.size': 10})
    fig.autofmt_xdate(rotation=45)
    fig.tight_layout()
    
    for i,j in zip(coords_x,coords_y1):
        ax.annotate(str(j),xy=(i,j+700))
    for i,j in zip(coords_x,coords_y2):
        ax.annotate(str(j),xy=(i,j+700))

    plt.savefig('output/plot/Aug.png')
    print 'output/plot/Aug.png'+' generated'
    plt.close()
    
def togSort(alarm_index):
    print len(alarm_index)
    compiled_list={}
    for key in alarm_index:
        day=settings.gocc[key]['sourcetime'].date()
        loc=truncate(settings.gocc[key]['equipment'])
        if '90' in loc:
            loc=loc[:-1]
        
        if day in compiled_list:
            if loc in compiled_list[day]:
                compiled_list[day][loc]+=1
            else:
                compiled_list[day][loc]=1
        else:
            compiled_list[day]={}
    

    coords_x=[]
    coords_y=[]
    for k, v in compiled_list.iteritems():
        #print k
        #print v
        total_asset=len(v)
        total_entries=0
        for key, value in v.iteritems():
            total_entries+=value
        coords_x.append(total_asset)
        coords_y.append(total_entries)
    
    print coords_x
    print coords_y
    fig=plt.figure(figsize=(15,10))
    sub1=fig.add_subplot(111)
    sub1.scatter(coords_x, coords_y,c='r', marker='o', s=80)
    
    compiled_list2={}
    for k,v in settings.alarm.iteritems():
        if v.min_time==None:
            ##print 'None detected in time. Alarm_id: ',v.alarm_id
            pass
        else:
            day=v.min_time.date()
            loc=v.loc
            if '90' in loc:
                loc=loc[:-1]
                
            #if loc=='9077':
              #  print v
            
            if day in compiled_list2:
                if loc in compiled_list2[day]:
                    compiled_list2[day][loc]+=1
                else:
                    compiled_list2[day][loc]=1
            else:
                compiled_list2[day]={}   
            
    coords_x_1=[]
    coords_y_1=[]
    for k, v in compiled_list2.iteritems():
        #print k
        #print v
        total_asset=len(v)
        total_entries=0
        for key, value in v.iteritems():
            total_entries+=value
        coords_x_1.append(total_asset)
        coords_y_1.append(total_entries)    

    print coords_x_1
    print coords_y_1
    sub1.scatter(coords_x_1, coords_y_1,c='b', marker='o', s=80)
    #plt.show()
    sub1.set_ylim(ymin=0)
    sub1.set_title('Total No. of alarm entries vs total no. of systems giving the alarms. One datapoint = one day')
    plt.savefig('output/plot/Aug Alarms.png')
    plt.close()

    
def crawl():
    settings.alarm={}
    print "\nIdentifying related log. Please wait.."
    alarm_index, readiness_index, schedule_index, skip_index=identify()  
  
    print "\nSorting alarm related log. Please wait.."
    create(alarm_index)   
    print "\nInitializing alarms. Please wait.."
    initialize_alarms()
    
    #print "\nToggling Comparison. Please wait.."
    #simpleSort(alarm_index)    
    #togSort(alarm_index)
    
    
    print "\nSorting readiness log. Please wait.."
    create_rsstatus(readiness_index)
    print "\nInitializing readiness log. Please wait.."
    initialize_rsstatus()
    
    print "\nSorting train schedule. Please wait.."
    create_schedule(schedule_index)
    
    print "\nIdentify Skip. Please wait.."
    settings.skip={}
    identifySkip(skip_index)
    
    