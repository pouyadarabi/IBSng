from core.lib import time_lib

class VoIPRas:
    attr_index={"H323-conf-id":13,
                "H323-remote-address":20,
                "H323-setup-time":16,
                "H323-connect-time":18,
                "H323-disconnect-time":21,
                "H323-disconnect-cause":22,
                "H323-call-origin":17,
                "H323-call-type":15,
                "h323-gw-address":16,
                "Quintum-h323-conf-id":13,
                "Quintum-h323-connect-time":18,
                "Quintum-h323-disconnect-time":21,
                "Quintum-h323-disconnect-cause":22,
                "Quintum-h323-call-origin":17,
                "Quintum-h323-call-type":15,
                
               }
    
    def getH323AttrIndex(self,attr_name):
        """
            return cut index of attr_name
        """
        return self.attr_index[attr_name]

    def getH323AttrValue(self,attr_name,pkt):
        """
            return correct value of voip attr "attr_name"
            Cisco Style H323 attribute values has format "name=value", so for
            correct value we must cut the head of value
        """
        return pkt[attr_name][0][self.getH323AttrIndex(attr_name):]
        
    def getH323EpochTimeFromAttr(self,attr_name,pkt):
        """
            convert "attr_name" value from pkt to epoch and return it
        """
        return time_lib.getEpochFromRadiusTime(self.getH323AttrValue(attr_name,pkt))
        
    def setH323TimeInAttrs(self,ras_msg,attr_dic):
        """
            set H323 converted time in ras_msg. All Times are converted to epoch.
            attr_dic(dic): dic in format radius_attr_name=>ras_msg_attr_name
        """
        for rad_attr_name in attr_dic:
            ras_msg[attr_dic[rad_attr_name]]=self.getH323EpochTimeFromAttr(rad_attr_name,ras_msg.getRequestPacket())

    def setSingleH323CreditTime(self,reply_pkt,credit_time, conv_to_int=False):
        """
            set H323-Credit-Time or other attribute in reply_pkt
            this is only for rases that support pre-paid calling card type of auth          
        """
        if conv_to_int:
            credit_time  = int(credit_time)
            
        reply_pkt["H323-credit-time"]="h323-credit-time=%s"%credit_time

    def setSingleH323CreditAmount(self,reply_pkt,credit_amount, precision=0):
        """
	    set H323-Credit-Amount
        """
        credit_amount  = self.fixCreditPrecision(credit_amount, precision)

        reply_pkt["H323-credit-amount"]="h323-credit-amount=%s"%credit_amount

    def setSingleH323ReturnCode(self,reply_pkt,return_code):
        """

        """
        reply_pkt["H323-return-code"]="h323-return-code=%s"%return_code


    def fixCreditPrecision(self, credit, precision):
    	if precision:
	    factor = float(10**precision)
    	    return "%.2f"%(int(round(credit*factor))/factor)
    	else:
    	    return int(credit)


    def setH323PreferredLanguage(self,reply_pkt,language_code):
        """
	    Set preferred language to two char language code ex ("en","ch","sp","ru","fa",...)
        """
        reply_pkt["H323-preferred-lang"]="h323-preferred-lang=%s"%language_code
	
    def getAttrInCiscoAVPair(self, attr_name, pkt):
        """
            return value of "attr_name" in Cisco-AVPair attribute of "pkt"
        """
        for av_pair in pkt["Cisco-AVPair"]:
            if av_pair.startswith(attr_name):
                return av_pair[self.getH323AttrIndex(attr_name):]
        return ""

    def setRedirectNumber(self, reply_pkt, redirect_number):
        reply_pkt["H323-redirect-number"]="h323-redirect-number=%s"%redirect_number
    
