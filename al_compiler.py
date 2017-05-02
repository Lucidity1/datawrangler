# -*- coding: utf-8 -*-
import settings
import csv
import print_progress as pp
import sys

def tryInt(s):
    try:
        int(s)
        return int(s)
    except ValueError:
        return s
    
def scan():   
    count=0
    total=len(settings.fname_assetlisting)    
        
    for file in settings.fname_assetlisting:
        with open(file,'rb') as csvfile:
            reader=csv.DictReader(csvfile, delimiter = ';')
            if settings.scan_report==True:
                print "Scanning File: ", file    
            data_line=0
            
            for row in reader:
                try:
                    settings.al[row['Asset']]={\
                    'Description':row['Description'],\
                    'Location':row['Location'],\
                    'Location Code':row['Location Code'],\
                    'Maintenance Owner':row['Maintenance Owner'],\
                    'Equipment Type':(row['Equipment Type']),\
                    'Physical Area Code':(row['Physical Area Code']),\
                    'Serial #':row['Serial #'],\
                    'Parent':row['Parent'],\
                    'Rotating Item':row['Rotating Item'],\
                    'Status':row['Status'],\
                    }
                except:
                    #print "Fail to scan Line ",data_line
                    print "Unexpected error:", sys.exc_info()[1]
                    pass
                data_line += 1
                
            count+=1
            pp.printProgress(count,total, prefix='Scanning Asset Listing:', suffix='Complete', barLength=10)
        
            if settings.scan_report==True:
                print "There are ",data_line, " lines"

    
    
