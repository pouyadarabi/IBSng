import re,os
import analyze_exceptions

split_url_pattern=re.compile("(.*://)?([^/]+)(.*)")

#################
def splitUrl(url):
    """
        split a url to find host, directory and file name
    """
    match_obj = split_url_pattern.match(url)
    if match_obj == None:
        analyze_exceptions.toLog("splitUrl: url '%s' is invalid"%url)
        return ("","","","")
    else:
        protocol, host, path = match_obj.groups()
        
        if protocol == None:
            protocol == ""
        
        filename_idx=path.rfind("/")
        if filename_idx == -1 or filename_idx == len(path)-1: 
            directory = path
            filename = ""
        else:
            directory = path[:filename_idx]
            filename = path[filename_idx:]
        
        return (protocol, host, directory, filename)

################################ Timing 
def synchTime(server_addr):
    """
        Just get the date on IBSng server, and set it on local system
    """
    buff = os.popen('ssh %s date'%server_addr)
    ret = os.system('date -s %s'%buff[0].strip())
    if not ret: # evaluated successfully
        ret = os.system('hwclock --systohc')
    else:
        toLog("synchTime, failed")
    return
    