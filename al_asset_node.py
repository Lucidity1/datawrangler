# -*- coding: utf-8 -*-

class Asset:
    def __init__(self, asset_id, obj=None):
        self.asset_id=asset_id
        self.parent=obj
        
    def setParent(self,obj):
        self.parent=obj