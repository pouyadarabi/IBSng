from core.user import user_main

class VoIPErrors:
    #standard debit card errors
    errors={"VOIP_USERNAME_DOESNT_EXISTS":1, 
            "WRONG_PASSWORD":1,
            "NO_VOIP_USERNAME_DEFINED":1,
            "NO_APPLICABLE_RULE":2,
            "NO_PREFIX_FOUND":2,
            "MAX_CONCURRENT":3,
            "CANT_USE_MORE_THAN_ONE_SERVICE":3,
            "RAS_DOESNT_ALLOW_MULTILOGIN":3,
            "CREDIT_FINISHED":4,
            "ABS_EXP_DATE_REACHED":5,
            "REL_EXP_DATE_REACHED":5,
            "LOGIN_FROM_THIS_CALLER_ID_DENIED":7,
            "USER_LOCKED":7,
            "NO_CHARGE_DEFINED":7,
            "UNKNOWN_ERROR":-1
            }


    def applySuccess(self,ras_msg):
        """
            apply error/return codes to successful voip ras message
        """

        if ras_msg.hasAttr("single_session_h323"):
            user_obj = self.__getUserObj(ras_msg)
            if ras_msg.hasAttr("h323_pre_authentication"):
                remaining_credit = user_main.getUserPool().getUserByCallerID(ras_msg["caller_id"]).getBasicUser().getCredit()
                ras_msg.getRasObj().setSingleH323CreditAmount(ras_msg.getReplyPacket(), remaining_credit)

            elif ras_msg.hasAttr("h323_authentication"):
                remaining_credit = user_main.getUserPool().getUserByVoIPUsername(ras_msg["voip_username"]).getBasicUser().getCredit()
                ras_msg.getRasObj().setSingleH323CreditAmount(ras_msg.getReplyPacket(), remaining_credit)

            elif ras_msg.hasAttr("h323_authorization"):
                remaining_time = user_obj.getTypeObj().getSingleSessionRemainingTime()
                ras_msg.getRasObj().setSingleH323CreditTime(ras_msg.getReplyPacket(), remaining_time)

            
            ras_msg.getRasObj().setSingleH323ReturnCode(ras_msg.getReplyPacket(), 0)
    
        return True

    
    def applyFailure(self,ras_msg, err_obj):
        """
            apply error/return codes to failed voip ras message
            err_obj (IBSError instance): Error object, that has been raised as Exception
        """
        ras_msg["error_key"]=err_obj.getErrorKey()

        if ras_msg.hasAttr("single_session_h323"):
            if ras_msg.hasAttr("h323_pre_authentication"):
                return_code = 1
                return_val = True
                
            if ras_msg.hasAttr("h323_authentication") or ras_msg.hasAttr("h323_authorization"):
                return_code = self.getErrorCode(err_obj)
                return_val = False
        
            ras_msg.getRasObj().setSingleH323ReturnCode(ras_msg.getReplyPacket(), return_code)
            return return_val

        return False    
    
    def __getUserObj(self,ras_msg):
        return user_main.getOnline().getUserObjByUniqueID(ras_msg.getRasID(), ras_msg.getUniqueIDValue())


    def getErrorCode(self,ibs_error_obj):
        try:
            return self.errors[ibs_error_obj.getErrorKey()]
        except:
            return self.errors["UNKNOWN_ERROR"]
        