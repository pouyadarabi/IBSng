from core.ibs_exceptions import *
from core.errors import errorText
from core.lib.general import *
from core.db import db_main,ibs_db,ibs_query
from core.charge.voip_tariff import tariff_main
from core.charge import charge_main
import itertools,copy


class TariffActions:
    def addNewTariff(self,tariff_name,comment):
        """
            add new tariff
            tariff_name(str): name of new tariff
        """
        self.__addNewTariffCheckInput(tariff_name,comment)
        tariff_id=self.__getNewTariffID()
        self.__insertTariffDB(tariff_id,tariff_name,comment)
        tariff_main.getLoader().loadTariffByID(tariff_id)
        return tariff_id


    def __addNewTariffCheckInput(self,tariff_name,comment):
        if not isValidName(tariff_name):
            raise GeneralException(errorText("VOIP_TARIFF","BAD_TARIFF_NAME")%tariff_name)
        
        if tariff_main.getLoader().tariffNameExists(tariff_name):
            raise GeneralException(errorText("VOIP_TARIFF","TARIFF_NAME_ALREADY_EXISTS")%tariff_name)
            
    def __getNewTariffID(self):
        return db_main.getHandle().seqNextVal("voip_charge_rule_tariff_tariff_id_seq")

    def __insertTariffDB(self,tariff_id,tariff_name,comment):
        db_main.getHandle().transactionQuery(self.__insertTariffQuery(tariff_id,tariff_name,comment))

    def __insertTariffQuery(self,tariff_id,tariff_name,comment):
        return ibs_db.createInsertQuery("voip_charge_rule_tariff",{"tariff_id":tariff_id,
                                                                   "tariff_name":dbText(tariff_name),
                                                                   "comment":dbText(comment)})
    #######################################
    def updateTariff(self,tariff_id,tariff_name,comment):
        """
            update tariff with id tariff_id
        """
        self.__updateTariffCheckInput(tariff_id,tariff_name,comment)
        self.__updateTariffDB(tariff_id,tariff_name,comment)
        tariff_main.getLoader().unloadTariffByID(tariff_id)
        tariff_main.getLoader().loadTariffByID(tariff_id)
        
    def __updateTariffCheckInput(self,tariff_id,tariff_name,comment):
        tariff_obj=tariff_main.getLoader().getTariffByID(tariff_id)
        if tariff_obj.getTariffName()!=tariff_name:
            if not isValidName(tariff_name):
                raise GeneralException(errorText("VOIP_TARIFF","BAD_TARIFF_NAME")%tariff_name)
        
            if tariff_main.getLoader().tariffNameExists(tariff_name):
                raise GeneralException(errorText("VOIP_TARIFF","TARIFF_NAME_ALREADY_EXISTS")%tariff_name)


    def __updateTariffDB(self,tariff_id,tariff_name,comment):
        db_main.getHandle().transactionQuery(self.__updateTariffQuery(tariff_id,tariff_name,comment))

    def __updateTariffQuery(self,tariff_id,tariff_name,comment):
        return ibs_db.createUpdateQuery("voip_charge_rule_tariff",
                                        {"tariff_name":dbText(tariff_name),
                                        "comment":dbText(comment)},
                                        "tariff_id=%s"%tariff_id)
    #########################################
    def deleteTariff(self,tariff_name):
        """
            delete a tariff using it's "tariff_name"
        """     
        self.__deleteTariffCheckInput(tariff_name)
        tariff_obj=tariff_main.getLoader().getTariffByName(tariff_name)
        self.__deleteTariffDB(tariff_obj.getTariffID())
        tariff_main.getLoader().unloadTariffByID(tariff_obj.getTariffID())
    
    def __deleteTariffCheckInput(self,tariff_name):
        tariff_obj=tariff_main.getLoader().getTariffByName(tariff_name)
        self.__tariffUsedInCharge(tariff_obj.getTariffID())


    def __tariffUsedInCharge(self,tariff_id):
        def checkTariffInChargeObj(charge_obj):
            if charge_obj.isVoIPCharge():
                for rule_obj in charge_obj.getRules().itervalues():
                    if rule_obj.getTariffObj().getTariffID()==tariff_id:
                        raise GeneralException(errorText("VOIP_TARIFF","TARIFF_USED_IN_CHARGE")%charge_obj.getChargeName())


        charge_main.getLoader().runOnAllCharges(checkTariffInChargeObj)

    def __deleteTariffDB(self,tariff_id):
        query=self.__deleteTariffPrefixesQuery(tariff_id)
        query+=self.__deleteTariffQuery(tariff_id)
        db_main.getHandle().transactionQuery(query)
    
    def __deleteTariffQuery(self,tariff_id):
        return ibs_db.createDeleteQuery("voip_charge_rule_tariff","tariff_id=%s"%tariff_id)
        
    def __deleteTariffPrefixesQuery(self,tariff_id):
        return ibs_db.createDeleteQuery("tariff_prefix_list","tariff_id=%s"%tariff_id)
    
    ########################################
    def addPrefix(self,tariff_name,prefix_codes,prefix_names,cpms,free_seconds,min_durations,round_tos,min_chargable_durations):
        """
            add a prefix to tariff with name "tariff_name"
            prefix_codes(list of str): list of prefix codes
            prefix_names(list of str): list of prefix names
            cpms(list of float): list of charge per minutes
            free_seconds(list of int): list of free seconds of calls
            min_durations(list of int): list of minimum durations of call in seconds
            round_tos(list of int): round calls to this amount of seconds
            min_chargable_durations(list of int): list of minimum chargable durations
            
            WARNING: All lists should have same length
            
            return a dictionary in format {"success":bool,"errs":list of errs}
        """
        errs=self.__addPrefixCheckInput(tariff_name,prefix_codes,prefix_names,cpms,free_seconds,min_durations,round_tos,min_chargable_durations)
        if errs: return {"errs":errs,"success":False}
        tariff_obj=tariff_main.getLoader().getTariffByName(tariff_name)
        prefix_ids=map(lambda x:self.__getNewPrefixID(),xrange(len(prefix_codes)))
        self.__addPrefixDB(tariff_obj.getTariffID(),prefix_ids,prefix_codes,prefix_names,cpms,free_seconds,min_durations,round_tos,min_chargable_durations)
        tariff_main.getLoader().loadTariffByID(tariff_obj.getTariffID())
        return {"errs":[],"success":True}

    def __addPrefixCheckInput(self,tariff_name,prefix_codes,prefix_names,cpms,free_seconds,min_durations,round_tos,min_chargable_durations):
        tariff_obj=tariff_main.getLoader().getTariffByName(tariff_name)
        if not len(prefix_codes)==len(prefix_names)==len(cpms)==len(free_seconds)==len(min_durations)==len(round_tos)==len(min_chargable_durations):
            raise GeneralException(errorText("VOIP_TARIFF","PREFIX_COUNT_NOT_EQUAL"))
        errs=[]
        line=1
        for code,name,cpm,free_sec,min_duration,round_to,min_chargable_duration in itertools.izip(prefix_codes,prefix_names,cpms,free_seconds,min_durations,round_tos,min_chargable_durations):
            cpm,free_sec,min_duration,round_to,min_chargable_duration=self.__convertToInt(cpm,free_sec,min_duration,round_to,min_chargable_duration,errs,line)
            self.__checkPrefix(code,name,cpm,free_sec,min_duration,round_to,min_chargable_duration,errs,line)
            self.__checkCodeExistence(code,tariff_obj,errs,line)
            self.__checkCodeDuplicates(prefix_codes,line-1,errs,line)
            line+=1
        
        return errs

    def __convertToInt(self,cpm,free_sec,min_duration,round_to,min_chargable_duration,errs,line):
        try:
            cpm=float(cpm)
        except ValueError:
            errs.append("%s:%s"%(line,errorText("CHARGES","CPM_NOT_NUMERIC")))
            cpm=0

        try:
            free_sec=int(free_sec)
        except ValueError:
            errs.append("%s:%s"%(line,errorText("VOIP_TARIFF","FREE_SECONDS_NOT_NUMERIC")))
            free_sec=0

        try:
            min_duration=int(min_duration)
        except ValueError:
            errs.append("%s:%s"%(line,errorText("VOIP_TARIFF","MIN_DURATION_NOT_NUMERIC")))
            min_duration=0

        try:
            round_to=int(round_to)
        except ValueError:
            errs.append("%s:%s"%(line,errorText("VOIP_TARIFF","ROUND_TO_NOT_NUMERIC")))
            round_to=0

        try:
            min_chargable_duration=int(min_chargable_duration)
        except ValueError:
            errs.append("%s:%s"%(line,errorText("VOIP_TARIFF","MIN_CHARGABLE_DURATION_NOT_NUMERIC")))
            round_to=0

        return (cpm,free_sec,min_duration,round_to,min_chargable_duration)
        
    def __checkPrefix(self,code,name,cpm,free_sec,min_duration,round_to,min_chargable_duration,errs,line):
        if not code.isdigit():
            errs.append("%s:%s"%(line,errorText("VOIP_TARIFF","PREFIX_CODE_IS_NOT_DIGIT")%code))
            
        if not isFloat(cpm):
            errs.append("%s:%s"%(line,errorText("CHARGES","CPM_NOT_NUMERIC")))

        if cpm<0:
            errs.append("%s:%s"%(line,errorText("CHARGES","CPM_NOT_POSITIVE")))
        
        if not isInt(free_sec) or free_sec<0:
            errs.append("%s:%s"%(line,errorText("VOIP_TARIFF","FREE_SECONDS_NOT_NUMERIC")))
        
        if not isInt(min_duration) or min_duration<0:
            errs.append("%s:%s"%(line,errorText("VOIP_TARIFF","MIN_DURATION_NOT_NUMERIC")))
        
        if not isInt(round_to) or round_to<0:
            errs.append("%s:%s"%(line,errorText("VOIP_TARIFF","ROUND_TO_NOT_NUMERIC")))

        if not isInt(min_chargable_duration) or min_chargable_duration<0:
            errs.append("%s:%s"%(line,errorText("VOIP_TARIFF","MIN_CHARGABLE_DURATION_NOT_NUMERIC")))
        

    def __checkCodeExistence(self,code,tariff_obj,errs,line):
        if tariff_obj.hasPrefixCode(code):
            errs.append("%s:%s"%(line,errorText("VOIP_TARIFF","PREFIX_CODE_ALREADY_EXIST")%(code,tariff_obj.getTariffName())))

    def __checkCodeDuplicates(self,prefix_codes,_index,errs,line):
        """
            check if there's duplicate prefix_code for prefix_codes[_index] from 0 to _index
        """
        for i in xrange(0,_index):
            if prefix_codes[i]==prefix_codes[_index]:
                errs.append("%s:%s"%(line,errorText("VOIP_TARIFF","DUPLICATE_PREFIX_CODE")%(prefix_codes[_index])))
                return

    def __getNewPrefixID(self):
        return db_main.getHandle().seqNextVal("tariff_prefix_list_tariff_id_seq")

    def __addPrefixDB(self,tariff_id,prefix_ids,prefix_codes,prefix_names,cpms,free_seconds,min_durations,round_tos,min_chargable_durations):
        query=ibs_query.IBSQuery()
        for _id,code,name,cpm,free_sec,min_duration,round_to,min_chargable_duration in itertools.izip(prefix_ids,prefix_codes,prefix_names,cpms,free_seconds,min_durations,round_tos,min_chargable_durations):
            query+=self.__addPrefixQuery(tariff_id,_id,code,name,cpm,free_sec,min_duration,round_to,min_chargable_duration)
        query.runQuery()

    def __addPrefixQuery(self,tariff_id,prefix_id,code,name,cpm,free_sec,min_duration,round_to,min_chargable_duration):
        return ibs_db.createInsertQuery("tariff_prefix_list",{"tariff_id":tariff_id,
                                                       "prefix_id":prefix_id,
                                                       "prefix_code":dbText(code),
                                                       "prefix_name":dbText(name),
                                                       "cpm":cpm,
                                                       "free_seconds":free_sec,
                                                       "min_duration":min_duration,
                                                       "round_to":round_to,
                                                       "min_chargable_duration":min_chargable_duration})
    ###############################################
    def updatePrefix(self,tariff_name,prefix_id,prefix_code,prefix_name,cpm,free_second,min_duration,round_to,min_chargable_duration):
        self.__updatePrefixCheckInput(tariff_name,prefix_id,prefix_code,prefix_name,cpm,free_second,min_duration,round_to,min_chargable_duration)
        tariff_obj=tariff_main.getLoader().getTariffByName(tariff_name)
        self.__updatePrefixDB(tariff_obj.getTariffID(),prefix_id,prefix_code,prefix_name,cpm,free_second,min_duration,round_to,min_chargable_duration)
        tariff_main.getLoader().loadTariffByID(tariff_obj.getTariffID())

    def __updatePrefixCheckInput(self,tariff_name,prefix_id,prefix_code,prefix_name,cpm,free_second,min_duration,round_to,min_chargable_duration):
        tariff_obj=tariff_main.getLoader().getTariffByName(tariff_name)
        
        if not tariff_obj.hasPrefixID(prefix_id):
            raise GeneralException(errorText("VOIP_TARIFF","TARIFF_DOESNT_HAVE_PREFIX_ID")%(tariff_obj.getTariffName(),prefix_id))

        if tariff_obj.getPrefixByID(prefix_id).getPrefixCode()!=prefix_code and tariff_obj.hasPrefixCode(prefix_code):
            raise GeneralException(errorText("VOIP_TARIFF","PREFIX_CODE_ALREADY_EXIST")%(prefix_code,tariff_obj.getTariffName()))
                
        errs=[]
        self.__checkPrefix(prefix_code,prefix_name,cpm,free_second,min_duration,round_to,min_chargable_duration,errs,1)
        if errs:
            raise GeneralException("\n".join(errs))

    def __updatePrefixDB(self,tariff_id,prefix_id,prefix_code,prefix_name,cpm,free_second,min_duration,round_to,min_chargable_duration):
        db_main.getHandle().transactionQuery(
            self.__updatePrefixQuery(tariff_id,prefix_id,prefix_code,prefix_name,cpm,free_second,min_duration,round_to,min_chargable_duration))

    def __updatePrefixQuery(self,tariff_id,prefix_id,prefix_code,prefix_name,cpm,free_second,min_duration,round_to,min_chargable_duration):
        return ibs_db.createUpdateQuery("tariff_prefix_list",{"prefix_code":dbText(prefix_code),
                                                       "prefix_name":dbText(prefix_name),
                                                       "cpm":cpm,
                                                       "free_seconds":free_second,
                                                       "min_duration":min_duration,
                                                       "round_to":round_to,
                                                       "min_chargable_duration":min_chargable_duration},"prefix_id=%s"%prefix_id)
    ###############################################
    def deletePrefix(self,tariff_name,prefix_codes):
        """
            prefix_codes(iterable object): prefix codes
        """
        self.__delPrefixCheckInput(tariff_name,prefix_codes)
        tariff_obj=tariff_main.getLoader().getTariffByName(tariff_name)
        self.__delPrefixDB(tariff_obj.getTariffID(),prefix_codes)
        tariff_main.getLoader().loadTariffByID(tariff_obj.getTariffID())

    def __delPrefixCheckInput(self,tariff_name,prefix_codes):
        tariff_obj=tariff_main.getLoader().getTariffByName(tariff_name)
        if not len(prefix_codes):
            raise GeneralException(errorText("VOIP_TARIFF","NO_PREFIX_TO_DELETE"))
        for code in prefix_codes:
            if not tariff_obj.hasPrefixCode(code):
                raise GeneralException(errorText("VOIP_TARIFF","TARIFF_DOESNT_HAVE_PREFIX_CODE")%(tariff_obj.getTariffName(),code))
                
    def __delPrefixDB(self,tariff_id,prefix_codes):
        db_main.getHandle().transactionQuery(self.__delPrefixQuery(tariff_id,prefix_codes))

    def __delPrefixQuery(self,tariff_id,prefix_codes):
        prefix_code_cond = " or ".join(map(lambda code:"prefix_code=%s"%dbText(code),prefix_codes))
        return ibs_db.createDeleteQuery("tariff_prefix_list","(%s) and tariff_id = %s"%(prefix_code_cond, tariff_id))
    ################################################