# -*- coding: utf-8 -*-
import settings
import prettytable as pt

     
def show ():
    x=pt.PrettyTable(["Command","Description"])
    for item in settings.cmd_table:
        x.add_row([item[0],item[1]])
    print x