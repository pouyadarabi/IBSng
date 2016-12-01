
def applyLimitOnUser(user_obj,instance,rate_kbytes):
    """
        apply "ras_kbytes" limit on "instance" of "user_obj"
        currently this method only support linux ppp Ras.
    """
    user_msg=user_obj.createUserMsg(instance,"SIMPLE_BANDWIDTH_LIMIT")
    user_msg["rate_kbytes"]=rate_kbytes
    user_msg["action"]="apply"
    user_msg.send()

def removeLimitOnUser(user_obj,instance):
    user_msg=user_obj.createUserMsg(instance,"SIMPLE_BANDWIDTH_LIMIT")
    user_msg["action"]="remove"
    user_msg.send()