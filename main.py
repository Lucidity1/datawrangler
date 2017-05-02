# -*- coding: utf-8 -*-
import settings
import header

import al_compiler
#import al
import al_crawler

import gocc_compiler
#import gocc
import gocc_crawler
import gocc_alarm
import gocc_rsstatus
import gocc_alarm_analyzer_whisker
import gocc_dwell
import gocc_skip
#import pm_compiler
#import cm_compiler

import wo_compiler
import wo_crawler

#import summary


#import pm_data
#import cm_data

import power_compiler
import power_crawler

import command_table

def main():
    #initialize global variables
    settings.init()
    
    #Display welcome header
    header.header()
    
    #Load Files
    print "\nScanning Files. Please wait.."
    #al_compiler.scan()
    #gocc_compiler.scan()
    #pmd_compiler.scan()
    #cmd_compiler.scan()
    #wo_compiler.scan()
    power_compiler.scan()
    print "Scan Complete.\n"
    
    #temp-  to be deletd
    #gocc_crawler.crawl()
    #gocc_alarm_analyzer_whisker.analyze()
    #summary.summary()
    #loop prompting for user command
    #al_crawler.crawl()
    #wo_crawler.crawl()
    power_crawler.crawl()
    
    while (False):
        counter=0 
        input = str(raw_input('\nPROMPT: Enter \
        \n\t"/summary" to generate report.{DEPRECATED}\
        \n\t"/listing_crawl" to generate asset listing tree. \
        \n\t"/occ_crawl" to generate OCC alarm tables. \
        \n\t"/alarm_query" to search OCC alarms by equipment and date. Must have run /occ_crawl.\
        \n\t"/expand" to show all available commands.\
        \n\t"/break" to terminate. \n'))
        
        input=input.lower()
        
        if input =='/occ_query':
            gocc.query()
        elif input=='/rsstatus_query':
            gocc_rsstatus.query()
        elif input=='/alarm_analyze':
            gocc_alarm_analyzer_whisker.analyze()
        elif input=='/schedule':
            gocc_dwell.query()
        elif input=='/schedule_all':
            gocc_dwell.printAll()
        elif input=='/skip_all':
            gocc_skip.printAll("SAVE")
        elif input =='/summary':
            summary.summary()
            print '"'+settings.ofname+'" successfully generated.' 
        elif input == '/occ_crawl':
            gocc_crawler.crawl()
            print '\nCrawl complete. Alarms have been sorted.'
        elif input =='/wo_crawl':
            wo_crawler.crawl()
        elif input =='/wo_query':
            wo_compiler.query() #testing only
        elif input=='/al_query':
            al_crawler.query()
        elif input == '/alarm_query':
            gocc_alarm.query()
        elif input == '/listing_crawl':
            al_crawler.crawl()
        elif input == '/pmd_query':
            pm_data.searchPMD()       
        elif input == '/cmd_query':
            cm_data.searchCMD() 
        elif input == '/settings':
            settings.prompt()
            print 'Severity filter set to ',settings.sev
            print 'Recurrence limit set to ',settings.filter_limit
            print 'Only consider working asset ',settings.working_asset_only
        elif input =='/rescan':
            print "\nScanning Files.. Please wait."
            al_compiler.scan()
            pm_compiler.scan()
            cm_compiler.scan()
            gocc_compiler.scan()
            print "\nScan Complete."
        elif input=='/expand':
            command_table.show()
        elif input=='/break':
            break
        elif(counter<3):
            counter +=1
            print 'Invalid command. Please retry.'
        else:
            break
    
    print "Shutting down ..."
    

if __name__ =="__main__":
    main()