# -*- coding: utf-8 -*-
import settings
import csv
import datetime as dt
import print_progress as pp

def convTime(datestring,timestring):
    return dt.datetime.strptime(datestring+' '+timestring, "%d/%m/%y %H:%M:%S ")
    

def tryInt(s):
    try:
        int(s)
        return int(s)
    except ValueError:
        return s
    
def scan():   
    count=0
    total=len(settings.fname_power)    
        
    for file in settings.fname_power:
        with open(file,'rb') as csvfile:
            reader=csv.DictReader(csvfile, delimiter = ',')
            if settings.scan_report==True:
                print "Scanning File: ", file    
            data_line=0
            
            for row in reader:
                try:
                    settings.power[data_line]={\
                    'id':data_line,\
                    'Time':convTime(row['Date'],row['Time']),\
                    'Phy Add':row['Phy Add'],\
                    'Sys/Sub':row['Sys/Sub'],\
                    'SubSys':row['SubSys'],\
                    'Description':row['Description'],\
                    'Status':row['Status'],\
                    'RC':row['RC'],\
                    'User':row['User'],
                    }
                except Exception as e: print str(e)
                data_line += 1
                
            count+=1
            pp.printProgress(count,total, prefix='Scanning GOCC Log:', suffix='Complete', barLength=10)
        
            if settings.scan_report==True:
                print "There are ",data_line, " lines"
                print settings.power[35]
