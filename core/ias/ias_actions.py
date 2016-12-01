from core.db import db_main,ibs_db,ibs_query
from core.lib.general import *
from core.lib import report_lib

class IASActions:
    TYPES=["CHANGE_CREDIT","CHANGE_DEPOSIT","ADD_USER","DELETE_USER","ADD_ADMIN","DELETE_ADMIN"]

    def logEvent(self, event_type, admin_username, amount, destination, comment=""):
        """
            log an event to ias_event table. Returing the query needed to insert the event
            
            WARNING: this function doesn't validate the inputs. Upper levels are
                     responsible for validating
        """
        if defs.IAS_ENABLED:
            event_id=self.__getNewEventID()
            event_type_id=self.__typeTextToID(event_type)
            return self.__logEventQuery(event_id, event_type_id, admin_username, amount, destination, comment)
        else:
            return ""

    def __getNewEventID(self):
        return db_main.getHandle().seqNextVal("ias_event_event_id")

    def __typeTextToID(self, event_type):
        return self.TYPES.index(event_type) +1

    def __logEventQuery(self, event_id, event_type_id, admin_username, amount, destination, comment):
        return ibs_db.createFunctionCallQuery("insert_ias_event", \
                        ["%s::bigint"%event_id,"%s::smallint"%event_type_id,dbText(admin_username),"%s::numeric"%amount,dbText(destination),dbText(comment)])
    ###############################################################
    def getEvents(self, from_event_id, _from, to):
        self.__getEventsCheckInput(from_event_id,_from,to)
        return db_main.getHandle().get("ias_event","event_id>%s"%from_event_id,_from,to,"event_id")

    def __getEventsCheckInput(self, from_event_id,_from,to):
        if not isInt(from_event_id):
            raise GeneralException(errorText("IAS","INVALID_EVENT_ID")) 
            
        report_lib.checkFromTo(_from,to)
    #################################################################       
    def deleteEvents(self, event_ids):
        self.__deleteEventsCheckInput(event_ids)
        self.__deleteEventsDB(event_ids)

    def __deleteEventsCheckInput(self, event_ids):
        for event_id in event_ids:
            if not isInt(event_id):
                raise GeneralException(errorText("IAS","INVALID_EVENT_ID")) 

    def __deleteEventsDB(self, event_ids):
        query=ibs_query.IBSQuery()
        for event_id in event_ids:
            query+=self.__deleteEventQuery(event_id)
        query.runQuery()
    
    def __deleteEventQuery(self, event_id):
        return ibs_db.createDeleteQuery("ias_event","event_id=%s"%event_id)
