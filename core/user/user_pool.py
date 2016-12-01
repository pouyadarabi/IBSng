"""
XXX TODO: Make getUserByNormalUsername and similars efficent without two query of same table

"""

from core.user import user_main
from core.user.loading_user import LoadingUser
from core.stats import stat_main
from core.ibs_exceptions import *
from core.errors import errorText
import threading

class ReleaseCandidates:
    """
        this class keep loaded users and can be queried to release a user and tells the user id of user
            that should be released
        users will be kept in a sorted list that will be act as a lifo queue
        
        NOTE: we're keeping LoadedUser instance of online users in the same list as others
              if we see one of them, we add them to the end of list. This makes life easy(TM) but
              maybe inefficient if USER_POOL_SIZE is small.
              so please keep USER_POOL_SIZE 10x factor of your online users
    """
    def __init__(self):
        """
            initialize the internal list            
        """
        self.__release_candidates=[] #sorted list of release candidate users sorted 
        self.lock=threading.RLock()

    def addUser(self,loaded_user):
        """
            add a new user to queue
            loaded_user(LoadedUser instance)
        """
        self.lock.acquire()
        try:
            self.__release_candidates.append(loaded_user)
        finally:
            self.lock.release()
        
    def getCandidate(self):
        """
            get a candidate to release.
            return LoadedUser instance(deleted from our queue already) or 
            None value if no user can be released at this time (Shows that USER_POOL_SIZE is small!)
        """
        self.lock.acquire()
        try:
            loaded_user=None
            try:
                loaded_user=self.__release_candidates.pop(0)
            except IndexError: #empty list BadThingHappened(TM)
                toLog("User Pool is full and we can't release anyone!!! Please increase USER_POOL_SIZE in defs ASAP!",LOG_ERROR&LOG_DEBUG)
                return None
        
            return loaded_user
        finally:
            self.lock.release()


class UserPool:
    """
        XXX MISSING: Normal And VoIP mapping to user_ids in memory!
    """
    DEBUG=False

    def __init__(self):
        self.__pool_by_id={} #this is reference pool. All users should be here
        self.__pool_len=0
        self.__black_list=[] #user_ids that we should not load
        self.loading_users=LoadingUser()
        self.rel_candidates=ReleaseCandidates()
        self.lock=threading.RLock() #dictionary lock

        stat_main.getStatKeeper().registerStat("user_pool_hits", "int")
        stat_main.getStatKeeper().registerStat("user_pool_misses", "int")

    def __incHits(self):
        stat_main.getStatKeeper().inc("user_pool_hits")

    def __incMisses(self):
        stat_main.getStatKeeper().inc("user_pool_misses")

    def __fixUserID(self,user_id):
        return long(user_id)
        
    def __isInPoolByID(self,user_id):
        """
            check if user with id "user_id" is in pool return LoadedUser instance if 
            it's in pool or None if it isn't
        """
        self.lock.acquire()
        try:
            if self.__pool_by_id.has_key(user_id):
                self.__incHits()
                return self.__pool_by_id[user_id]

            self.__incMisses()
            return None
        finally:
            self.lock.release()

    def __saveInPool(self,loaded_user):
        """
            Save LoadedUser instance into pool
        """
        self.__checkPoolSize()
        self.rel_candidates.addUser(loaded_user)
        self.__addToPool(loaded_user)

    def __addToPool(self,loaded_user):
        self.lock.acquire()
        try:
            self.__pool_by_id[loaded_user.getUserID()]=loaded_user
        finally:
            self.lock.release()

    def __checkPoolSize(self):
        """
            check pool size and release a user if we are more then defs.MAX_USER_POOL_SIZE
        """
        self.lock.acquire()
        try:
            self.__pool_len+=1
        finally:
            self.lock.release()

        if self.__pool_len>defs.MAX_USER_POOL_SIZE: 
            self.__releaseOneUser()

    def __releaseOneUser(self):
        """
            release a user from pool, if possible
        """
        loaded_user=self.rel_candidates.getCandidate()
        while loaded_user:
            self.loading_users.loadingStart(loaded_user.getUserID())
            try:
                if not loaded_user.isOnline():
                    try:
                        self.__delFromPool(loaded_user.getUserID())
                        break
                    except KeyError: #user has been deleted previously by userChanged method
                        pass

            finally:
                self.loading_users.loadingEnd(loaded_user.getUserID())
            
            loaded_user=self.rel_candidates.getCandidate()          

    def __delFromPool(self,user_id):
        """
            delete user with id "user_id" from pool
        """
        self.lock.acquire()
        try:
            self.__pool_len-=1
            del(self.__pool_by_id[user_id])
        finally:
            self.lock.release()


    def __loadUserByID(self,user_id):
        """
            load user into memory using user id and return a LoadedUser instance
            also put user in pool
        """     
        loaded_user=user_main.getUserLoader().getLoadedUserByUserIDs((user_id,))[0]
        self.__saveInPool(loaded_user)
        return loaded_user

    def __loadUsersByID(self,user_ids):
        """
            load user with ids in memory and return a list of LoadedUser instances
        """     
        loaded_users=user_main.getUserLoader().getLoadedUserByUserIDs(user_ids)
        map(self.__saveInPool,loaded_users)
        return loaded_users

