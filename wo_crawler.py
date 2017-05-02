# -*- coding: utf-8 -*-
import settings
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime as dt

def writeFile(content):
    with open(settings.ofname_wo_crawler, 'a') as fl:
        fl.write(content)

def sortFn(array):
    return len(array[1])

def printTable(array):
    #print 'Asset\n'
    writeFile('Asset\n')
    #print '\t'
    writeFile('\t')
    #print 'Work Orders'+'\n'
    writeFile('Work Orders'+'\n')
    
    for index, item in enumerate(array):
        #print str(index+1)+'. '+str(item[0])+'; '+str(len(item[1]))+'\n'
        writeFile(str(index+1)+'. '+str(item[0])+'; '+str(len(item[1]))+'\n')
        #print '\t'
        writeFile('\t')
        #print str(item[1])+'\n'
        writeFile(str(item[1])+'\n')

def crawl():
    wo_count_limit=15
    counter={}
    print "\nCrawling WOs. Please wait.."
    for k,v in settings.wo.iteritems():
        if v['Work Type']=="CM" and v['Asset']!='':
            if v['Asset'] in counter:
                counter[v['Asset']].append(k)
            else:
                counter[v['Asset']]=[k]
    
    print "Crawling done.\n"

    
    freq=sorted(counter.items(), key=sortFn, reverse=True)
    
    freq_filtered=[]
    for item in freq:
        if len(item[1])>=wo_count_limit:
            freq_filtered.append(item)
    
    
    
    with open(settings.ofname_wo_crawler, 'w'):
        print 'Output file "'+settings.ofname_wo_crawler+'" created in root directory.'
    
    writeFile('Assets with >='+str(wo_count_limit)+' WOs in the time period. Sorted in descending order.\n')
    print printTable(freq_filtered)
    print 'Output file recorded.'
    
    
    print "Generating N(t) Plot. Please wait.."
        
    for item in freq_filtered:
        x=[]
        count=0
        asset_id=item[0]
        for wo in item[1]:          
            x.append(settings.wo[wo]["Reported Date"])
            count+=1
        x.sort()
        y = np.arange(1, count+1, 1)
        
        fig=plt.figure(1, figsize=(30,30))        
        ax=fig.add_subplot(111)
        ax.set_yticks(np.arange(0, count+2, 1))
        ax.set_ylim(ymin=0)
        ax.set_xlim(xmin=dt.datetime(2016,1,1), xmax=dt.datetime(2016,11,30))
        #ax.set_xticks(x)
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m-%Y'))            
        ax.set_title("N(t) Plot for Asset ID: "+asset_id)
        ax.set_ylabel("N(t)")
        ax.set_xlabel("Time")
        ax.grid(True)
        
        ax.plot_date(x, y, marker='o',markersize=30, linewidth=1.0, color=settings.color_code[0])
        plt.rcParams.update({'font.size': 20})
        fig.autofmt_xdate(rotation=45)
        fig.tight_layout()
        
        plt.savefig('output/plot/'+"N(t) Plot for Asset ID "+asset_id+'.png')
        print 'output/plot/'+"N(t) Plot for Asset ID "+asset_id+'.png'+' generated'
        plt.close()
    
    print "All N(t) Plot has been generated."