from core.ibs_exceptions import *
from core.errors import errorText

class RasFactory:
    def __init__(self):
        self.ras_classes={} #{ras_type:ras_class}

    def register(self,ras_class,ras_type):
        if ras_type in self.ras_classes:
            raise IBSException(errorText("RAS","DUPLICATE_TYPE_REGISTRATION")%ras_type)
        self.ras_classes[ras_type]=ras_class

    def getClassFor(self,ras_type):
        try:
            return self.ras_classes[ras_type]
        except KeyError:
            raise IBSException(errorText("RAS","RAS_TYPE_NOT_REGISTERED")%ras_type)

    def hasType(self,ras_type):
        """
            return 1 if "ras_type" is valid and exists and 0 if it's not
        """
        return ras_type in self.ras_classes

    def getAllTypes(self):
        """
            return a list of ras ip's
        """
        return list(self.ras_classes.keys())
