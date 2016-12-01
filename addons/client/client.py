#!/usr/bin/python

import xmlrpclib
import sys
import os


def printUsage():
    print """
        Usage: client.py <filename> <system password> [-fo]
        
            filename: filename containing python codes to run in running ibs
            -f: tell server to read from file instead of sending the file content
                useful for large files
            
            -o: tell server not to collect output and just execute the code
                this causes server not to fork for collecting output.
                Forking make problem with db connections and has some other issues
    
    """
    

def readFile(file_name):
    fd=open(file_name)
    contents=fd.read(os.stat(file_name)[6])
    fd.close()
    return contents

def sendRequest(contents, system_password, read_from_file = False, no_output = False):
    server=xmlrpclib.ServerProxy("http://localhost:1235")
    args={"command":contents,
          "auth_name":"system",
          "auth_pass":system_password,
          "auth_type":"ADMIN",
          "auth_remoteaddr":"127.0.0.1"}
    
    if read_from_file:
        args["read_from_file"] = True

    if no_output:
        args["no_output"] = True
    
    return getattr(server,"util.runDebugCode")(args)


def main():
    if len(sys.argv) not in [3,4,5]:
        printUsage()
        sys.exit(1)

    file_name=sys.argv[1]
    system_password=sys.argv[2]
    
    read_from_file = False
    no_output = False
    
    if "-f" in sys.argv:
        read_from_file = True
    
    if "-o" in sys.argv:
        no_output = True
    
    if read_from_file:
        contents=os.path.realpath(file_name)
    else:
        contents=readFile(file_name)

    result=sendRequest(contents, system_password, read_from_file, no_output)

    print result

if __name__=="__main__":
    main()
    
