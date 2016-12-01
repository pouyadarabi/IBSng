from core.ibs_exceptions import *
from core.lib.date import *

import time
import re

class LogConsole:
    LOG_BUFFER_SIZE = 200 #number of log lines kept in buffer
    capitalize_pattern = re.compile("\s[a-z]|^[a-z]")
    
    def __init__(self):
        self.__buffer = [] #(epoch_time, username, action, message)


    ####################################

    def __generateAVPairsFromRasMsg(self, ras_msg, attr_names):
        """
            Generate a well formatted AVPair from attributes that name is in attr_names
            attr_names(list): list of interested attribute names
        """
        avpairs = []
    
        for attr_name in ras_msg.getAttrs():
            if attr_name in attr_names:
                avpairs.append((self.__capitalize(attr_name.replace("_"," ")), ras_msg[attr_name]))

        return avpairs + self.__getCommonElements(ras_msg)


    def __getCommonElements(self, ras_msg):
        """
            return a list that contains common elements of each log line
        """
        return [("Ras", ras_msg.getRasObj().getRasDesc()), 
                ("ID", "(%s,%s)"%(ras_msg["unique_id"], ras_msg.getUniqueIDValue()))]
                
    def __capitalize(self, _str):
        """
            Capitalize first letter of all words in _str
        """
        return self.capitalize_pattern.sub(lambda x:x.group().upper(), _str)
    
    def __getRasMsgAction(self, ras_msg):
        """
            retrieve ,format and return action of ras_msg
        """
        return self.__capitalize(ras_msg.getAction().replace("_"," ").lower())

    def __getUsernameFromRasMsg(self, ras_msg):
        return ras_msg.getUserRepr()
    
    ###################################
    
    def logAuthRasMsg(self, ras_msg):
        """
            log an auth* RasMsg to console
        """
        self.log(self.__getUsernameFromRasMsg(ras_msg), 
                 self.__getRasMsgAction(ras_msg), 
                 [("Status","Try")] + self.__generateAuthMessage(ras_msg))

    def __generateAuthMessage(self, ras_msg):
        return self.__generateAVPairsFromRasMsg(ras_msg, ["mac", "caller_id", "station_ip", "called_number"])

    #######################################

    def logAuthRasMsgSuccess(self, ras_msg):
        """
            log an auth* RasMsg to console while result was succesful
        """
        self.log(self.__getUsernameFromRasMsg(ras_msg), 
                 self.__getRasMsgAction(ras_msg), 
                 [("Status","Successful")] + self.__getCommonElements(ras_msg))

    ########################################

    def logAuthRasMsgFailure(self, ras_msg, err_obj):
        """
            log an auth* RasMsg to console while result was failure
            err_obj(IBSError Instance): error that prevented this user from auth
        """
        self.log(self.__getUsernameFromRasMsg(ras_msg), 
                 self.__getRasMsgAction(ras_msg), 
                 [("Status","Failure"), ("Reason",err_obj.getErrorText())] + self.__getCommonElements(ras_msg) )

    #######################################

    def logStopRasMsg(self, ras_msg):
        self.log(self.__getUsernameFromRasMsg(ras_msg), 
                 self.__getRasMsgAction(ras_msg), 
                 self.__getCommonElements(ras_msg))

    def logUpdateRasMsg(self, ras_msg):
        pass

    #######################################3

    def log(self, username, action, avpairs):
        """
            log actions and message to console

            username(str): username of ras_msg. Maybe user_id: <user_id> in case username is not available
            action(str): ras message action
            avpairs(str): list of tuples in format [(attr_name,attr_value)]
            
        """
        message = self.__generateMessageFromAVPairs(avpairs)
        toLog("%s: %s %s"%(username, action, message), LOG_CONSOLE)
        self.__addToBuffer(username, action, avpairs, time.time())

    def __generateMessageFromAVPairs(self, avpairs):
        message = []
        for name, value in avpairs:
            message.append("%s:%s"%(name, value))
        
        return ", ".join(message)

    def __addToBuffer(self, username, action, avpairs, _time):
        if len(self.__buffer) > self.LOG_BUFFER_SIZE:
            self.__buffer.pop(0)
        
        self.__buffer.append((_time, username, action, avpairs))


    #######################################
    def getBuffer(self):
        return self.__buffer

    def getBufferFormatted(self, date_type):
        """
            return buffer as list of tuples in format (epoch_time, formatted_time, username, action, message)
        """
        formatted_buffer = []
        for _time, username, action, avpairs in self.getBuffer():
            formatted_buffer.append((_time, 
                                     AbsDateFromEpoch(_time).getDate(date_type), 
                                     username, 
                                     action, 
                                     avpairs))
        
        return formatted_buffer
