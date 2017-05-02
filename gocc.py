# -*- coding: utf-8 -*-

import settings
import datetime as dt
import prettytable as pt
from operator import itemgetter
import matplotlib.pyplot as plt
#from pylab import show, figure, plot, xlabel, ylabel, grid, hold, legend, title, savefig

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

def searchArea(local_search):
    global search
    if local_search=='':
        local_search = str(raw_input('\nPROMPT: Enter search term for equipment: '))
        search=local_search
    count=0
    results=[]
    for index,eqm in enumerate(settings.gocc_equipment):
        if search in eqm:
            count+=1
            results.append(index);
    print count," entries found.\n"
    return results

def searchWithin(eqm, start, end):
    count=0
    results=[]
    
    for k,v in settings.gocc.iteritems():
        if eqm in v['equipment'] and start<=v['sourcetime']<=end:
            count+=1
            results.append(k);   
    return results

    
def searchDate(index_list, date):
    if date=='':
        while (True):
            date = str(raw_input('\nPROMPT: Enter search date (DD/MM/YYYY): '))
            date=date.lower()            
            if date == 'all':
                break
            elif checkFormat(date):
                break
            else:
                print "Invalid date format. Retry."
    count=0
    results=[]
    
    if not date == 'all':
        date=convTime(date).date()
        for index in index_list:
            if settings.gocc_sourcetime[index].date()==date:
                results.append(index)
                count+=1
        print count," entries found.\n"
       
           
    else:
        for index in index_list:
            results.append(index)
            count+=1
        print count," entries found.\n"
    return results
    
def identifyRecur(alarms):
    events_filter_limit=0
    alarms_recur=[]
    for index in alarms:
        tracker=False
        for index2, sublist in enumerate(alarms_recur):
            if settings.gocc_equipment[index] == sublist[0]:
                alarms_recur[index2][1]=sublist[1]+1
                tracker=True
        if tracker==False:
            alarms_recur.append([settings.gocc_equipment[index],1])
    
    alarms_recur[:]= [sublist for sublist in alarms_recur if sublist[1]>=events_filter_limit]
    alarms_recur=sorted(alarms_recur,key=itemgetter(1),reverse=True)
    return alarms_recur
    
def pareto(result_list):
    plt.figure(1, figsize=(6,4.5))
    plt.xlabel('% of Equipment Area')
    plt.ylabel('% of Event Log')
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
        sum=sum+result[1]
    perc_x.append(0)
    perc_y.append(0)
    internal_sum=0
    for index, result in enumerate(result_list):
        internal_sum=internal_sum+result[1]
        perc_x.append((index+1)/float(len(result_list))*100)
        perc_y.append(internal_sum/float(sum)*100)
        
    plt.plot(def_x, def_y, settings.color_code[0], linewidth=lw)
    plt.plot(perc_x, perc_y, settings.color_code[1], linewidth=lw)

    print "Pareto Plot for equipment area "+ search +" generated."
    
    #legend((r'$y_m$', r'$y_l$'), prop=FontProperties(size=16))
    #legend((r'${\dot\Theta}_m$', r'${\dot\Theta}_1$', r'${\dot\Theta}_2$', r'${\dot\Theta}_l$'), prop=FontProperties(size=16))
    plt.title('Event Pareto Distribution for Equipment Area "'+search+'"')
    plt.show()
        

def queryTime(eqm, start, end):
    results=searchWithin(eqm, start, end)
    
    if not len(results)==0:
        x=pt.PrettyTable(["Time","Event Type","Equipment","Description","Value"])
        for result in (results):                
            x.add_row([settings.gocc[result]['sourcetime'],settings.gocc[result]['eventtype'],settings.gocc[result]['equipment'],settings.gocc[result]['description'],settings.gocc[result]['value']])
        return "\n"+x.get_string(sortby='Time')+"\n"
    
    
def query():
    results=searchArea('')       
    results=searchDate(results,'')
    
    if not len(results)==0:
        x=pt.PrettyTable(["Time","Event Type","Equipment","Description","Value"])
        
        for result in (results):                
            x.add_row([settings.gocc_sourcetime[result],settings.gocc_eventtype[result],settings.gocc_equipment[result],settings.gocc_description[result],settings.gocc_value[result]])
        print x
        
        #list top 10
        results=identifyRecur(results)
        limit=min(len(results), settings.pareto_limit)
        y=pt.PrettyTable(["S\N","Equipment","Recurrence"])
        for index in range(0, limit):         
            y.add_row([index+1, results[index][0], results[index][1]])
        print y
        
        #deduce pareto
        pareto(results)
  