# -*- coding: utf-8 -*-
import prettytable as pt

class Dwell:
    def __init__(self, loc_id, direction, station,time_start,time_end):
        self.loc_id=loc_id
        self.direction=direction
        self.station=station
        self.time_start=time_start
        self.time_end=time_end
        
        self.dwell_time=None
        
    
    def calDwellTime(self):
        try:
            self.dwell_time=self.time_end-self.time_start
        except:
            pass

    def __str__(self):
        x=pt.PrettyTable(["RS no.", "station", "direction", "dwell time", "open_time"])
        x.add_row([self.loc_id,self.station, self.direction, self.dwell_time, self.time_start])
        return x.get_string()
    
    def get_string(self):
        return [self.loc_id,self.station, self.direction, self.dwell_time, self.time_start]