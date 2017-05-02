# -*- coding: utf-8 -*-

import settings
import datetime as dt
from operator import itemgetter

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

def sort(rsstatus):
    for index in rsstatus:
        settings.rsstatus[rsstatus].date
        
def search(search):
    count=0
    results=[]
    global search_g
    
    if search=='':
        search = str(raw_input('\nPROMPT: Enter RS number: '))
        search_g=search
    '''
    if date_l=='':
        while (True):
            date_l = str(raw_input('PROMPT: Enter search date (DD/MM/YYYY): '))
            date_g= date_l           
            date_l=date_l.lower()            
            if date_l == 'all':
                break
            elif checkFormat(date_l):
                break
            else:
                print "Invalid date format. Retry."

    if date_l != 'all':
        date_l=convTime(date_l).date()
        for k,v in settings.rsstatus.iteritems():
            if search in v.loc and date_l==v.date:
                count+=1
                results.append([k,v.date]);   
    else:
    '''
    for k,v in settings.rsstatus.iteritems():
        if v.status_id != None:
            if search in v.loc:
                count+=1
                return k
                
    
    
        

def queryIndex(event_id):
    for index, item in enumerate(settings.gocc_id):
        if item == event_id:
            return index
    
def query(se='',date='',printout=False):
    if not len(settings.rsstatus)==0:
        result=search(se)
        
        if printout==False:
            #if not len(results)==0:
                #for result in results:
            print settings.rsstatus[result]
                #print '\n',len(results),'RS status entry found.\n'
        elif printout==True:
            return settings.rsstatus[result].to_string(date)      
            

    else:
        print 'RSStatus table empty. Re-run /occ_crawl.'
  