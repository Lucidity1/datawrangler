# -*- coding: utf-8 -*-
import settings

def writeFile(content):
    with open(settings.ofname_skip, 'a') as fl:
        fl.write(content)

def printAll(option="PRINT"):
    count=0
    if option=="PRINT":
        for skip in settings.skips.iteritems():
            print skip
            count+=1
        if count==0:
            print 'No station skip detected within the time period.'

    if option=="SAVE":
        with open(settings.ofname_skip, 'w'):
            print 'Output file "'+settings.ofname_skip+'" created in root directory.'
    
        for skip in settings.skips.iteritems():
            writeFile(skip)
            count+=1
        if count==0:
            writeFile('No station skip detected within the time period.')
