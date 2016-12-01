from lib.ibs_logger import Logger
import ibs_agi
import sys
import traceback


def toLog(_str): 
    if "logger" not in globals():
        global logger
        logger=Logger(ibs_agi.getConfig().getValue("log_file"))
    logger.write("%s:%s"%(ibs_agi.getConfig().getValue("username"),_str))

def getExceptionText():
    """
        create and return text of last exception
    """
    (_type,value,tback)=sys.exc_info()
    return "".join(traceback.format_exception(_type, value, tback))

def logException(extra_str=""):
    err_text=getExceptionText()
    toLog(extra_str+"\n"+err_text)

class IBSException(Exception):
    pass