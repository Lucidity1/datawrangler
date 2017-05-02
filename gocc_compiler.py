# -*- coding: utf-8 -*-
import settings
import csv
import datetime as dt
import print_progress as pp

def convTime(timestring):
    try:
        place=timestring.index('.')
        timestring=timestring[:place]
    except ValueError:
        timestring=timestring
    return dt.datetime.strptime(timestring, "%Y-%m-%d %H:%M:%S")
    

def tryInt(s):
    try:
        int(s)
        return int(s)
    except ValueError:
        return s
    
def scan():   
    count=0
    total=len(settings.fname_gocc)    
        
    for file in settings.fname_gocc:
        with open(file,'rb') as csvfile:
            reader=csv.DictReader(csvfile, delimiter = ',')
            if settings.scan_report==True:
                print "Scanning File: ", file    
            data_line=0
            
            for row in reader:
                try:
                    settings.gocc[row['id']]={\
                    'id':tryInt(row['id']),\
                    'uniqueid':row['uniqueid'],\
                    'alarm':row['alarm'],\
                    'eventtype':row['eventtype'],\
                    'system':row['system'],\
                    'subsystem':row['subsystem'],\
                    'sourcetime':convTime(row['sourcetime']),\
                    'operator':row['operator'],\
                    'alarmvalue':tryInt(row['alarmvalue']),\
                    'value':row['value'],\
                    'equipment':row['equipment'],\
                    'location':row['location'],\
                    'severity':tryInt(row['severity']),\
                    'description':row['description'],\
                    'state':tryInt(row['state']),\
                    'mmsstate':tryInt(row['mmsstate']),\
                    'zone':row['zone'],\
                    'graphicelement':row['graphicelement'],\
                    }
                except:
                    pass
                data_line += 1
                
            count+=1
            pp.printProgress(count,total, prefix='Scanning GOCC Log:', suffix='Complete', barLength=10)
        
            if settings.scan_report==True:
                print "There are ",data_line, " lines"
