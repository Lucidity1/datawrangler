
# -*- coding: utf-8 -*-
import settings
import csv
import datetime as dt
import print_progress as pp
import sys

def convTime(timestring, file,data_line,marker="", surpress=False):
    try:
        return dt.datetime.strptime(timestring, "%d/%m/%Y %H:%M:%S")
    except:
        if surpress==False:
            print "Time format error detected at "+file+" line "+str(data_line)+"-"+str(marker)
            return None
    

def tryInt(s):
    try:
        int(s)
        return int(s)
    except ValueError:
        return s
    
def scan():   
    count=0
    total=len(settings.fname_wo)    
        
    for file in settings.fname_wo:
        with open(file,'rb') as csvfile:
            reader=csv.DictReader(csvfile, delimiter = '$')
            if settings.scan_report==True:
                print "Scanning File: ", file    
            data_line=0
            
            for row in reader:
                if not (row['Reported Date']=='' or convTime(row['Reported Date'],file,data_line,"",True)==None):
                    try:
                        settings.wo[row['Work Order']]={\
                        'Work Order':tryInt(row['Work Order']),\
                        'Description':row['Description'],\
                        'Asset':row['Asset'],\
                        'Work Type':row['Work Type'],\
                        'Work Group':row['Work Group'],\
                        #'Actual Start':convTime(row['Actual Start'],data_line,1),\
                        #'Actual Finish':convTime(row['Actual Finish'],data_line,2),\
                        'Reported Date':convTime(row['Reported Date'],file,data_line,3),\
                        }
                    except:
                        #print "Fail to scan Line ",data_line
                        print "Unexpected error:", sys.exc_info()[1]
                        pass
                else:
                    #print "skipping line: ",data_line
                    pass
                data_line += 1
                
            count+=1
            pp.printProgress(count,total, prefix='Scanning WO Log:', suffix='Complete', barLength=10)
        
            if settings.scan_report==True:
                print "There are ",data_line, " lines"

def query():
    search= str(raw_input('\nPROMPT: Enter WO number: ')) 
    
    print settings.wo[search]