import os,sys

"""
    This file contains:
        - config scheme, wich defines what vars will be available at the run time,
        - Configurations Interface, provides get/set functionality over config vars

        and routines to handle conf related operations
"""
class Config:
    """
        The Global Scheme for Squid Ananlyzer Configurations
    """
    def __init__(self):
        self.version='P.0.2'
      
    def getValue(self,name):
        return getattr(self,name)

    def setValue(self, name, value):
        setattr(self,name,value)

class AnalyzeConfig(Config):
    def __init__(self):
        #Config.__ini__(self)
        self.default_conf_path="/usr/local/IBSng/addons/squid_analyzer/conf/squid_analyzer.conf"
        self.doInitConf()
        
    def doInitConf(self):
        lines = self.__getConfContent(self.__validateConfFile(self.default_conf_path))
        if not len(lines):
            raise "ERROR: Conf file contains no line"
            sys.exit(-1)
        
        conf_dict = self.__parseConfLine(lines)
        for item in conf_dict:
            self.setValue(item, conf_dict[item])
    
    def __validateConfFile(self, passed_conf_path):
        """
            We assume that at least the default conf file is present.
        """
        if os.path.exists(passed_conf_path) and os.path.isfile(passed_conf_path):
            return passed_conf_path
        else:
            print "ERROR: squid_analyzer.conf File, not fount. Exiting"
            sys.exit(-1)
            

    def __getConfContent(self, file_path):
        try:
            fd=open(file_path)
            lines = fd.readlines()
            fd.close()
            return lines
        except:
            logException()
            sys.exit(-1)
            
    def __parseConfLine(self,lines):
        CONF_NAME=0
        CONF_VAL=1

        _dict={}
        for line in lines:
            if line.startswith('#') or len(line)<=1:
                continue
        
            nv_pair = line.strip().split('=')
            if nv_pair[CONF_VAL].isdigit():
                nv_pair[CONF_VAL] = int(nv_pair[CONF_VAL])
            
            _dict[nv_pair[CONF_NAME]]=nv_pair[CONF_VAL]
            
        return _dict
    
def getConf(cname):
    if "conf_holder" not in globals():
        global conf_holder
        try:
            conf_holder = AnalyzeConfig()
        except:
            raise
    return conf_holder.getValue(cname)
