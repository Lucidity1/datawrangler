# -*- coding: utf-8 -*-

import settings
import datetime as dt
import prettytable as pt
from operator import itemgetter
import matplotlib.pyplot as plt
import numpy as np

global search
search=''

def convTime(timestring):
    return dt.datetime.strptime(timestring, "%d/%m/%Y")
        
def checkFormat(timestring):
    condition=True
    data = timestring.split("/")
    if len(data)!=3:
        condition=False
    else:
        if not (data[0].isdigit() & data[1].isdigit() & data[2].isdigit()):
            condition = False
        if not len(data[2])==4:
            condition = False
    return condition

def printAlarm(alarms):
    for alarm in alarms:
        print alarm.alarm_id
        
def search(search,date):
    count=0
    results=[]
    global search_g
    global date_g
    
    if search=='':
        search = str(raw_input('\nPROMPT: Enter search term for equipment: '))
        search_g=search
    if date=='':
        while (True):
            date = str(raw_input('PROMPT: Enter search date (DD/MM/YYYY): '))
            date_g= date           
            date=date.lower()            
            if date == 'all':
                break
            elif checkFormat(date):
                break
            else:
                print "Invalid date format. Retry."

    if date != 'all':
        date=convTime(date).date()
        for k,v in settings.alarm.iteritems():
            temp=v.min_time
            if temp!= None:
                temp=temp.date()
            if search in v.equipment and date==temp:
                count+=1
                results.append(k);   
    else:
        for k,v in settings.alarm.iteritems():
            if search in v.equipment:
                count+=1
                results.append(k);
        
    print count," unique alarms found.\n"
    return results
    
    
def identifyRecur(event_ids):
    alarms_recur=[]
    for event_id in event_ids:
        name=str(settings.alarm[event_id].equipment)+'_'+str(settings.alarm[event_id].description)    
        if any(name in sublist[0] for sublist in alarms_recur):
            for sublist in alarms_recur:
                if sublist[0]==name:
                    time=settings.alarm[event_id].total_time
                    if time != None:
                        sublist[1]+=time
                    break
        else:
            time=settings.alarm[event_id].total_time
            if time==None:
                time=dt.timedelta(seconds=0)
            alarms_recur.append([name,time])
    
    alarms_recur=sorted(alarms_recur,key=itemgetter(1),reverse=True)
    return alarms_recur

def calcGini(x_list, y_list):
    lorenz=np.trapz([y_list], x=x_list)  
    return ((5000-lorenz)/5000)
    
def pareto(result_list):
    plt.figure(1, figsize=(6,4.5))
    plt.xlabel('% of Equipment')
    plt.ylabel('% of Time')
    plt.grid(True)
    plt.hold(True)
    lw=1
    def_x=[0,20,40,60,80,100]
    def_y=[0,20,40,60,80,100]
    perc_x=[]
    perc_y=[]
    
    result_list=sorted(result_list,key=itemgetter(1))
    sum=0
    for result in (result_list):
        sum=sum+result[1].total_seconds()
    perc_x.append(0)
    perc_y.append(0)
    internal_sum=0
    for index, result in enumerate(result_list):
        internal_sum=internal_sum+result[1].total_seconds()
        perc_x.append((index+1)/float(len(result_list))*100)
        perc_y.append(internal_sum/float(sum)*100)
        
    plt.plot(def_x, def_y, settings.color_code[0], linewidth=lw)
    plt.plot(perc_x, perc_y, settings.color_code[1], linewidth=lw)

    gini=calcGini(perc_x,perc_y)
    print "Pareto Plot for equipment area "+ search_g +', date: '+date_g+" generated."
    
    #legend((r'$y_m$', r'$y_l$'), prop=FontProperties(size=16))
    #legend((r'${\dot\Theta}_m$', r'${\dot\Theta}_1$', r'${\dot\Theta}_2$', r'${\dot\Theta}_l$'), prop=FontProperties(size=16))
    plt.title('Event Pareto Distribution for "'+search_g+'"'+', date: '+date_g)
    plt.savefig('output/plot/'+search_g+'_'+date_g+'.png')
    
    plt.show()
    return gini    

        

def queryIndex(event_id):
    for index, item in enumerate(settings.gocc_id):
        if item == event_id:
            return index
    
def query():
    if not len(settings.alarm)==0:
        results=search('','')       
        
        if not len(results)==0:
            for result in results:
                print settings.alarm[result]
            print '\n',len(results),'unique alarms found.\n'
            

            results=identifyRecur(results)
            y=pt.PrettyTable(["S\N","Equipment_Desc","total_time"])
            for index in range(0, len(results)):         
                y.add_row([index+1, results[index][0], results[index][1]])
            print y
            
            #deduce pareto
            gini=pareto(results)
            print "\nGini Coefficient: "+str(gini)
    else:
        print 'Alarm table empty. Re-run /occ_crawl.'
  