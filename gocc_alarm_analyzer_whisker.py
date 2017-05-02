# -*- coding: utf-8 -*-
'''
import settings
import matplotlib.pyplot as plt

def categorize():
    rs_alarm = {k:v for k, v in settings.alarm.items() if 'Signalling changed to FBSS' in v.description and settings.rsstatus[v.loc[:-1]+'2'].request(v.min_time)}
    return rs_alarm

def writeFile(content):
    with open(settings.ofname_alarm_analyzer, 'a') as fl:
        fl.write(content)

def analyze():
    rs_alarm=categorize()
    
    rs_basket=[]
    with open(settings.ofname_alarm_analyzer, 'w'):
        print 'Output file "'+settings.ofname_alarm_analyzer+'" created in root directory.'
    
    for k,v in rs_alarm.iteritems():
        time=v.total_time
        if time==None:
            time=0
        else:
            time=time.total_seconds()
            if time>0:
                #print '\nAlarm_id: ',k,' more than 50seconds (',str(time),'s)\n'                
                #print settings.alarm[k]
                writeFile('\nAlarm_id: '+k+' more than 50seconds ('+str(time)+'s)\n')
                writeFile(settings.alarm[k].to_string())
            
            rs_basket.append(time)
      

    
    
    fig=plt.figure(figsize=(20,20))
    sub1=fig.add_subplot(111)
    sub1.boxplot([rs_basket], whis=5)
    sub1.set_xticklabels("Alarm timespan / Signalling changed to FBSS")

    axes = plt.gca()
    axes.set_ylim([0,50])

    sub1.set_title("RS all alarms timespan")
    plt.savefig('output/plot/RS all alarms timespan.png', format='png')
        
    plt.show()
    '''

import settings
import matplotlib.pyplot as plt
import datetime as dt
import gocc
import gocc_rsstatus
import gocc_dwell as gd

def categorize():
    rs_alarm = {k:v for k, v in settings.alarm.items() if 'EB' in v.description and settings.rsstatus[v.loc[:-1]+'2'].request(v.min_time)}
    return rs_alarm

def categorize_train(train_id):
    rs_alarm = {k:v for k, v in settings.alarm.items() if 'EB' in v.description and settings.rsstatus[v.loc[:-1]+'2'].request(v.min_time) and train_id in v.equipment}
    return rs_alarm
    
def writeFile(content):
    with open(settings.ofname_alarm_analyzer, 'a') as fl:
        fl.write(content)

def analyzeTrain(train_id):
    rs_alarm=categorize_train(train_id)
    count=0
    filter=0
    #ignore=0.5*60*60
    ignore_start=dt.datetime.strptime('00:30:00',"%H:%M:%S").time()
    ignore_end= dt.datetime.strptime('04:30:00',"%H:%M:%S").time()
    
    rs_basket=[]
    coord_basket=[]
    with open(settings.ofname_alarm_analyzer, 'w'):
        print 'Output file "'+settings.ofname_alarm_analyzer+'" created in root directory.'
    
    writeFile('ALARM ANALYZER - EMERGENCY BRAKE\n')
    writeFile('================================')
    
    for k,v in rs_alarm.iteritems():
        time=v.total_time
        if time==None:
            time=0
        else:
            time=time.total_seconds()
            if not ignore_start<=v.min_time.time()<=ignore_end:
                if time>=filter:
                    #print '\nAlarm_id: ',k,' more than 50seconds (',str(time),'s)\n'                
                    #print settings.alarm[k]
                    search=v.truncate()[:-1]
                    writeFile('\n\nAlarm_id: '+k+' more than '+str(filter)+' seconds ('+str(time)+'s)\n')
                    coord=gd.requestCoord(search,v.min_time)   
                    coord_basket.append(coord)
                    writeFile(str(coord)) 
                    writeFile('\n')
                    writeFile(settings.alarm[k].to_string())
                    writeFile(gocc_rsstatus.query(search, v.min_time.date(),True))
                    writeFile('\n')                    
                    writeFile(gd.printTrip(search,v.min_time.date(),coord[1]-1,"SAVE"))
                    writeFile(gocc.queryTime(search, v.min_time, v.max_time))
                    
            
                rs_basket.append(time)
            else:
                count+=1
      
    writeFile('\n'+str(count)+' non-service hr alarms have been filtered off')
    
    
    fig=plt.figure(figsize=(20,20))
    sub1=fig.add_subplot(111)
    sub1.boxplot([rs_basket], whis=1)
    sub1.set_xticklabels("Alarm timespan / EB initiated by the ATP")

    #axes = plt.gca()
    #axes.set_ylim([0,200])

    sub1.set_title("RS all eb alarms timespan, september 2016")
    plt.savefig('output/plot/RS-EB initiated by the ATP-alarm timespan.png', format='png')
     
    plt.close()
    #plt.show()
    return coord_basket
    
def analyze():
    rs_alarm=categorize()
    count=0
    filter=0
    #ignore=0.5*60*60
    ignore_start=dt.datetime.strptime('00:30:00',"%H:%M:%S").time()
    ignore_end= dt.datetime.strptime('04:30:00',"%H:%M:%S").time()
    
    rs_basket=[]
    coord_basket=[]
    with open(settings.ofname_alarm_analyzer, 'w'):
        print 'Output file "'+settings.ofname_alarm_analyzer+'" created in root directory.'
    
    writeFile('ALARM ANALYZER - EMERGENCY BRAKE\n')
    writeFile('================================')
    
    for k,v in rs_alarm.iteritems():
        time=v.total_time
        if time==None:
            time=0
        else:
            time=time.total_seconds()
            if not ignore_start<=v.min_time.time()<=ignore_end:
                if time>=filter:
                    #print '\nAlarm_id: ',k,' more than 50seconds (',str(time),'s)\n'                
                    #print settings.alarm[k]
                    search=v.truncate()[:-1]
                    writeFile('\n\nAlarm_id: '+k+' more than '+str(filter)+' seconds ('+str(time)+'s)\n')
                    coord=gd.requestCoord(search,v.min_time)   
                    coord_basket.append(coord)
                    writeFile(str(coord)) 
                    writeFile('\n')
                    writeFile(settings.alarm[k].to_string())
                    writeFile(gocc_rsstatus.query(search, v.min_time.date(),True))
                    writeFile('\n')                    
                    writeFile(gd.printTrip(search,v.min_time.date(),coord[1]-1,"SAVE"))
                    writeFile(gocc.queryTime(search, v.min_time, v.max_time))
                    
            
                rs_basket.append(time)
            else:
                count+=1
      
    writeFile('\n'+str(count)+' non-service hr alarms have been filtered off')
    
    
    fig=plt.figure(figsize=(20,20))
    sub1=fig.add_subplot(111)
    sub1.boxplot([rs_basket], whis=1)
    sub1.set_xticklabels("Alarm timespan / EB initiated by the ATP")

    #axes = plt.gca()
    #axes.set_ylim([0,200])

    sub1.set_title("RS all eb alarms timespan, september 2016")
    plt.savefig('output/plot/RS-EB initiated by the ATP-alarm timespan.png', format='png')
     
    plt.close()
    #plt.show()
    return coord_basket