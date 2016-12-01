from core.charge.internet_charge import InternetCharge
from core.charge.voip_charge import VoipCharge
from core.charge.internet_charge_rule import InternetChargeRule
from core.charge.voip_charge_rule import VoipChargeRule
from core.lib.time_lib import *
from core.ibs_exceptions import *

def getChargeClassForType(_type):
    if _type=="Internet":
        return InternetCharge
    elif _type=="VoIP":
        return VoipCharge
    else:
        raise IBSException(errorText("CHARGES","INVALID_CHARGE_TYPE")%_type)
    
def getRulesTable(_type):
    """
        return table that rules of _type charge_obj is available there
        rule tables are diffrent based on charge type
    """
    if _type=="Internet":
        return "internet_charge_rules"
    elif _type=="VoIP":
        return "voip_charge_rules"
    else:
        raise IBSException(errorText("CHARGES","INVALID_CHARGE_TYPE")%_type)

def getChargeRuleObjForType(_type,rule_info,charge_obj,day_of_weeks,ports):
    if _type=="Internet":
        return InternetChargeRule(rule_info["charge_rule_id"],charge_obj,rule_info["cpm"],rule_info["cpk"],day_of_weeks,\
                          rule_info["start_time"],rule_info["end_time"],rule_info["bandwidth_limit_kbytes"],\
                          rule_info["bw_transmit_leaf_id"],rule_info["bw_receive_leaf_id"],rule_info["assumed_kps"],\
                          rule_info["ras_id"],ports)


    elif _type=="VoIP":
        return VoipChargeRule(rule_info["charge_rule_id"],charge_obj,\
                          day_of_weeks,rule_info["start_time"],rule_info["end_time"], \
                          rule_info["tariff_id"],rule_info["ras_id"],ports)
    else:
        raise IBSException(errorText("CHARGES","INVALID_CHARGE_TYPE")%_type)
