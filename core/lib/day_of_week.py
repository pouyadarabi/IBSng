WEEK_DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

class DayOfWeekInt:
    def __init__(self,day_of_week_int):
        """
            day_of_week_int: integer representation of day of week
            0=>"Monday", 1=>"Tuesday", 2=>"Wednesday", 3=>"Thursday", 4=>"Friday", 5=>"Saturday", 6=>"Sunday"
        """
        self.day_of_week=day_of_week_int

    def __eq__(self,other):
        """
            other(integer): integer representation of day
        """
        return other==self.day_of_week

    def getIntValue(self):
        """
            return int value of this day of week
        """
        return self.day_of_week


    def getDayString(self):
        """
            return an string representaion of this day
        """
        return WEEK_DAYS[self.day_of_week]
        
class DayOfWeekString:

    def __init__(self,day_of_week):
        """
            day_of_week: string representation of day_of_week, relation between integer and string
                         day of weeks are described on DayOfWeekInt
        
            this method may raise an general exception on bad day_of_week input
        """
        day_of_week_int=self.__dayOfWeekConvert(day_of_week)
        self.dow_int=DayOfWeekInt(day_of_week_int)
        self.dow_str=day_of_week

    def getDowInt(self):
        """
            return a DayOfWeekInt instance, that represents same day of week as this
        """
        return self.dow_int

    def __dayOfWeekConvert(self,dow_str):
        """
            convert dow_str to an integer that represents it
            dow_str is a string like Monday, Tuesday ...
            see the week_days list to understand day name => integer mapping

        """
        try:
            return WEEK_DAYS.index(dow_str)
        except ValueError:
            raise GeneralException(errorText("GENERAL","INVALID_DAY_OF_WEEK")%dow_str)

class DayOfWeekIntContainer:
    """
        This class used in charge rules to keep multiple day of weeks (multi DayOfWeekInt instances)
    """
    def __init__(self,*day_of_weeks):
        """
            day_of_weeks: list of DayOfWeekInt instances
        """
        self.day_of_weeks=[]
        apply(self.append,day_of_weeks)

    def __iter__(self):
        return iter(self.day_of_weeks)
        
    def append(self,*day_of_weeks):
        """
            day_of_weeks: list of DayOfWeekInt instances
        """

        for day_of_week in day_of_weeks:
            self.day_of_weeks.append(day_of_week)

    def hasOverlap(self, dow_container):
        """
            check if this container has a same day with another container. 
        """
        for dow in self.day_of_weeks:
            if dow in dow_container:
                return True
        return False

    def getDayNames(self):
        """
            return a list of day names, that we contain
        """
        return map(lambda x:x.getDayString(),self.day_of_weeks)
