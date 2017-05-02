# -*- coding: utf-8 -*-

import settings
import al_tree
import prettytable as pt
import print_progress as pp

global display
global x

def writeFile(content):
    with open(settings.ofname_listing, 'a') as fl:
        fl.write(content)
        
def exist(temp):
    check=True
    have_all=True
    #check if all components in temp exists
    i=temp[-1]
    if not any(i==node.cargo for node in settings.list_node):
        #print i,' does not exist'
        have_all = False
        check = False
    #else:
        #print i,' exists'
    #check if they are in the proper order
    if have_all==True:
        for index, item in enumerate(temp[:-1]):
            if not any(temp[index+1] == child.cargo for child in nodeSearch(item).children):
                check=False
                #print 'but second check fail, as multiple ',item,' exists'
    return check

####!!!Warning! Logic Error - To improve at later time
def nodeSearch(search):
    for node in settings.list_node:
        if node.cargo==search:
            return node
        
        
def generateEqmTree():
    settings.list_node=[]
    count=0
    total=len(settings.assetlisting_equipmenttype)
    #print 'Crawling asset listing, please wait...'
    for ix, eqm in enumerate(settings.assetlisting_equipmenttype):
        
        #print '\nScanning line'
        temp = eqm.split("/")
        #print temp
        level=[]
        for index, item in enumerate(temp):
            #print 'Checking: ',temp[:index+1]
            item.replace(' ','')
            if not item=='':
                if index==0:
                    if not exist(temp[:index+1]):
                        #print 'Item does not exist, creating node. Index=',index
                        #create node
                        if index==len(temp)-1:
                            holder=settings.assetlisting_description[ix]
                        else:
                            holder=None
                        #print 'Holder= ',holder
                        node=al_tree.Tree(index,item,holder)
                        level.append(node)
                        settings.list_node.append(node)
                    else:
                        #print 'Item exists, ignoring.. Index=',index
                        level.append(nodeSearch(temp[index]))
                else:
                    if not exist(temp[:index+1]):
                        #print 'Item does not exist, creating node. Index=',index
                        #create node
                        if index==len(temp)-1:
                            holder=settings.assetlisting_description[ix]
                        else:
                            holder=None
                        #print 'Holder= ',holder
                        node=al_tree.Tree(index,item,holder)
                        #print level
                        level[index-1].add_child(node)
                        level.append(node)
                        settings.list_node.append(node)
                    else:
                        #print 'Item exists, ignoring.. Index=',index
                        level.append(nodeSearch(temp[index]))
        count+=1
        if(count%1000==0  or count/total>0.98):
            pp.printProgress(count,total, prefix='Crawling asset Listing:', suffix='Complete', barLength=10)
        
def printNode(search):
    tab='-'
    for node in settings.list_node:
        if node.cargo==search:
            print tab+node.cargo
            for child in node.children:
                print 2*tab+child.cargo
    
def printSubTree(node,lvl):
    global display
    global x
    if node==None:return
    #print display+'\t\t'+lvl*tab+node.cargo
    x.add_row([display, node.cargo,node.fullname])
    remember=display
    number=1
    lvl=lvl+1
    for child in node.children:
        display=display+'.'+str(number)
        printSubTree(child, lvl)
        number=number+1
        display=remember
        #print 'Global Display set as ',display
        
def printTree():
    with open(settings.ofname_listing, 'w'):
        print 'Output file "'+settings.ofname_listing+'" created in root directory.'
    global display
    global x
    ancestor=[]
    children_list=[]
    print '\nGenerating asset listing table. Please wait...'
    for node in settings.list_node:
        for child in node.children:
            children_list.append(child.cargo)
    for node in settings.list_node:
        if not any (node.cargo == child for child in children_list):
            ancestor.append(node)
    number=1    
    for node in ancestor:
        x=pt.PrettyTable(["S\N","Equipment", "Full name"])
        display=str(number)
        printSubTree(node, 0)
        number=number+1
        
        #print x
        writeFile(x.get_string())
        writeFile('\n')