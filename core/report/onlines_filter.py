from core import defs
from core.plugins.plugin_loader import loadPlugins

from core.ibs_exceptions import *
ONLINES_FILTER_PATH="%s/report/online_filters"%defs.IBS_CORE

def init():
    initFilters()

def initFilters():
    global filters
    
    filters = []
    for module_obj in loadPlugins(ONLINES_FILTER_PATH).itervalues():
        for obj_name in dir(module_obj):
            try:
                obj = getattr(module_obj, obj_name)
                if issubclass(obj, OnlinesFilter) and obj != OnlinesFilter:
                    filters.append(obj())
            except TypeError:
                pass

def getFilters():
    return filters
    
def createFilterManager(conds):
    return OnlinesFilterManager(conds, getFilters())

class OnlinesFilter:
    def appliesOnCond(self, conds):
        """
            gived conditions "conds" should this filter apply ?
            return True or False
            
            children are allowed to add new keys in conds dictionary to make
            filtering faster. the key should start with filter name following by _
        """
        return False

    def filter(self, user_obj, instance, conds):
        """
            return True if this instance allows to pass through filter and be available on list
            return False if this instance should be filtered
        """
        return False

class OnlinesFilterManager:
    def __init__(self, conds, filter_objs):
        self.__conds = conds #dic of conditions
        self.__filters = filter_objs #filter methods
        self.__filters_apply = self.__generateFiltersApply() #what filters should apply?
        
    def __generateFiltersApply(self):
        return map(lambda filter_obj: filter_obj.appliesOnCond(self.__conds), self.__filters)
    
    def filter(self, user_obj, instance):
        if True not in self.__filters_apply:
            return True #no filter was requested

        i = 0
        for filter_obj in self.__filters:
            if self.__filters_apply[i] and filter_obj.filter(user_obj, instance, self.__conds):
                return True
        
            i += 1
        
        return False
