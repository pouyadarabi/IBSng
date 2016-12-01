from core.admin import admin_main

class AdminLock:
    def __init__(self, lock_id, locker_admin_id, admin_id, reason):
        self.lock_id=lock_id
        self.locker_admin_id=locker_admin_id
        self.admin_id=admin_id
        self.reason=reason

    def getLockerID(self):
        return self.locker_admin_id
        
    def getReason(self):
        return self.reason

    def getLockInfo(self):
        return {"lock_id":self.lock_id,
                "locker_admin":admin_main.getLoader().getAdminByID(self.locker_admin_id).getUsername(),
                "reason":self.reason}