from core.errors import errorText
from core.lib.general import *

def checkFromTo(_from,to):
        if not isInt(_from) or _from<0:
            raise GeneralException(errorText("GENERAL","FROM_VALUE_INVALID")%_from)

        if not isInt(to) or to<0 or to>1024*1024*50:
            raise GeneralException(errorText("GENERAL","TO_VALUE_INVALID")%to)
        
        if _from>to or to-_from>3000:
            raise GeneralException(errorText("GENERAL","TO_VALUE_INVALID")%to)


def fixConditionsDic(conds):
    """
        fix conditions dictionary, convert dictionary members to lists, if they were lists originally
        some implementions (ex. php) convert arrays to python dics instead of lists, this method fix em by
        converting them to lists again
    """ 
    for key in conds:
        val=conds[key]
        if type(val)==types.DictType:
            conds[key]=fixXMLRPCList(val)
    return conds

    