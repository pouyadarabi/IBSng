
class DialerErrors:
    errors={"NORMAL_USERNAME_DOESNT_EXISTS":900,
        "USER_LOCKED":901,
        "NO_CHARGE_DEFINED":902,
        "NO_APPLICABLE_RULE":903,
        "ABS_EXP_DATE_REACHED":904,
        "REL_EXP_DATE_REACHED":905,
        "CREDIT_FINISHED":906,
        "WRONG_PASSWORD":907,
        "MAX_CONCURRENT":908,
        "RAS_DOESNT_ALLOW_MULTILOGIN":908,
        "UNKNOWN_ERROR":909,
        "LOGIN_FROM_THIS_MAC_DENIED":910,
        "LOGIN_FROM_THIS_IP_DENIED":911,
        "CANT_USE_MORE_THAN_ONE_SERVICE":912,
        "LOGIN_FROM_THIS_CALLER_ID_DENIED":913,
        "TIMELY_QUOTA_EXCEEDED":914,
        "TRAFFIC_QUOTA_EXCEEDED":915,
        "SYSTEM_SHUTTING_DOWN":916,
        "LOGIN_NOT_ALLOWED":917}

    def applyToRasMsg(self, ras_msg, ibs_error_obj):
        err_code=self.getErrorCode(ibs_error_obj)

        if ras_msg.hasAttr("pap_password"):
            reply_message = "E=%s"%err_code
        else:
            reply_message = "E=%s R=0 "%err_code

        ras_msg.getReplyPacket()["Reply-Message"] = reply_message

    def getErrorCode(self,ibs_error_obj):
        try:
            return self.errors[ibs_error_obj.getErrorKey()]
        except:
            return self.errors["UNKNOWN_ERROR"]
