from core.db import ibs_db,db_main
from core.lib.general import *

class DepositChangeLogActions:
    def logDepositChangeQuery(self,changer_admin_id,admin_id,deposit_change,comment,remote_addr):
        deposit_change_id=self.__getNewDepositChangeID()
        return ibs_db.createInsertQuery("admin_deposit_change",{"admin_id":changer_admin_id,
                                                                "to_admin_id":admin_id,
                                                                "deposit_change":deposit_change,
                                                                "comment":dbText(comment),
                                                                "remote_addr":dbText(remote_addr),
                                                                "admin_deposit_change_id":deposit_change_id})
                                                
    def __getNewDepositChangeID(self):
        return db_main.getHandle().seqNextVal("admin_deposit_change_id")
        