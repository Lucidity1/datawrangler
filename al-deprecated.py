# -*- coding: utf-8 -*-
import settings
import prettytable as pt

global search
search=''

def searchArea(local_search):
    global search
    if local_search=='':
        local_search = str(raw_input('\nPROMPT: Enter search term for equipment: '))
        search=local_search
    count=0
    results=[]
    for index,eqm in enumerate(settings.assetlisting_equipmenttype):
        if search in eqm:
            count+=1
            results.append(index);
    print count," entries found.\n"
    return results
    
def searchAsset():
    if not len(settings.list_node)==0:
        results=searchArea('')       
        
        x=pt.PrettyTable(["Equipment","Physical Area Code", "Description"])
        count=0
        for result in (results):                
            x.add_row([settings.assetlisting_equipmenttype[result],settings.assetlisting_areacode[result],settings.assetlisting_description[result]])
            count=count+1
            #print len(settings.assetlisting_description[result])
            if count==10:
                break
        x.set_field_align("Description", "r")
        print x
        
        '''
        for item in settings.assetlisting_description:
            print item
            '''
    else:
        print 'Asset listing table empty. Re-run /al_crawl.'

