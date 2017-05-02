# -*- coding: utf-8 -*-
import settings
import csv
import print_progress as pp

    
def scan():
    settings.assetlisting_asset=[]
    settings.assetlisting_description=[]
    settings.assetlisting_location=[]
    settings.assetlisting_locationcode=[]
    settings.assetlisting_owner=[]
    settings.assetlisting_equipmenttype=[]
    settings.assetlisting_areacode=[]
    settings.assetlisting_serial=[]
    settings.assetlisting_parent=[]
    settings.assetlisting_item=[]
    settings.assetlisting_status=[]
    
    count=0
    total=len(settings.fname_assetlisting)    
    
    
    for file in settings.fname_assetlisting:
        with open(file,'rb') as csvfile:
            reader=csv.DictReader(csvfile, delimiter = ';')
            if settings.scan_report==True:
                print "Scanning File: ", file    
            data_line=0
            
            for row in reader:
                settings.assetlisting_asset.append(row['Asset'])
                settings.assetlisting_description.append(row['Description'])
                settings.assetlisting_location.append(row['Location'])
                settings.assetlisting_locationcode.append(row['Location Code'])
                settings.assetlisting_owner.append(row['Maintenance Owner'])
                settings.assetlisting_equipmenttype.append(row['Equipment Type'])
                settings.assetlisting_areacode.append(row['Physical Area Code'])
                settings.assetlisting_serial.append(row['Serial #'])
                settings.assetlisting_parent.append(row['Parent'])
                settings.assetlisting_item.append(row['Rotating Item'])
                settings.assetlisting_status.append(row['Status'])
                data_line += 1
                
            count+=1
            pp.printProgress(count,total, prefix='Scanning Asset Listing:', suffix='Complete', barLength=10)
        
            if settings.scan_report==True:
                print "There are ",data_line, " lines"

