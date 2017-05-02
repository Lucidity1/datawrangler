# -*- coding: utf-8 -*-
import settings
import prettytable as pt
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import gocc_alarm_analyzer_whisker as gaa

def writeFile(content):
    with open(settings.ofname_schedule, 'a') as fl:
        fl.write(content)
        
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
    
def requestCoord(train_id, time):
    rack=settings.rsschedule[train_id][time.date()]
    trip=None
    try:
        for row_index, row in enumerate(rack):
            if time>=row[0].time_start and time<=row[-1].time_start:
                trip=row_index+1
            elif time>=row[-1].time_start and time<=rack[row_index+1][0].time_start:
                trip=row_index+1
        if trip!=None:
            master_trip=[]
            for row in rack:
                master_trip+=row
            #print 'master_trip: ',master_trip
            for dwell_index, dwell in enumerate(master_trip):
                if dwell.time_start<=time and time<=master_trip[dwell_index+1].time_start:
                    if dwell.time_end<=time:
                        return [time,trip,str(master_trip[dwell_index+1].direction),str(dwell.station),'TRAVEL']
                    else:
                        return [time,trip,str(dwell.direction),str(dwell.station),'DWELL']
    except:
        print 'Error in RequestCoord: train_id, time:',train_id,' ', time
    return 'Unable to get train coordinate'

def printTrainAll(train_id, option='PRINT'):
    try:
        date_min=min(settings.rsschedule[train_id])
        date_max=max(settings.rsschedule[train_id])
        
        date=date_min
        while date<=date_max:
            printSchedule(train_id,date, option)
            date= date+ dt.timedelta(days=1)
    except:
        print 'ERROR in printTrainAll - train_id:', train_id
        
def printAll():
    temp=[]
    with open(settings.ofname_schedule, 'w'):
        print 'Output file "'+settings.ofname_schedule+'" created in root directory.'
    
    for k, v in settings.rsschedule.iteritems():
        temp.append(k)
    temp=sorted(temp)
    for item in temp:
        printTrainAll(item, 'SAVE')

def printSchedule(train_id, date, option='PRINT'):
    if date!='all':
        rack = settings.rsschedule[train_id][date]
        if rack!=None:
            if option=='PRINT':
                for index, row in enumerate(rack):
                    print '\nTRIP ',index+1,':'
                    x=pt.PrettyTable(["RS no.", "station", "direction", "dwell time", "open_time"])
                    if len(row)<17:
                        print 'WARNING: Wrong station estimation (<17)'
                    for dwell in row:
                        x.add_row(dwell.get_string())
                    print x
            if option=='SAVE':
                for index, row in enumerate(rack):
                    writeFile('\nTRIP '+str(index+1)+':\n')
                    x=pt.PrettyTable(["RS no.", "station", "direction", "dwell time", "open_time"])
                    if len(row)<17:
                        writeFile('WARNING: Wrong station estimation (<17)\n')
                    for dwell in row:
                        x.add_row(dwell.get_string())
                    writeFile(x.get_string())          
                writeFile("\n////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////\n")
    else:
        printTrainAll(train_id)

def printTrip(train_id, date, trip, option="PRINT"):
    if option=="PRINT":
        rack = settings.rsschedule[train_id][date]
        row=rack[trip]
        print '\nTRIP ',trip+1,':'
        x=pt.PrettyTable(["RS no.", "station", "direction", "dwell time", "open_time"])
        if len(row)<17:
            print 'WARNING: Wrong station estimation (<17)'
        for dwell in row:
            x.add_row(dwell.get_string())
        print x
    elif option=="SAVE":
        rack = settings.rsschedule[train_id][date]
        temp=[]
        row=rack[trip]
        temp= '\nTRIP '+str(trip+1)+':'
        x=pt.PrettyTable(["RS no.", "station", "direction", "dwell time", "open_time"])
        if len(row)<17:
            temp=temp+'WARNING: Wrong station estimation (<17)\n'
        else:
            temp=temp+'\n'
        for dwell in row:
            x.add_row(dwell.get_string())
        return temp+x.get_string()

