from core.threadpool import thread_main

class UserType:
    def __init__(self,user_obj):
        self.user_obj=user_obj

    def killInstance(self,instance):
        """
            should be called while online lock has been held
        """
        self.user_obj.getInstanceInfo(instance)["killed"] = True
        user_msg=self.user_obj.createUserMsg(instance,"KILL_USER")
        thread_main.runThread(user_msg.send,[])

    def logout(self,instance,ras_msg):
        """
            logout the user
            return an tuple of (ibs_query instance, used_credit)
            this function is responsible for commiting user credit if necessary
        """
        pass

    def getOnlineReportDic(self,instance):
        return {}

    def getLoginTime(self,instance):
        """
            return login time of instance in epoch
        """
        pass
    


    