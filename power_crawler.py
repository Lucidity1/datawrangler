# -*- coding: utf-8 -*-
import settings
import print_progress as pp
import prettytable as pt
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import datetime as dt

def identify():
    total=len(settings.power)
    stabalizer=int(total/100)
    
    sixtyFourP_index=[]

    count=0
    for key, value in settings.power.iteritems():
        if '64P' in value['Description'] and 'Negative Voltage Detection' in value['Description']:
            sixtyFourP_index.append(key)
        count+=1
        if(count%stabalizer==0 or count/total>0.98):
            pp.printProgress(count,total, prefix='Identifying:', suffix='Complete', barLength=10)
    return sixtyFourP_index

def writeFile(content):
    with open(settings.ofname_power_64p, 'a') as fl:
        fl.write(content)
        

def generate(interests,sixtyFourP_index, name):
    
    for key, value in enumerate(interests):
        interests[key]='PWR '+value
    
    dictionary={}
           
    for interest in interests:
        
        x=pt.PrettyTable(["Status","Time"])
        count=0

        dictionary[interest]={}
        dictionary[interest]['Time']=[]
        dictionary[interest]['Status']=[]
        for index in sixtyFourP_index:
            if settings.power[index]['Sys/Sub']==interest:
                dictionary[interest]['Time'].append(settings.power[index]['Time'])         
                x.add_row([settings.power[index]['Status'],settings.power[index]['Time']])
                if "YES" in settings.power[index]['Status']:
                    count+=1
                    dictionary[interest]['Status'].append(1)
                elif "NO" in settings.power[index]['Status']:
                    dictionary[interest]['Status'].append(0)
        print '\n'+interest+' ('+str(count)+' trips)'+':'
        
        writeFile('\n'+interest+' ('+str(count)+' trips)'+':')
        if count>0:
            writeFile('\n')
            writeFile(x.get_string())
            print x
        writeFile('\n')
        
    #combine the plots       
    print "\n"+str(name)+" 64P Touch Voltage Protection Trip Sequence:"
    fig=plt.figure(1, figsize=(25,6))
    ax=fig.add_subplot(111)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))       
    ax.set_yticks(np.arange(0, 1.2, 1.0))
    ax.set_ylim(ymin=-0.2, ymax=3.0)
    ax.grid(True)
    ax.set_title(str(name)+" 64P Touch Voltage Protection Trip Sequence:")
    ax.set_ylabel("Trip Status")
    ax.set_xlabel("Incidence Time")
    mindate=None
    maxdate=None

    count=0

    for k,v in dictionary.iteritems():
        #print k
        time=v['Time']
        status=v['Status']
        
        if len(status)!=0:
            #print time
            #print status
            
            if mindate==None or min(time)<mindate:
                mindate=min(time)
            if maxdate==None or max(time)>maxdate:
                maxdate=max(time)
    
        
            ax.step(time,status, where='post',label=k)
            fig.autofmt_xdate(rotation=45)
            fig.tight_layout()
            
            store=None
            for index, value in enumerate(status):
                if value==1 and(store==None or time[index]-store>dt.timedelta(minutes=7)):          
                    ax.annotate(k[4:],xy=(time[index],1.1),xytext=(time[index],1.1+0.1*count))
                    store=time[index]
            count+=1
            #print "Count="+str(count)
       
    mindate= mindate+dt.timedelta(minutes=-30)
    maxdate= maxdate+dt.timedelta(minutes=60)
    
 
    
    ax.set_xlim(mindate, maxdate)
    ax.legend(loc=5)
    plt.savefig('output/plot/'+'64P Trip '+str(name)+'.png')
    print 'output/plot/'+'64P NSL Trip.png'+' generated'
    plt.close()
    

            
    #plt.show()
def crawl():
    settings.power_alarm={}
    print "\nIdentifying related log. Please wait.."
    sixtyFourP_index=identify()
    
    with open(settings.ofname_power_64p, 'w'):
        print 'Output file "'+settings.ofname_power_64p+'" created in root directory.'
  
    generate(settings.ns_lpu[:],sixtyFourP_index, 'NS')
    generate(settings.ew_lpu[:],sixtyFourP_index, 'EW')
    #interests=['PWR ALJ']
    