def graphTrip(train_id, date, option="PRINT"):
        rack = settings.rsschedule[train_id][date]
        coord_basket=[]
        if option=="PRINT":
            #print stations
            #print time
            #print mdates.num2date(time)
            fig=plt.figure(1, figsize=(200,30))
            ax=fig.add_subplot(111)
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))            
            ax.set_yticks(np.arange(0, 19, 1.0))
            ax.set_ylim(ymin=1, ymax=19)
            ax.set_title("Trip Plot "+str(train_id)+" "+str(date))
            ax.set_ylabel("Stations")
            ax.set_xlabel("Time")
            ax.grid(True)
            
            time_all=[]
            for row in rack:
                stations=[]
                time=[]
                
                for dwell in row:
                    stations.append(dwell.station)
                    time.append(mdates.date2num(dwell.time_start))
                    stations.append(dwell.station)
                    time.append(mdates.date2num(dwell.time_end))
                

                ax.plot_date(time, stations, ls='-', marker='o', linewidth=3.0, color=settings.color_code[0])
                time_all+=time
            ax.set_xticks(time_all)
                
            plt.rcParams.update({'font.size': 12})
            fig.autofmt_xdate(rotation=45)
            fig.tight_layout()
            
            coord_basket=gaa.analyzeTrain(train_id)

            for item in coord_basket:
                if item[4]=="DWELL":
                    st=float(item[3])
                elif item[4]=="TRAVEL":
                    st=float(item[3])+0.5
                ax.plot_date(item[0], st, ls='-', marker='*', markersize=60,linewidth=10.0, color='#FF0000')
        

            plt.savefig('output/plot/'+"Trip Plot "+str(train_id)+" "+str(date)+'.png')
            print 'output/plot/'+"Trip Plot "+str(train_id)+" "+str(date)+'.png'+' generated'
            plt.close()
            #plt.show()
        
def graphTripAll(date):
    rs=[]
    for k, v in settings.rsschedule.iteritems():
        rs.append(k)
    rs=sorted(rs)

    #print stations
    #print time
    #print mdates.num2date(time)
    fig=plt.figure(1, figsize=(200,30))
    ax=fig.add_subplot(111)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))            
    ax.set_yticks(np.arange(0, 19, 1.0))
    ax.set_ylim(ymin=0, ymax=19)
    ax.set_title("Trip Plot All "+"+str(date)")
    ax.set_ylabel("Stations")
    ax.set_xlabel("Time")
    ax.grid(True)
    
    time_all=[]    
    
    
    for index,train_id in enumerate(rs):
        try:
            rack = settings.rsschedule[train_id][date]
    
            for row in rack:
                stations=[]
                time=[]
                
                for dwell in row:
                    stations.append(dwell.station)
                    time.append(mdates.date2num(dwell.time_start))
                    stations.append(dwell.station)
                    time.append(mdates.date2num(dwell.time_end))
                
    
                ax.plot_date(time, stations, ls='-', marker='o', linewidth=3.0, color=settings.color_code[index])
                time_all+=time
        except:
            print 'Skipping Train ID: ',train_id
            pass
                
    #ax.set_xticks(time_all)
        
    plt.rcParams.update({'font.size': 12})
    fig.autofmt_xdate(rotation=45)
    fig.tight_layout()

    coord_basket=gaa.analyze()

    for item in coord_basket:
        if item[4]=="DWELL":
            st=float(item[3])
        elif item[4]=="TRAVEL":
            st=float(item[3])+0.5
        ax.plot_date(item[0], st, ls='-', marker='*', markersize=60,linewidth=10.0, color='#FF0000')

    plt.savefig('output/plot/'+"Trip Plot All "+str(date)+'.png')
    print 'output/plot/'+"Trip Plot All "+str(date)+'.png'+' generated'
    plt.close()
    #plt.show()        
    
def query(train_id='',date=''):
    if not len(settings.rsschedule)==0:
        if train_id=='':
            train_id = str(raw_input('\nPROMPT: Enter RS number: '))
        
        if date=='':
            while (True):
                date = str(raw_input('PROMPT: Enter search date (DD/MM/YYYY): '))          
                date=date.lower()            
                if date == 'all':
                    break
                elif checkFormat(date):
                    break
                else:
                    print "Invalid date format. Retry."
    
        if date != 'all':
            date=convTime(date).date()
 
        
        printSchedule(train_id, date)
        graphTrip(train_id, date)
        graphTripAll(date)
        
    else:
        print 'Schedule table empty. Re-run /occ_crawl.'