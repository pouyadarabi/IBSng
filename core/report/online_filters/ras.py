from core.report.onlines_filter import OnlinesFilter
from core.ras import ras_main

class RasOnlinesFilter(OnlinesFilter):
    """
        filter online users by ras ip
    """
    def appliesOnCond(self, conds):
        if conds.has_key("ras_ips"):
            
            conds["ras_ids"] = []
            for ras_ip in conds["ras_ips"]:
                conds["ras_ids"].append(ras_main.getLoader().getRasByIP(ras_ip).getRasID())
    
            return True
        
        return False
    
    def filter(self, user_obj, instance, conds):
        return user_obj.getInstanceInfo(instance)["ras_id"] in conds["ras_ids"]
