# -*- coding: utf-8 -*-

class Tree:
    def __init__(self, hier, cargo, fullname=None):
        self.cargo=cargo
        self.fullname=fullname
        self.children=[]
        self.hierarchy=hier

        
    def add_child(self, obj):
        self.children.append(obj)