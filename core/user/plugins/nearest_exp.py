from core.user import user_main
from core.lib.date import *
import time

def init():
    user_main.getAttributeManager().registerHandler(None,[],[],[],[calcNearestExpDate])


def calcNearestExpDate(_id,_type,raw_attrs,parsed_attrs,date_type):
    if _type!="user":
        return
        
    nearest_exp_date = defs.MAXLONG
    group_obj = user_main.getUserPool().getUserByID(_id).getBasicUser().getGroupObj()
    
    if "first_login" in raw_attrs:
        if "rel_exp_date" in raw_attrs:
            nearest_exp_date = int(raw_attrs["first_login"]) + int(raw_attrs["rel_exp_date"])

        elif group_obj.hasAttr("rel_exp_date"):
            nearest_exp_date = int(raw_attrs["first_login"]) + int(group_obj.getAttr("rel_exp_date"))

    if "abs_exp_date" in raw_attrs:
        nearest_exp_date = min(nearest_exp_date , int(raw_attrs["abs_exp_date"]) )
            
    elif group_obj.hasAttr("abs_exp_date"):
        nearest_exp_date = min(nearest_exp_date , int(group_obj.getAttr("abs_exp_date")) )

    if nearest_exp_date != defs.MAXLONG:
        parsed_attrs["nearest_exp_date"]=AbsDateFromEpoch(nearest_exp_date).getDate(date_type)
        parsed_attrs["nearest_exp_date_epoch"]=nearest_exp_date
        parsed_attrs["time_to_nearest_exp_date"]=nearest_exp_date - time.time()