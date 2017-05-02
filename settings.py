# -*- coding: utf-8 -*-
from collections import defaultdict
import gocc_rsstatus_node

def init():    
    global gocc
    gocc={}

    global power
    power={}
    
    global power_alarm
    power_alarm={}
    
    global alarm
    alarm={}
    
    global rsstatus
    rsstatus=defaultdict(lambda: gocc_rsstatus_node.RSStatus(None,None,None))
    
    global rsschedule
    rsschedule=defaultdict(lambda:None)
    
    global skips
    skips=defaultdict(lambda:None)
    
    global wo
    wo=defaultdict(lambda:None)
    
    global al
    al=defaultdict(lambda:None)
  
    global pmd_pmdid
    global pmd_dateandtime
    global pmd_trainno
    global pmd_carno
    global pmd_locationcode
    global pmd_metername
    global pmd_processid
    global pmd_paramid
    global pmd_pmdvalue
    global pmd_translatedvalue
    global pmd_conditionname
    global pmd_conditiondesciption
    
    global cmd_cmdid
    global cmd_faultdate
    global cmd_trainno
    global cmd_carno
    global cmd_locationcode
    global cmd_processid
    global cmd_eventid
    global cmd_eventname
    global cmd_eventdescription
    global cmd_priority
    global cmd_srnumber
    
    
    global pareto_limit
    pareto_limit=1000
    
    global all_pareto_limit
    all_pareto_limit=5000
    
    #printout scanning files..
    global scan_report
    scan_report=False
        
    global list_node
    list_node=[]
    
    global assets
    assets={}

    global fname_assetlisting
    fname_assetlisting=[]
    fname_assetlisting.append("raw/asset_listing/dtl_asset_listing.csv")
    
    global fname_pmd
    fname_pmd=[]
    fname_pmd.append("PMD/PMD-02Sep16.csv")
    
    global fname_cmd
    fname_cmd=[]
    fname_cmd.append("CMD/CMD-23Aug16.csv")
    
    global fname_gocc
    fname_gocc=[]
    
    '''
    fname_gocc.append("raw/events/GOCC/2016-08/events2016-08-01.csv")
    
    fname_gocc.append("raw/events/GOCC/2016-08/events2016-08-02.csv")
    
    fname_gocc.append("raw/events/GOCC/2016-08/events2016-08-03.csv")    
    
    fname_gocc.append("raw/events/GOCC/2016-08/events2016-08-04.csv")
        
    fname_gocc.append("raw/events/GOCC/2016-08/events2016-08-05.csv")    
    
    fname_gocc.append("raw/events/GOCC/2016-08/events2016-08-06.csv")
    fname_gocc.append("raw/events/GOCC/2016-08/events2016-08-07.csv")
    fname_gocc.append("raw/events/GOCC/2016-08/events2016-08-08.csv")
    fname_gocc.append("raw/events/GOCC/2016-08/events2016-08-09.csv")
    fname_gocc.append("raw/events/GOCC/2016-08/events2016-08-10.csv")
    fname_gocc.append("raw/events/GOCC/2016-08/events2016-08-11.csv")
    fname_gocc.append("raw/events/GOCC/2016-08/events2016-08-12.csv")
    fname_gocc.append("raw/events/GOCC/2016-08/events2016-08-13.csv")
    fname_gocc.append("raw/events/GOCC/2016-08/events2016-08-14.csv")
    fname_gocc.append("raw/events/GOCC/2016-08/events2016-08-15.csv")
    fname_gocc.append("raw/events/GOCC/2016-08/events2016-08-16.csv")
    fname_gocc.append("raw/events/GOCC/2016-08/events2016-08-17.csv")
    fname_gocc.append("raw/events/GOCC/2016-08/events2016-08-18.csv")
    fname_gocc.append("raw/events/GOCC/2016-08/events2016-08-19.csv")
    fname_gocc.append("raw/events/GOCC/2016-08/events2016-08-20.csv")
    fname_gocc.append("raw/events/GOCC/2016-08/events2016-08-21.csv")
    fname_gocc.append("raw/events/GOCC/2016-08/events2016-08-22.csv")
    fname_gocc.append("raw/events/GOCC/2016-08/events2016-08-23.csv")
    fname_gocc.append("raw/events/GOCC/2016-08/events2016-08-24.csv")
    fname_gocc.append("raw/events/GOCC/2016-08/events2016-08-25.csv")
    fname_gocc.append("raw/events/GOCC/2016-08/events2016-08-26.csv")
    fname_gocc.append("raw/events/GOCC/2016-08/events2016-08-27.csv")
    fname_gocc.append("raw/events/GOCC/2016-08/events2016-08-28.csv")
    fname_gocc.append("raw/events/GOCC/2016-08/events2016-08-29.csv")
    fname_gocc.append("raw/events/GOCC/2016-08/events2016-08-30.csv")
    
    fname_gocc.append("raw/events/GOCC/2016-08/events2016-08-31.csv")  
    
    fname_gocc.append("raw/events/GOCC/2016-09/events2016-09-01.csv")
    
    fname_gocc.append("raw/events/GOCC/2016-09/events2016-09-02.csv")
    fname_gocc.append("raw/events/GOCC/2016-09/events2016-09-03.csv")
    fname_gocc.append("raw/events/GOCC/2016-09/events2016-09-04.csv")
    fname_gocc.append("raw/events/GOCC/2016-09/events2016-09-05.csv")
    
    fname_gocc.append("raw/events/GOCC/2016-09/events2016-09-06.csv")
    fname_gocc.append("raw/events/GOCC/2016-09/events2016-09-07.csv")
    fname_gocc.append("raw/events/GOCC/2016-09/events2016-09-08.csv")
    fname_gocc.append("raw/events/GOCC/2016-09/events2016-09-09.csv")
    fname_gocc.append("raw/events/GOCC/2016-09/events2016-09-10.csv")
    fname_gocc.append("raw/events/GOCC/2016-09/events2016-09-11.csv")
    fname_gocc.append("raw/events/GOCC/2016-09/events2016-09-12.csv")
    fname_gocc.append("raw/events/GOCC/2016-09/events2016-09-13.csv")
    fname_gocc.append("raw/events/GOCC/2016-09/events2016-09-14.csv")
    fname_gocc.append("raw/events/GOCC/2016-09/events2016-09-15.csv")
    
    fname_gocc.append("raw/events/GOCC/2016-09/events2016-09-16.csv")
    fname_gocc.append("raw/events/GOCC/2016-09/events2016-09-17.csv")
    fname_gocc.append("raw/events/GOCC/2016-09/events2016-09-18.csv")
    fname_gocc.append("raw/events/GOCC/2016-09/events2016-09-19.csv")
    '''
    fname_gocc.append("raw/events/GOCC/2016-09/events2016-09-20.csv")
    '''
    fname_gocc.append("raw/events/GOCC/2016-09/events2016-09-21.csv")
    fname_gocc.append("raw/events/GOCC/2016-09/events2016-09-22.csv")
    fname_gocc.append("raw/events/GOCC/2016-09/events2016-09-23.csv")
    fname_gocc.append("raw/events/GOCC/2016-09/events2016-09-24.csv")    
    fname_gocc.append("raw/events/GOCC/2016-09/events2016-09-25.csv")
    fname_gocc.append("raw/events/GOCC/2016-09/events2016-09-26.csv")
    
    fname_gocc.append("raw/events/GOCC/2016-09/events2016-09-27.csv")
   
    fname_gocc.append("raw/events/GOCC/2016-09/events2016-09-28.csv")
    
    fname_gocc.append("raw/events/GOCC/2016-09/events2016-09-29.csv")
    
    fname_gocc.append("raw/events/GOCC/2016-09/events2016-09-30.csv")
    
    
    fname_gocc.append("raw/events/GOCC/2016-10/events2016-10-01.csv")
    fname_gocc.append("raw/events/GOCC/2016-10/events2016-10-02.csv")
    
    fname_gocc.append("raw/events/GOCC/2016-10/events2016-10-03.csv")
    
    fname_gocc.append("raw/events/GOCC/2016-10/events2016-10-04.csv")
    
    fname_gocc.append("raw/events/GOCC/2016-10/events2016-10-05.csv")
    fname_gocc.append("raw/events/GOCC/2016-10/events2016-10-06.csv")
    fname_gocc.append("raw/events/GOCC/2016-10/events2016-10-07.csv")
    fname_gocc.append("raw/events/GOCC/2016-10/events2016-10-08.csv")
    fname_gocc.append("raw/events/GOCC/2016-10/events2016-10-09.csv")
    fname_gocc.append("raw/events/GOCC/2016-10/events2016-10-10.csv")
    fname_gocc.append("raw/events/GOCC/2016-10/events2016-10-11.csv")
    fname_gocc.append("raw/events/GOCC/2016-10/events2016-10-12.csv")
    fname_gocc.append("raw/events/GOCC/2016-10/events2016-10-13.csv")
    fname_gocc.append("raw/events/GOCC/2016-10/events2016-10-14.csv")
    fname_gocc.append("raw/events/GOCC/2016-10/events2016-10-15.csv")
    fname_gocc.append("raw/events/GOCC/2016-10/events2016-10-16.csv")
    fname_gocc.append("raw/events/GOCC/2016-10/events2016-10-17.csv")
    fname_gocc.append("raw/events/GOCC/2016-10/events2016-10-18.csv")
    fname_gocc.append("raw/events/GOCC/2016-10/events2016-10-19.csv")
    fname_gocc.append("raw/events/GOCC/2016-10/events2016-10-20.csv")
    fname_gocc.append("raw/events/GOCC/2016-10/events2016-10-21.csv")
    fname_gocc.append("raw/events/GOCC/2016-10/events2016-10-22.csv")
    fname_gocc.append("raw/events/GOCC/2016-10/events2016-10-23.csv")
    fname_gocc.append("raw/events/GOCC/2016-10/events2016-10-24.csv")
    fname_gocc.append("raw/events/GOCC/2016-10/events2016-10-25.csv")
    fname_gocc.append("raw/events/GOCC/2016-10/events2016-10-26.csv")
    fname_gocc.append("raw/events/GOCC/2016-10/events2016-10-27.csv")
    fname_gocc.append("raw/events/GOCC/2016-10/events2016-10-28.csv")
    fname_gocc.append("raw/events/GOCC/2016-10/events2016-10-29.csv")
    fname_gocc.append("raw/events/GOCC/2016-10/events2016-10-30.csv")
    fname_gocc.append("raw/events/GOCC/2016-10/events2016-10-31.csv")
    fname_gocc.append("raw/events/GOCC/2016-11/events2016-11-01.csv")
    fname_gocc.append("raw/events/GOCC/2016-11/events2016-11-02.csv")
    fname_gocc.append("raw/events/GOCC/2016-11/events2016-11-03.csv")
    fname_gocc.append("raw/events/GOCC/2016-11/events2016-11-04.csv")
    fname_gocc.append("raw/events/GOCC/2016-11/events2016-11-05.csv")
    fname_gocc.append("raw/events/GOCC/2016-11/events2016-11-06.csv")
    fname_gocc.append("raw/events/GOCC/2016-11/events2016-11-07.csv")
    fname_gocc.append("raw/events/GOCC/2016-11/events2016-11-08.csv")
    fname_gocc.append("raw/events/GOCC/2016-11/events2016-11-09.csv")
    fname_gocc.append("raw/events/GOCC/2016-11/events2016-11-10.csv")
    fname_gocc.append("raw/events/GOCC/2016-11/events2016-11-11.csv")
    fname_gocc.append("raw/events/GOCC/2016-11/events2016-11-12.csv")
    fname_gocc.append("raw/events/GOCC/2016-11/events2016-11-13.csv")
    fname_gocc.append("raw/events/GOCC/2016-11/events2016-11-14.csv")
    fname_gocc.append("raw/events/GOCC/2016-11/events2016-11-15.csv")
    fname_gocc.append("raw/events/GOCC/2016-11/events2016-11-16.csv")
    fname_gocc.append("raw/events/GOCC/2016-11/events2016-11-17.csv")
    fname_gocc.append("raw/events/GOCC/2016-11/events2016-11-18.csv")
    fname_gocc.append("raw/events/GOCC/2016-11/events2016-11-19.csv")
    fname_gocc.append("raw/events/GOCC/2016-11/events2016-11-20.csv")
    fname_gocc.append("raw/events/GOCC/2016-11/events2016-11-21.csv")
    fname_gocc.append("raw/events/GOCC/2016-11/events2016-11-22.csv")
    fname_gocc.append("raw/events/GOCC/2016-11/events2016-11-23.csv")
    fname_gocc.append("raw/events/GOCC/2016-11/events2016-11-24.csv")
    fname_gocc.append("raw/events/GOCC/2016-11/events2016-11-25.csv")
    fname_gocc.append("raw/events/GOCC/2016-11/events2016-11-26.csv")
    fname_gocc.append("raw/events/GOCC/2016-11/events2016-11-27.csv")
    fname_gocc.append("raw/events/GOCC/2016-11/events2016-11-28.csv")
    fname_gocc.append("raw/events/GOCC/2016-11/events2016-11-29.csv")
    fname_gocc.append("raw/events/GOCC/2016-11/events2016-11-30.csv")
    '''
    
    global fname_wo
    fname_wo=[]
    
    fname_wo.append("raw/wo/JAN WOs.csv")
    fname_wo.append("raw/wo/FEB WOs.csv")
    fname_wo.append("raw/wo/MAR WOs.csv")
    
    fname_wo.append("raw/wo/APR WOs.csv")
    
    fname_wo.append("raw/wo/MAY WOs.csv")
    fname_wo.append("raw/wo/JUN WOs.csv")
    
    fname_wo.append("raw/wo/JUL WOs.csv")
    fname_wo.append("raw/wo/AUG WOs.csv")
    fname_wo.append("raw/wo/SEP WOs.csv")
    fname_wo.append("raw/wo/OCT WOs.csv")
    fname_wo.append("raw/wo/NOV WOs.csv")
    #fname_wo.append("raw/wo/SEP WOs.csv")
    
    
    global fname_power
    fname_power=[]
    fname_power.append("raw/compass_line/070715pow_lta.csv")
    
    
    
    global dtl_train
    global dtl_station
    global dtl_depot
    dtl_train=[]
    dtl_station=[]
    dtl_depot=[]
    
    global working_asset_only
    working_asset_only=False
    
    dtl_train.append("90010")
    
    dtl_train.append("90020")
    dtl_train.append("90030")   
    dtl_train.append("90040")
    dtl_train.append("90050")
    dtl_train.append("90060")
    dtl_train.append("90070")
    dtl_train.append("90080")
    dtl_train.append("90090")
    dtl_train.append("90100")    
    dtl_train.append("90110")
    dtl_train.append("90120")
    dtl_train.append("90130")
    dtl_train.append("90140")
    dtl_train.append("90150")
    dtl_train.append("90160")
    dtl_train.append("90170")
    dtl_train.append("90180")
    dtl_train.append("90190")
    dtl_train.append("90200")
    dtl_train.append("90210")
    dtl_train.append("90220")
    dtl_train.append("90230")
    dtl_train.append("90240")
    dtl_train.append("90250")
    dtl_train.append("90260")
    dtl_train.append("90270")
    dtl_train.append("90280")
    dtl_train.append("90290")
    dtl_train.append("90300")
    dtl_train.append("90310")
    dtl_train.append("90320")
    dtl_train.append("90330")
    dtl_train.append("90340")
    dtl_train.append("90350")
    dtl_train.append("90360")
    dtl_train.append("90370")
    dtl_train.append("90380")
    dtl_train.append("90390")
    dtl_train.append("90740")
    dtl_train.append("90750")
    dtl_train.append("90760")
    dtl_train.append("90770")
    dtl_train.append("90780")
    dtl_train.append("90790")

    dtl_station.append("DT01")
    dtl_station.append("DT02")
    dtl_station.append("DT03")

    dtl_station.append("DT05")
    dtl_station.append("DT06")
    dtl_station.append("DT07")
    dtl_station.append("DT08")
    dtl_station.append("DT09")
    dtl_station.append("DT10")
    dtl_station.append("DT11")
    dtl_station.append("DT12")
    dtl_station.append("DT13")
    dtl_station.append("DT14")
    dtl_station.append("DT15")
    dtl_station.append("DT16")
    dtl_station.append("DT17")
    dtl_station.append("DT18")
    dtl_station.append("DT19")
    
    dtl_depot.append("GBD")


    global ofname
    global ofname_listing
    global ofname_alarm_analyzer
    global ofname_schedule
    global ofname_skip
    global ofname_wo_crawler
    global ofname_power_64p
    global exclude
    global sev
    global filter_limit 
    
    ofname='output/summary.txt'
    ofname_listing='output/asset_listing.txt'
    ofname_alarm_analyzer='output/alarm_analyzer.txt'
    ofname_schedule='output/train_schedule.txt'
    ofname_skip='output/station_skip.txt'
    ofname_wo_crawler='output/wo_crawler.txt'
    ofname_power_64p='output/64p.txt'
    
    exclude = ['UNKNOWN', 'NORMAL','NOT DETECTED','NOT ACTIVATED', 'CLOSED', 'OK']
    sev=5
    filter_limit=0

    pmd_pmdid=[]
    pmd_dateandtime=[]
    pmd_trainno=[]
    pmd_carno=[]
    pmd_locationcode=[]
    pmd_metername=[]
    pmd_processid=[]
    pmd_paramid=[]
    pmd_pmdvalue=[]
    pmd_translatedvalue=[]
    pmd_conditionname=[]
    pmd_conditiondesciption=[]

    cmd_cmdid=[]
    cmd_faultdate=[]
    cmd_trainno=[]
    cmd_carno=[]
    cmd_locationcode=[]
    cmd_processid=[]
    cmd_eventid=[]
    cmd_eventname=[]
    cmd_eventdescription=[]
    cmd_priority=[]
    cmd_srnumber=[]

    global color_code
    color_code=[]
    #color_code.append('#53868B') #dodgerblue
    #color_code.append('#00BFFF') #dodgerblue
    color_code.append('#E78A61')#tangerine
    color_code.append('#00FFFF')#cyan
    color_code.append('#0000A0')#darkblue
    color_code.append('#2C3539')#gunmetal
    color_code.append('#2B1B17')#midnight
    color_code.append('#25383C')#darkslategrey
    color_code.append('#3D3C3A')#iridium
    color_code.append('#34282C')#charcoal
    color_code.append('#736F6E')#gray
    color_code.append('#B6B6B4')#graycloud
    color_code.append('#BCC6CC')#metallicsilver
    color_code.append('#98AFC7')#bluegray
    color_code.append('#616D7E')#jetgray
    color_code.append('#566D7E')#marbleblue
    color_code.append('#737CA1')#slateblue
    color_code.append('#4863A0')#steelblue
    color_code.append('#151B54')#midnightblue
    color_code.append('#000080')#navyblue
    color_code.append('#342D7E')#bluewhale
    color_code.append('#0041C2')#blueberryblue
    color_code.append('#1569C7')#blueeyes
    color_code.append('#736AFF')#lightslateblue
    color_code.append('#3090C7')#blueivy
    color_code.append('#95B9C7')#babyblue
    color_code.append('#3BB9FF')#deepskyblue
    color_code.append('#7FFFD4')#aquamarine
    color_code.append('#3EA99F')#lightseagreen
    color_code.append('#307D7E')#greenishblue
    color_code.append('#4E8975')#seagreen
    color_code.append('#728C00')#venomgreen
    color_code.append('#254117')#darkforestgreen
    color_code.append('#437C17')#seaweedgreen
    color_code.append('#7F525D')#dullpurple
    color_code.append('#FF00FF')#magenta
    color_code.append('#D4A017')#orangegold
    color_code.append('#C2B280')#sand
    color_code.append('#493D26')#mocha
    color_code.append('#E55451')#valentinered
    color_code.append('#C04000')#mahogany
    color_code.append('#810541')#maroon

    global cmd_table
    cmd_table=[\
        ["/summary", 'To generate report {Deprecated}'],\
        ["/listing_crawl", 'To generate asset listing tree. Output file will be generated.'],\
        ["/al_query", 'To query asset'],\
        ["/schedule", 'To search train schedule'],\
        ["/schedule_all", 'To print all train schedule'],\
        ["/skip_all", 'To print all station skips'],\
        ["/alarm_analyze", 'To analyze alarms'],\
        ["/occ_query", 'To search OCC event log by equipment and date'],\
        ["/occ_crawl", 'To generate OCC alarm data tables'],\
        ["/wo_crawl", 'To generate work orders data tables'],\
        ["/wo_query", 'To search work orders by WO number'],\
        ["/alarm_query", 'To search OCC alarms by equipment and date. Must have run /occ_crawl'],\
        ["/rsstatus_query", 'To search OCC RS status by RS NO. and date. Must have run /occ_crawl'],\
        ["/pmd_query", 'To search pmd log by equipment {Deprecated}'],\
        ["/cmd_query", 'To search cmd log by equipment {Deprecated}'],\
        ["/settings", 'To set global variable {Deprecated}'],\
        ["/rescan", 'To rescan files'],\
        ["/break", 'To terminate this program'],\
         ]
    
    global ns_lpu
    ns_lpu=[]
    ns_lpu.append('BBT')
    ns_lpu.append('BGB')
    ns_lpu.append('JPO')
    ns_lpu.append('CCK')
    ns_lpu.append('CKO')
    ns_lpu.append('YWT')
    ns_lpu.append('KDO')
    ns_lpu.append('KRJ')
    ns_lpu.append('MSL')
    ns_lpu.append('WDL')
    ns_lpu.append('ADM')
    ns_lpu.append('SBW')
    ns_lpu.append('CPO')
    ns_lpu.append('YIS')
    ns_lpu.append('YAO')
    ns_lpu.append('KTB')
    ns_lpu.append('SSO')
    ns_lpu.append('LKO')
    ns_lpu.append('YCK')
    ns_lpu.append('AKO')
    ns_lpu.append('AMK')
    ns_lpu.append('BDI')
    ns_lpu.append('BSH')
    ns_lpu.append('BSD')
    ns_lpu.append('BDL')
    ns_lpu.append('TAP')
    ns_lpu.append('NOV')
    ns_lpu.append('NEW')
    ns_lpu.append('ORC')
    ns_lpu.append('SOM')
    ns_lpu.append('DBG')
    ns_lpu.append('SFI')
    ns_lpu.append('CTH')
    ns_lpu.append('RFP')
    ns_lpu.append('MRB')
    ns_lpu.append('MSP')
    
    global ew_lpu
    ew_lpu=[]
    ew_lpu.append('JKN')
    ew_lpu.append('PNR')
    ew_lpu.append('BNL')
    ew_lpu.append('LKS')
    ew_lpu.append('CNG')
    ew_lpu.append('JUR')
    ew_lpu.append('SUO')
    ew_lpu.append('CLE')
    ew_lpu.append('CWO')
    ew_lpu.append('DVR')
    ew_lpu.append('BNI')
    ew_lpu.append('BNV')
    ew_lpu.append('COM')
    ew_lpu.append('QUE')
    ew_lpu.append('RDH')
    ew_lpu.append('DLO')
    ew_lpu.append('TIB')
    ew_lpu.append('OTP')
    ew_lpu.append('TPG')
    ew_lpu.append('RFP')
    ew_lpu.append('SFI')
    ew_lpu.append('OCC')
    ew_lpu.append('CTH')
    ew_lpu.append('BGS')
    ew_lpu.append('LVR')
    ew_lpu.append('KAL')
    ew_lpu.append('ALJ')
    ew_lpu.append('PYL')
    ew_lpu.append('YSI')
    ew_lpu.append('EUN')
    ew_lpu.append('KEM')
    ew_lpu.append('BDK')
    ew_lpu.append('TNM')
    ew_lpu.append('SBO')
    ew_lpu.append('SIM')
    ew_lpu.append('TAM')
    ew_lpu.append('PSR')
    ew_lpu.append('XPO')
    ew_lpu.append('CGO')
    ew_lpu.append('CGA')
    
    
         
def resetSev(value):
    global sev
    sev= value
    
def setFilterLimit(value):
    global filter_limit
    filter_limit=value

def setWorkingAssetOnly(value):
    global working_asset_only
    working_asset_only=value

def prompt():
    while (True):
        try:
            value = int(raw_input('PROMPT: Enter severity filter value (1-5). Severity code more than the input value will be filtered off.\n '))
        except ValueError:
            print("Input must be an integer. Retry.")
            continue
        else:
            if(1<=value<=5):
                break 
            else:
                print("Input must be between 1 to 5. Retry")
                continue
    resetSev(value)
    
    while (True):
        try:
            value = int(raw_input('PROMPT: Enter recurrence limit. Recurrence less than the input value will be filtered off.\n '))
        except ValueError:
            print("Input must be an integer. Retry.")
            continue
        else:
            break
    setFilterLimit(value)
    
    while (True):
        value = (raw_input('Prompt: Only consider working asset? (y/n)\n'))
        value=value.lower()
        if not (value == 'y' or value == 'n'):
            print("Invalid input. Retry.")
            continue
        else:
            if value=='y':
                setWorkingAssetOnly(True)
                break
            elif value == 'n':
                setWorkingAssetOnly(False)
                break
        