from core.lib.general import *
from core.errors import errorText
from core.ibs_exceptions import *
from core.lib.jalali import *
import time,re

def dbTimeFromEpoch(epoch_time):
    return time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(epoch_time))

#############################33
def cur_day_of_week():
    return time.localtime()[6]
    
###############################
def secondsFromMorning(_time=0):
    """
        return number of seconds from 00:00:00 of today
    """
    if _time:
        tm=time.localtime(_time)
    else:
        tm=time.localtime()
    return tm[3]*3600+tm[4]*60+tm[5] # elapsed seconds from 00:00:00 of today


#################################
class Time:
    """
        Time class provoid method to handle time types
    """
    def __init__(self,time_str):
        """
            time_str(string): string representing time. it may be not fully described time 
                              ex. 12, 12:3, 12:30:12 are valid inputs
        
            This method may raise GeneralException on bad time_strs
            Genrated Exceptions doesn't containg key, as described in errors.errorText  
        """
        self.time_str=time_str
        (self.formatted_time,self.hour,self.minute,self.second)=self.__formatTime(time_str)


    def __cmp__(self,time_obj):
        return cmp(self.getSecondsFromMorning(),time_obj.getSecondsFromMorning())

    def __formatTime(self,time_str):
        """
            check if time_str is valid and complete it if necessary
            for ex. it will change 12:30 to 12:30:00 and 12 to 12:00:00
            raise an general exception on error
            return completed time_str on success
        """
        time_str=self.__completeTime(time_str)
        (hour,minute,second)=map(int,time_str.split(":"))
        if hour>24 or hour<0 or minute>60 or minute<0 or second>60 or second<0:
            raise GeneralException(errorText("GENERAL","TIME_OUT_OF_RANGE"))
        return (time_str,hour,minute,second)

    def __completeTime(self,time_str):
        if time_str.startswith("24"):
            time_str="23:59:59"
        elif re.match("^[0-9]{1,2}$",time_str):
            time_str="%s:00:00"%time_str
        elif re.match("^[0-9]{1,2}:[0-9]{1,2}$",time_str):
            time_str="%s:00"%time_str
        elif re.match("^[0-9]{1,2}:[0-9]{1,2}:[0-9]{1,2}$",time_str):
            pass
        else:
            raise GeneralException(errorText("GENERAL","INVALID_TIME_STRING")%time_str)

        return time_str

    def getSecondsFromMorning(self):
        return self.hour*3600+self.minute*60+self.second

    def getFormattedTime(self):
        return self.formatted_time


############################################
radius_time_parse_pattern=re.compile("[\.\*]?(\d+:\d+:\d+)\.\d+ (\w+ \w+ \w+ \d+ \d+)")
def getEpochFromRadiusTime(rad_time):
    """
        return epoch from radius time eg. 04:34:58.000 IRDT Thu Apr 14 2005
    """

    match_obj = radius_time_parse_pattern.match(rad_time)
    if match_obj == None:
        raise IBSError(errorText("GENERAL","INVALID_RADIUS_TIME")%rad_time)

    (_time,date) = match_obj.groups()
    
    #daylight saving is auto detemined
    time_tuple = time.strptime("%s %s" % (_time,date), "%H:%M:%S %Z %a %b %d %Y" ) 
    
    
    return time.mktime( time_tuple )
##############################################
def getGregorianNextMonthEpoch():
    """
        return epoch date for start of next month
    """
    year,month = time.localtime()[:2]
    month += 1 #python mktime nows how to handle month>11
    return time.mktime((year,month,1,0,0,0,0,0,-1))

def getJalaliNextMonthEpoch():
    """
        return epoch date for start of next jalali month
    """
    gyear,gmonth,gday = time.localtime()[:3]
    gtoj = GregorianToJalali(gyear, gmonth , gday)
    jyear, jmonth, jday = gtoj.getJalaliList()
    jmonth += 1
    if jmonth > 12:
        jyear += 1
        jmonth = 1
    
    jtog = JalaliToGregorian(jyear, jmonth, 1)
    year, month, day = jtog.getGregorianList()
    return time.mktime((year,month,day,0,0,0,0,0,-1))


def formatDuration(duration_seconds):
    """
        format seconds in duration format Hours:Minutes:Seconds
    """
    _list = []
    for i in range(2):
        _list.append( duration_seconds % 60 )
        duration_seconds /= 60
    _list.append( duration_seconds )
    return "%02d:%02d:%02d"%(_list[2],_list[1],_list[0])

#************************** NOT TESTED

def dbTimeToEpoch(dbTime):
    return time.mktime(dbTimeToList(dbTime))

def dbTimeToList(dbTime):
    """
    BROKEN
    """
    dot=dbTime.find(".")
    if dot ==-1:
        plus=dbTime.find("+") #old postgresqls date representation
        if plus==-1:
            dot=len(dbTime)
        else:
            dot=plus
    
    try:
        ret=list(time.strptime(dbTime[:dot],"%Y-%m-%d %H:%M:%S"))
        ret[8]=-1
        return ret
    except:
        raise GeneralException("Invalid dbTime: " + str(dbTime))
        

def getEpochTimeFromHourOfDay(hour,_min=0,sec=0,dayToAdd=0):
    tm=list(time.localtime())
    tm[3]=hour
    tm[4]=_min
    tm[5]=sec
    tm[2]+=dayToAdd
    
    return time.mktime(tm)

def epochTimeFromRadiusTime(rad_time):
    sp=rad_time.split()
    if sp[0].startswith('.') or sp[0].startswith('*'):
        sp[0]=sp[0][1:]
    formatted_time=sp[5]+ " " + sp[3] + " " + sp[4] + " " + sp[0][:sp[0].find('.')]

    time_list=list(time.strptime(formatted_time,'%Y %b %d %H:%M:%S'))
    time_list[8]=-1 #daylight saving flag
    epoch=time.mktime(time_list)
    return epoch

def epochTimeFromRadiusUTCTime(rad_time):
    return epochTimeFromRadiusTime(rad_time)-time.timezone

def getDurationInSec(duration,unit):
    duration=integer(duration)
    if unit=="seconds":
        return duration
    elif unit=="minutes":
        return duration*60
    elif unit=="hours":
        return duration*3600
    elif unit=="days":
        return duration*3600*24
    else:
        raise GeneralException("Invalid duration unit %s"%unit)

    