def depositLog(dict): #incomplete
    query="select admin_id,to_admin_id,credit,paid_money,remote_addr,change_time from admin_deposit_log"
    cond=""
    if "admin_id" in dict:
            cond+="admin_id="+str(integer(dict["admin_id"]))+" and "

    if "to_admin_id" in dict:
        cond+="to_admin_id="+str(integer(dict["to_admin_id"]))+" and "

    if "admin" in dict:
        cond+="admin_id="+str(username2id(dict["admin"]))+" and "


    if "to_admin" in dict:
        cond+="to_admin_id="+str(username2id(dict["to_admin"]))+" and "


    if "fromTime" in dict and "fromType" in dict:
        timeCond=timeCondition(dict["fromTime"],dict["fromType"])
        cond+="change_time " + timeCond + " and "
        
    if "toTime" in dict and "toType" in dict:
        timeCond=timeCondition(dict["toTime"],dict["toType"])
        cond+="change_time " + timeCond + " and "

    if cond!="":
        query+=" where " + cond[0:-4]
        
    if "from" in dict:
        _from=integer(dict["from"])
        query+=" offset "+str(_from)
    else:
        _from=0

    if "to" in dict:
        to=integer(dict["to"])
        if to>_from:
            query+=" limit "+str(to-_from)

    return db_main.getHandle().selectQuery(query)

def adminReport(adminObj,conds):
    if "date_from" in conds and "date_from_type" in conds:
        date_from_cond=timeCondition(conds["date_from"],conds["date_from_type"])
    else:
        date_from_cond=None
    
    if "date_to" in conds and "date_to_type" in conds:
        date_to_cond=timeCondition(conds["date_to"],conds["date_to_type"])
    else:
        date_to_cond=None

    if "credit_consume" not in conds and "deposit_changes" not in conds:
        raise generalException("adminReport: Nothing to report")
    

    timeConditions=""
    if date_from_cond!=None:
        timeConditions+=" change_time " + date_from_cond + " and " 
    if date_to_cond!=None:
        timeConditions+=" change_time " + date_to_cond + " and "
    if timeConditions!="":
        timeConditions=" and " + timeConditions[:-4] 


    if "credit_consume" in conds:
        event=""
        if "ADD_USER" in conds:
            event+="event='ADD_USER' or "
        if "CREDIT_CHANGE" in conds:
            event+="event='CREDIT_CHANGE' or "
        if "DEL_USER" in conds:
            event+="event='DEL_USER' or "
        if "ADD_VOIP_USER" in conds:
            event+="event='ADD_VOIP_USER' or "
        if "VOIP_CREDIT_CHANGE" in conds:
            event+="event='VOIP_CREDIT_CHANGE' or "
        if "DEL_VOIP_USER" in conds:
            event+="event='DEL_VOIP_USER' or "
        if event=="":
            raise generalException("adminReport: no event choosed for admin log")
        event=" and ("+event[:-3]+")" + timeConditions

        condition=timeConditions + event        
        
        credits=db_main.getHandle().selectQuery("select extract(epoch from change_time) as change_time_e,change_time,username,admin_id,event,credit,paid_money,remote_addr,comment from credit_log where admin_id=%s %s order by change_time asc" 
        % (adminObj.admin_id,condition))
        

    if "deposit_changes" in conds:
        deposits=db_main.getHandle().selectQuery("select extract(epoch from change_time) as change_time_e,change_time,admin_id,credit,paid_money,remote_addr,comment from admin_deposit_log where to_admin_id = %s %s " 
        %(adminObj.admin_id,timeConditions))

    if "credit_consume" in conds and "deposit_changes" not in conds:
        return credits

    if "credit_consume" not in conds and "deposit_changes" in conds:
        return deposits
    
    if "credit_consume" not in conds and "deposit_changes" in conds:
        return deposits

    return reportlib.mergeLists(credits,deposits,"change_time_e","change_time_e")