################################
    def getUserByID(self,user_id,online_flag=False):
        """
            return a LoadedUser instance of user with id "user_id"
        """
        user_id=self.__fixUserID(user_id)
        self.loading_users.loadingStart(user_id)
        try:
            loaded_user=self.__isInPoolByID(user_id)
            if loaded_user==None:
                loaded_user=self.__loadUserByID(user_id)
            
            if online_flag: #it should be done here, because we don't want to release this user while he's trying to log in
                self.__checkBlackList(user_id)
                loaded_user.setOnlineFlag(True)
        finally:
            self.loading_users.loadingEnd(user_id)
        return loaded_user

    def getUsersByID(self,user_ids, keep_order=False):
        """
            return a list of LoadedUser instance of users with ids "user_ids"
            keep_order(boolean): if set to true, try keeping order of loaded_users as same order as user_ids
                                 this job is fairly expensive
        """
        loaded_users = []

        all_user_ids=map(self.__fixUserID,user_ids)
        all_user_ids.sort() #prevent dead lock by loading users in order
        
        i = 0
        to_load_ids = []
        while i < len(all_user_ids):
            user_id = all_user_ids[i]
            self.loading_users.loadingStart(user_id)
            try:
                loaded_user=self.__isInPoolByID(user_id)
                if loaded_user==None: # is user cached?
                    to_load_ids.append(user_id)
                    
                    if len(to_load_ids) == defs.POSTGRES_MAGIC_NUMBER: 
                        if self.DEBUG:
                            toLog("UserPool(getUsersById): bulk loading %s number of users"%len(to_load_ids),LOG_DEBUG)
                            
                        loaded_users += self.__loadUsersByID(to_load_ids)
                        map(self.loading_users.loadingEnd, to_load_ids)
                        to_load_ids = []
                        
                else:
                    loaded_users.append(loaded_user)
                    self.loading_users.loadingEnd(user_id)

            except:
                if user_id not in to_load_ids:
                    to_load_ids.append(user_id)

                map(self.loading_users.loadingEnd, to_load_ids)
                raise
                        
            i += 1

        #load rest of users
        try:
            if self.DEBUG:
                toLog("UserPool(getUsersById): rest loading %s number of users"%len(to_load_ids),LOG_DEBUG)

            loaded_users += self.__loadUsersByID(to_load_ids)
        finally:
            map(self.loading_users.loadingEnd, to_load_ids)
        
        if keep_order:
            return self.__fixLoadedUsersOrder(
                                                map(self.__fixUserID,user_ids), 
                                                loaded_users
                                             )
        else:
            return loaded_users
        
        
    def __fixLoadedUsersOrder(self, user_ids, loaded_users):
        """
            fix order of loaded_users as same order as user_ids
        """
        def cmp_func(loaded_user1, loaded_user2): #compare function based on index of user_ids
            if user_ids.index(loaded_user1.getUserID()) > user_ids.index(loaded_user2.getUserID()):
                return 1
            else:
                return -1
                
        loaded_users.sort(cmp_func)
        return loaded_users
        
        
#################################
    def getUserByNormalUsername(self,normal_username,online_flag=False):
        """
            XXX: current implemention can be optimized by not querying normal_users table twice
            return a LoadedUser instance of user with normal username "normal_username"
        """
        user_id=user_main.getUserLoader().normalUsername2UserID(normal_username)
        return self.getUserByID(user_id,online_flag)

#################################
    def getUserByVoIPUsername(self,voip_username,online_flag=False):
        """
            XXX: current implemention can be optimized by not querying voip_users table twice
            return a LoadedUser instance of user with voip username "voip_username"
        """
        user_id=user_main.getUserLoader().voipUsername2UserID(voip_username)
        return self.getUserByID(user_id,online_flag)


#################################
    def getUserByCallerID(self,caller_id,online_flag=False):
        """
            return a LoadedUser instance of user with caller id "caller_id"
        """
        user_id=user_main.getUserLoader().callerID2UserID(caller_id)
        return self.getUserByID(user_id,online_flag)

#################################
    def userChanged(self,user_id):
        """
            called when attributes or information of user with id "user_id" changed
        """
        user_id=self.__fixUserID(user_id)
        self.loading_users.loadingStart(user_id)
        try:
            loaded_user=self.__isInPoolByID(user_id)
            if loaded_user != None:
                if loaded_user.isOnline():
                    self.__reloadOnlineUser(loaded_user)
                else:
                    self.__delFromPool(user_id)
        finally:
            self.loading_users.loadingEnd(user_id)

    def __reloadOnlineUser(self,loaded_user):
        new_loaded_user=user_main.getUserLoader().getLoadedUserByUserIDs((loaded_user.getUserID(),))[0]
        loaded_user._reload(new_loaded_user)
        user_main.getOnline().reloadUser(loaded_user.getUserID())
        
##################################
    def addToBlackList(self,user_id):
        """
            add user_id to blacklist
            blacklist is used to not allow users to get online, 
            not allowing them to set online flag
        """
        user_id=self.__fixUserID(user_id)
        self.__black_list.append(user_id)

    def removeFromBlackList(self,user_id):
        """
            remove user_id from blacklist
        """
        user_id=self.__fixUserID(user_id)
        self.__black_list.remove(user_id)

    def __checkBlackList(self,user_id):
        if user_id in self.__black_list:
            raise GeneralException(errorText("USER","USER_IN_BLACKLIST")%user_id)
######################################
    def reloadUsersWithFilter(self,filter_func):
        """
            run reload users if filter_func return true
            filter_func should accept an loaded_user instance and return a bool
        """
        for user_id in self.__pool_by_id.keys():
            self.loading_users.loadingStart(user_id)
            try:
                try:
                    loaded_user=self.__pool_by_id[user_id]
                except KeyError:
                    continue
                
                if apply(filter_func,[loaded_user]):
                    self.userChanged(user_id)
            finally:
                self.loading_users.loadingEnd(user_id)
