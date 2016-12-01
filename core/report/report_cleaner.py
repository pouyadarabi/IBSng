from core.db import db_main
from core.lib import ibs_states
from core.event import daily_events
from core.lib.date import RelativeDate
from core.lib import ibs_states
from core.lib.general import *

class ReportCleaner:
    def __init__(self):
        self.__tables={"connection_log":"delete from connection_log_details where connection_log_id in \
                                         (select connection_log_id from connection_log where login_time < %%s); \
                                         delete from connection_log where login_time < %%s ;",
                       "credit_change":"delete from credit_change_userid where credit_change_id in \
                                        (select credit_change_id from credit_change where change_time < %%s); \
                                        delete from credit_change where change_time < %%s ;",
                       "user_audit_log":"delete from user_audit_log where change_time < %%s ;",
                       "snapshots":"delete from internet_onlines_snapshot where snp_date < %%s; \
                                    delete from voip_onlines_snapshot where snp_date < %%s; \
                                    delete from internet_bw_snapshot where snp_date < %%s; ",
                        "web_analyzer_log":"delete from web_analyzer_log where _date < %%s; "
                      }
        
        daily_events.addLowLoadJob(self.autoClean,[])


    def cleanLogs(self, table, date):
        """
            clean all logs of "table" before that "date", 
            "date" will be passed directly to database, so it can contain database clauses
        """
        try:
            query = self.__tables[table].replace("%%s",date)
        except KeyError:
            raise GeneralException(errorText("REPORTS","INVALID_CLEAN_TABLE") % table)
            
        db_main.getHandle().transactionQuery(query)


    def cleanLogsFromSeconds(self, table, seconds):
        return self.cleanLogs(table, "now() - interval '%s seconds'" % seconds)
    #########################################
    def getStateObj(self, table_name):
        return ibs_states.State("AUTO_CLEAN_%s"%table_name.upper())

    def autoClean(self):
        """
            Auto clean all tables, if it's set in ibs states.
            This method is called at low load daily jobs, every day
        """
        for table_name in self.__tables:
            state_obj = self.getStateObj(table_name)
            state_val = long(state_obj.getCurVal())
            if state_val > 0:
                self.cleanLogsFromSeconds(table_name, state_val)

    #####################################
    def updateAutoCleanStates(self,tables_dic):
        """
            tables_dic(dic): dic of table_name=>(date,date_unit)
            date and date_unit will be passed to RelativeDate, and should be valid for initializer
        """
        query = ""
        for table_name in tables_dic:
            if table_name not in self.__tables:
                raise GeneralException(errorText("REPORTS","INVALID_CLEAN_TABLE") % table_name)
        
            date, date_unit = tables_dic[table_name]
            
            date = to_int(date, "%s auto clean"%table_name)
            
            if date < 0 :
                raise GeneralException(errorText("REPORTS","INVALID_AUTO_CLEAN_TABLE_DATE") % (date, table_name))
            
            state_obj = self.getStateObj(table_name)
            
            query += state_obj.updateValueQuery(RelativeDate(date, date_unit).getDateSeconds())
                
        db_main.getHandle().transactionQuery(query)

    def getAutoCleanDates(self):
        """
            return a dic of {table_name=>(date,date_unit)}
        """
        dates = {}

        for table_name in self.__tables:
            state_obj = self.getStateObj(table_name)
            dates[table_name] = RelativeDate(state_obj.getCurVal(), "Seconds").getFormattedDate() 

        return dates