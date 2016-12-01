#!/usr/bin/python

import sys
sys.path.append("/usr/local/IBSng")
from def_var import RawDefVar

class Def2Sql:
    def __init__(self,python_file):
        self.python_file=python_file
        self.importPYFile()
        self.listVars()
        self.createDefsVarObjList()

    def importPYFile(self):
        dir_name,module_name=self.__getModuleName()
        self.module_obj=__import__(module_name)

    def __getModuleName(self):
        if not self.python_file.endswith(".py"):
            raise Exception("Python modules should be .py")
        last_slash=self.python_file.rfind("/")
        if last_slash==-1:
            return None,self.python_file[:-3]
        else:
            return self.python_file[:last_slash],self.python_file[last_slash+1:-3]
    
    def listVars(self):
        self.members=dir(self.module_obj)
    
    def createDefsVarObjList(self):
        self.var_list=[]
        for var_name in self.members:
            if var_name.startswith("__"): 
                continue
            value=getattr(self.module_obj,var_name)
            self.var_list.append(RawDefVar(var_name,value))

    def getInsertQuery(self):
        query=""
        for def_var in self.var_list:
            query+=def_var.insertToDefsQuery()+"\n"
        return query

    def getUpdateQuery(self):
        query=""
        for def_var in self.var_list:
            query+=def_var.updateDefsQuery()+"\n"
        return query


def checkArgs():
    if len(sys.argv)!=4 or (sys.argv[1]!="-i" and sys.argv[1]!="-u"):
        printUsage()
        sys.exit(1)

def printUsage():
    print """
defs2sql.py: Utility to convert IBS python defs file to sql script
Usage: defs2sql.py <-i|-u> <python_file.py> <sql_file.sql>
       -i : use insert queries
       -u : use update queries
               
       python_file.py : defs variables in python format
       sql_file.sql : sql scripts to be created
"""


def write2sqlfile(query):
    fd=open(sys.argv[3],"w+")
    fd.write(query)
    fd.close()
                

def main():
    checkArgs()
    def2sql=Def2Sql(sys.argv[2])
    if sys.argv[1]=="-i":
        query=def2sql.getInsertQuery()
    else:
        query=def2sql.getUpdateQuery()
    write2sqlfile(query)


main()