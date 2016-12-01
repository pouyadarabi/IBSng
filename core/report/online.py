from core.user import user_main
from core.ras import ras_main
from core.ibs_exceptions import *
from core.errors import errorText
from core.lib.sort import SortedList
from core.lib.date import *

def getFormattedOnlineUsers(date_type, onlines_filter):
    """
        return a list of online user dics. format is (normal_list, voip_list)
        return value is a tuple of lists to be sortable
    """
    onlines_dic=user_main.getOnline().getOnlineUsersByRas()
    normal_onlines=[]
    voip_onlines=[]
    for (ras_id,unique_id) in onlines_dic:
        user_obj=onlines_dic[(ras_id,unique_id)]
        try:
                instance = user_obj.getInstanceFromUniqueID(ras_id,unique_id)
                if instance == None: #eh?
                    continue
                
                #continue if we are not intreseted in this instance
                if not onlines_filter.filter(user_obj, instance):
                    continue
                
                instance_info=user_obj.getInstanceInfo(instance)
                report_dic={"user_id":user_obj.getUserID(),
                         "service":user_obj.getType(),
                         "ras_ip":ras_main.getLoader().getRasByID(instance_info["ras_id"]).getRasIP(),
                         "ras_description":ras_main.getLoader().getRasByID(instance_info["ras_id"]).getRasDesc(),
                         "unique_id":instance_info["unique_id"],
                         "unique_id_val":instance_info["unique_id_val"],
                         "login_time":AbsDateFromEpoch(user_obj.getTypeObj().getLoginTime(instance)).getDate(date_type),
                         "login_time_epoch":user_obj.getTypeObj().getLoginTime(instance),
                         "duration_secs":time.time()-user_obj.getTypeObj().getLoginTime(instance),
                         "attrs":instance_info["attrs"],
                         "owner_id":user_obj.getLoadedUser().getBasicUser().getOwnerObj().getAdminID(),
                         "owner_name":user_obj.getLoadedUser().getBasicUser().getOwnerObj().getUsername(),
                         "current_credit":user_obj.calcCurrentCredit(),
                         "group_name":user_obj.getLoadedUser().getBasicUser().getGroupObj().getGroupName()
                         }
                report_dic.update(user_obj.getTypeObj().getOnlineReportDic(instance))

                if user_obj.getType() == "VoIP":
                    voip_onlines.append(report_dic)
                else:
                    normal_onlines.append(report_dic)
        except:
                logException(LOG_DEBUG)
                pass

    return (normal_onlines, voip_onlines)

def sortOnlineUsers(normal_onlines, voip_onlines, normal_sort_by, voip_sort_by):
    """
        sort online normal_onlines and voip_onlines, based on normal_sort_by and voip_sort_by
        normal_onlines(list of dics): list of internet onlines returned by getFormattedOnlineUsers
        voip_onlines(list of dics): list of internet onlines returned by getFormattedOnlineUsers
        normal_sort_by(list): list in format [sort_by,desc]
        voip_sort_by(list): list in format [sort_by,desc]
        
        if sort_by is invalid or empty, default "login_time_epoch" is used
        if sort_by starts with attrs it means we should sort by one of instance attributes
    """
    normal_sort_by_list=["user_id","normal_username","login_time_epoch","duration_secs","ras_description",
                         "ras_ip","owner_name","unique_id_val","current_credit","group_name",
                         "attrs_remote_ip","in_bytes","out_bytes","in_rate",
                         "out_rate","attrs_mac","attrs_station_ip","attrs_caller_id"]

    voip_sort_by_list=["user_id","voip_username","login_time_epoch","duration_secs","ras_ip","ras_description",
                       "owner_name","unique_id_val","current_credit","called_number",
                       "prefix_name","group_name","attrs_caller_id","attrs_caller_ip","attrs_called_ip"]

    return (_sortOnlines(normal_onlines, normal_sort_by[0], normal_sort_by[1], normal_sort_by_list),
            _sortOnlines(voip_onlines, voip_sort_by[0], voip_sort_by[1], voip_sort_by_list))

def _sortOnlines(list, sort_by, desc, valid_sortbys):
    """
        sort "list" by post text of sort_by and desc.
        sort_by should be in valid_sortbys or default will be chosen
    """
    if sort_by in ("","login_time"):
        sort_by="login_time_epoch"
    elif sort_by not in valid_sortbys:
        toLog("SortOnlines: Invalid sort by %s %s"%(sort_by,valid_sortbys),LOG_DEBUG)
        sort_by="login_time_epoch"

    sorted_list=SortedList(list)
    if sort_by.startswith("attrs_"):
        sort_by_post_text='["attrs"]["%s"]'%sort_by[6:]
        sorted_list.sortByPostText(sort_by_post_text,desc)
    else:
        sorted_list.sortByValueDicKey(sort_by, desc)
        
    return sorted_list.getList()