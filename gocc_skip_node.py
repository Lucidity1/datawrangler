# -*- coding: utf-8 -*-
import gocc_dwell as gd


class Skip:
    def __init__(self, loc_id, time, schedule_row_index):
        self.loc_id=loc_id
        self.time=time
        self.schedule_row_index
    

    def __str__(self):
        print 'Skip Station detected on train ',self.loc,' at ', self.time
        gd.printTrip(self.loc,self.time.date(),self.schedule_row_index)
    