def depositLog(dict): #incomplete
    query="select admin_id,to_admin_id,credit,paid_money,remote_addr,change_time from admin_deposit_log"
    cond=""
    if dict.has_key("admin_id"):
            cond+="admin_id="+str(integer(dict["admin_id"]))+" and "

    if dict.has_key("to_admin_id"):
        cond+="to_admin_id="+str(integer(dict["to_admin_id"]))+" and "

    if dict.has_key("admin"):
        cond+="admin_id="+str(username2id(dict["admin"]))+" and "


    if dict.has_key("to_admin"):
        cond+="to_admin_id="+str(username2id(dict["to_admin"]))+" and "


    if dict.has_key("fromTime") and dict.has_key("fromType"):
        timeCond=timeCondition(dict["fromTime"],dict["fromType"])
        cond+="change_time " + timeCond + " and "
        
    if dict.has_key("toTime") and dict.has_key("toType"):
        timeCond=timeCondition(dict["toTime"],dict["toType"])
        cond+="change_time " + timeCond + " and "

    if cond!="":
        query+=" where " + cond[0:-4]
        
    if dict.has_key("from"):
        _from=integer(dict["from"])
        query+=" offset "+str(_from)
    else:
        _from=0

    if dict.has_key("to"):
        to=integer(dict["to"])
        if to>_from:
            query+=" limit "+str(to-_from)

    return db_main.getHandle().selectQuery(query)

def adminReport(adminObj,conds):
    if conds.has_key("date_from") and conds.has_key("date_from_type"):
        date_from_cond=timeCondition(conds["date_from"],conds["date_from_type"])
    else:
        date_from_cond=None
    
    if conds.has_key("date_to") and conds.has_key("date_to_type"):
        date_to_cond=timeCondition(conds["date_to"],conds["date_to_type"])
    else:
        date_to_cond=None

    if not conds.has_key("credit_consume") and not conds.has_key("deposit_changes"):
        raise generalException("adminReport: Nothing to report")
    

    timeConditions=""
    if date_from_cond!=None:
        timeConditions+=" change_time " + date_from_cond + " and " 
    if date_to_cond!=None:
        timeConditions+=" change_time " + date_to_cond + " and "
    if timeConditions!="":
        timeConditions=" and " + timeConditions[:-4] 


    if conds.has_key("credit_consume"):
        event=""
        if conds.has_key("ADD_USER"):
            event+="event='ADD_USER' or "
        if conds.has_key("CREDIT_CHANGE"):
            event+="event='CREDIT_CHANGE' or "
        if conds.has_key("DEL_USER"):
            event+="event='DEL_USER' or "
        if conds.has_key("ADD_VOIP_USER"):
            event+="event='ADD_VOIP_USER' or "
        if conds.has_key("VOIP_CREDIT_CHANGE"):
            event+="event='VOIP_CREDIT_CHANGE' or "
        if conds.has_key("DEL_VOIP_USER"):
            event+="event='DEL_VOIP_USER' or "
        if event=="":
            raise generalException("adminReport: no event choosed for admin log")
        event=" and ("+event[:-3]+")" + timeConditions

        condition=timeConditions + event        
        
        credits=db_main.getHandle().selectQuery("select extract(epoch from change_time) as change_time_e,change_time,username,admin_id,event,credit,paid_money,remote_addr,comment from credit_log where admin_id=%s %s order by change_time asc" 
        % (adminObj.admin_id,condition))
        

    if conds.has_key("deposit_changes"):
        deposits=db_main.getHandle().selectQuery("select extract(epoch from change_time) as change_time_e,change_time,admin_id,credit,paid_money,remote_addr,comment from admin_deposit_log where to_admin_id = %s %s " 
        %(adminObj.admin_id,timeConditions))

    if conds.has_key("credit_consume") and not conds.has_key("deposit_changes"):
        return credits

    if not conds.has_key("credit_consume") and conds.has_key("deposit_changes"):
        return deposits
    
    if not conds.has_key("credit_consume") and conds.has_key("deposit_changes"):
        return deposits

    return reportlib.mergeLists(credits,deposits,"change_time_e","change_time_e")
