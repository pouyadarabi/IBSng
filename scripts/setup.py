#!/usr/bin/python
import curses
import sys
import os
import stat
import re

def cursesMain(stdscr):
    setupMainWindow(stdscr)
    menu=MenuWindow(stdscr)
    log=LogWindow(stdscr)
    mainWindow(stdscr,menu,log)
    stdscr.getch()

def main():
    sys.path.append("/usr/local/IBSng")
    curses.wrapper(cursesMain)

def setupMainWindow(stdscr):
    if curses.has_colors():
        curses.init_pair(1,curses.COLOR_WHITE,curses.COLOR_BLACK)
        stdscr.bkgdset(0,curses.color_pair(1))
    stdscr.clear()
    stdscr.box()
    stdscr.addstr(0,0,"IBSng Setup",curses.A_BOLD)
    stdscr.addstr(stdscr.getmaxyx()[0]-1,1,"Copyright Parspooyesh co. (http://www.parspooyesh.com)")
    stdscr.refresh()


###################################
def mainWindow(stdscr,menu,log):
    clearAll(menu,log)
    while True:
        menu.clear()
        menu.setTitle("Main")
        menu.getOption([("1","Install",install),
                         ("2","Change System Password",changeSystemPassword),
                         ("3","Edit IBS Advanced Configuration",notImplemented),
                         ("4","Backup/Restore",notImplemented),
                         ("5","See Onlines",notImplemented),
                         ("x","Exit",exit)],stdscr,menu,log)

#########################################
def notImplemented(stdscr,menu,log):
    log.write("Not Implemented")
    
#######################################
def install(stdscr,menu,log):
    clearAll(menu,log)
    if checkRoot(stdscr,menu,log):
        return
    if checkPygresql(stdscr,menu,log):
        return
    if checkPostgresql(stdscr,menu,log):
        return
    if installEditDefs(stdscr,menu,log):
        return
    if importSqlFiles(stdscr,menu,log):
        return
    if changeSystemPassword(stdscr,menu,log):
        return
    if createLogDir(stdscr,menu,log):
        return
    if apacheConfig(stdscr,menu,log):
        return
    if logrotateConfig(stdscr,menu,log):
        return
    if copyInitFile(stdscr,menu,log):
        return
    installSuccess(stdscr,menu,log)

#######################################
def checkRoot(stdscr,menu,log):
    """
        check if we're runned by root
    """
    if os.getuid()!=0:
        log.write("ERROR: Install should be runned as root")
        return True

#########################################
def checkPygresql(stdscr,menu,log):
    menu.setTitle("Checking Pygresql")
    try:
        import pg
    except ImportError:
        log.write("Error: Pygresql is not installed\n \
                  1-Install postgresql-python rpm on distribution CDs(redhat/fedora on last CD)\n \
                  2-Download and install it from http://www.pygresql.org/")
        menu.getOption([("b","Back to main menu",None)],stdscr,menu,log)
        return True
    log.write("SUCCESS: Pygresql is installed.")
    return False

######################################
def checkPostgresql(stdscr,menu,log):
    """
        return True if the caller should return too, and we return to main menu
        return False to continue the caller method
    """
    while True:
        menu.clear()
        menu.setTitle("Checking Postgresql")
        ch=menu.getOption([("1","Edit Database Parameters",editDBParams),
                   ("2","Test DB Connection and continue",testDB),
                   ("b","Back to main menu",None)],stdscr,menu,log)
        if ch==ord("b"):
            return True
        elif ch==True: #database connection was OK
            return False

def editDBParams(stdscr,menu,log):
    callEditor("/usr/local/IBSng/core/db_conf.py",log)
    menu.clear()
    return

def testDB(stdscr,menu,log):
    try:
        con=getDBConnection()
        con.close()
    except:
        exctype, exc_value = sys.exc_info()[:2]
        if exc_value==None:            
            exc_value=str(exctype)
        log.write("Error occured:\n%s"%exc_value)
        log.write("Make sure you have created database and postgresql user")
        return
    log.write("SUCCESS: Successfully connected to database.")
    return True

def getDBConnection():
    from core import db_conf
    reload(db_conf)
    import pg
    con=pg.connect("IBSng",db_conf.DB_HOST,db_conf.DB_PORT,None,None,db_conf.DB_USERNAME,db_conf.DB_PASSWORD)
    return con
#######################################
def installEditDefs(stdscr,menu,log):
    while True:
        menu.clear()
        menu.setTitle("Editing Advanced Configs")
        ch=menu.getOption([("1","Edit Advanced Configuration",editDefs),
                   ("2","Compile Configuration and continue",compileDefs),
                   ("b","Back to main menu",None)],stdscr,menu,log)
        if ch==ord("b"):
            return True
        elif ch==True: #database connection was OK
            return False
    
def editDefs(stdscr,menu,log):
    callEditor("/usr/local/IBSng/core/defs_lib/defs_defaults.py",log)
    menu.clear()
    return

def compileDefs(stdscr,menu,log):
    ret=os.system("/usr/local/IBSng/core/defs_lib/defs2sql.py -i /usr/local/IBSng/core/defs_lib/defs_defaults.py /usr/local/IBSng/db/defs.sql 1>/dev/null 2>/dev/null")
    if ret!=0:
        log.write("ERROR: File didn't compile successfully\nRecheck config file and try again")
        return
    log.write("SUCCESS: Configuration Compiled Successfully.")
    return True
#######################################
def importSqlFiles(stdscr,menu,log):
    while True:
        menu.clear()
        menu.setTitle("Importing Database Tables")
        ch=menu.getOption([("1","Import Tables And Continue",doImportSqlFiles),
                   ("2","Continue Without Import",None),
                   ("b","Back to main menu",None)],stdscr,menu,log)
        if ch==ord("b"):
            return True
        elif ch==True or ch==ord("2"): 
            return False

def doImportSqlFiles(stdscr,menu,log):
    con=None
    try:
        con=getDBConnection()
        
        doSqlFile(con,"/usr/local/IBSng/db/tables.sql")
        log.write("SUCCESS: Tables Imported")

        doSqlFile(con,"/usr/local/IBSng/db/functions.sql")
        log.write("SUCCESS: Functions Imported")

        doSqlFile(con,"/usr/local/IBSng/db/initial.sql")
        log.write("SUCCESS: Initial Values Imported")

        doSqlFile(con,"/usr/local/IBSng/db/defs.sql")
        log.write("SUCCESS: Advanced Configuraion Imported.")

        con.close()
        return True
    except:
        if con:
            con.close()
        exctype, exc_value = sys.exc_info()[:2]
        if exc_value==None:            
            exc_value=str(exctype)
        log.write("Error occured:\n%s"%exc_value)
        return
    
def doSqlFile(con,file_name):
    content=open(file_name).read(1024*100)
    con.query(content)
    
#######################################
def changeSystemPassword(stdscr,menu,log):
    from core.lib import password_lib
    menu.clear()
    menu.setTitle("Change System Password")
    menu.write("Please Enter System Password:")
    menu.display()
    password=menu.getStr()
    passwd_obj=password_lib.Password(password)
    try:
        con=getDBConnection()
        con.query("update admins set password='%s' where username='system'"%passwd_obj.getMd5Crypt())
        con.close()
        log.write("SUCCESS: Password For System Changed.")
        log.write("You should (re)start IBSng to change take effect.")
        return 
    except:
        if con:
            con.close()
        exctype, exc_value = sys.exc_info()[:2]
        if exc_value==None:            
            exc_value=str(exctype)
        log.write("Error occured:\n%s"%exc_value)
        return

######################################
def createLogDir(stdscr,menu,log):
    lines=callAndGetLines("mkdir /var/log/IBSng")
    if lines:
        log.write("ERROR: Counldn't make log dir.")
        log.write("".join(lines).strip())
    else:
        log.write("SUCCESS: /var/log/IBSng created.")
    lines=callAndGetLines("chmod 770 /var/log/IBSng")

    if lines:
        log.write("ERROR: Counldn't chown log dir.")
        log.write("".join(lines).strip())
    else:
        log.write("SUCCESS: Permission set for /var/log/IBSng.")
        
######################################
def apacheConfig(stdscr,menu,log):
    global apache_conf_dir,apache_username
    apache_conf_dir="/etc/httpd/conf.d"
    apache_username="apache"
    while True:
        menu.clear()
        menu.setTitle("Apache Configuration")
        ch=menu.getOption([("1","Copy ibs.conf to '%s'"%apache_conf_dir,copyApacheConfig),
                   ("2","Chown apache directories to '%s'"%apache_username,changeApacheDirectoryOwners),
                   ("3","Change Apache Config Directory",changeApacheConfigDir),
                   ("4","Change Apache Username",changeApacheUsername),
                   ("5","Continue",None),
                   ("b","Back to main menu",None)],stdscr,menu,log)
        if ch==ord("b"):
            return True
        elif ch==ord("5"): 
            return False

def changeApacheConfigDir(stdscr,menu,log):
    global apache_conf_dir
    menu.clear()
    menu.setTitle("Change Apache Config Directory")
    menu.write("Please Enter Apache Config Directory:")
    menu.display()
    apache_conf_dir=menu.getStr()
    return

def changeApacheUsername(stdscr,menu,log):
    global apache_username
    menu.clear()
    menu.setTitle("Change Apache Username")
    menu.write("Please Enter Apache Username:")
    menu.display()
    apache_username=menu.getStr()
    return

def copyApacheConfig(stdscr,menu,log):
    lines=callAndGetLines("cp -f /usr/local/IBSng/addons/apache/ibs.conf %s"%apache_conf_dir)
    if lines:
        log.write("ERROR: Couldn't copy ibs.conf to %s."%apache_conf_dir)
        log.write("".join(lines).strip())
    else:
        log.write("SUCCESS: ibs.conf copied to %s."%apache_conf_dir)
    return
    
def changeApacheDirectoryOwners(stdscr,menu,log):
    lines=callAndGetLines("chown root:%s /var/log/IBSng"%apache_username)
    if lines:
        log.write("ERROR: Couldn't change owner of /var/log/IBSng to %s"%apache_username)
        log.write("".join(lines).strip())
    else:
        log.write("SUCCESS: Owner of /var/log/IBSng changed.")

    lines=callAndGetLines("chown %s /usr/local/IBSng/interface/smarty/templates_c"%apache_username)
    if lines:
        log.write("ERROR: Couldn't change owner of /usr/local/IBSng/interface/smarty/templates_c to %s"%apache_username)
        log.write("".join(lines).strip())
    else:
        log.write("SUCCESS: Owner of /usr/local/IBSng/smarty/templates_c changed.")
    return
#######################################
def logrotateConfig(stdscr,menu,log):
    global logrotate_conf_dir
    logrotate_conf_dir="/etc/logrotate.d"

    while True:
        menu.clear()
        menu.setTitle("Logrotate Configuration")
        ch=menu.getOption([("1","Copy Logrotate Conf to %s"%logrotate_conf_dir, copyLogrotateConfig ),
                   ("2","Change Logrotate Conf Directory",changeLogrotateConfigDir),
                   ("3","Continue",None),
                   ("b","Back to main menu",None)],stdscr,menu,log)
        if ch==ord("b"):
            return True
        elif ch==ord("3"): 
            return False

def changeLogrotateConfigDir(stdscr,menu,log):
    global logrotate_conf_dir
    menu.clear()
    menu.setTitle("Change Logrotate Config Directory")
    menu.write("Please Enter Logrotate Config Directory:")
    menu.display()
    logrotate_conf_dir=menu.getStr()
    return


def copyLogrotateConfig(stdscr,menu,log):
    lines=callAndGetLines("cp -f /usr/local/IBSng/addons/logrotate/IBSng %s"%logrotate_conf_dir)
    if lines:
        log.write("ERROR: Couldn't copy IBSng logrotate conf to %s."%logrotate_conf_dir)
        log.write("".join(lines).strip())
    else:
        log.write("SUCCESS: IBSng logrotate conf copied to %s."%logrotate_conf_dir)
    return

#######################################
def copyInitFile(stdscr,menu,log):
    while True:
        menu.clear()
        menu.setTitle("Copy Init.d file")
        ch=menu.getOption([("1","Copy Redhat init file to /etc/init.d",copyRHInitFile),
                   ("2","Set IBSng to start on reboot",chkconfigInit),
                   ("3","Continue",None),
                   ("b","Back to main menu",None)],stdscr,menu,log)
        if ch==ord("b"):
            return True
        elif ch==True or ch==ord("3"): 
            return False

def copyRHInitFile(stdscr,menu,log):
    lines=callAndGetLines("cp -f /usr/local/IBSng/init.d/IBSng.init.redhat /etc/init.d/IBSng")
    if lines:
        log.write("ERROR: Couldn't copy init file.")
        log.write("".join(lines).strip())
    else:
        log.write("SUCCESS: Init file copied.")
    return

def chkconfigInit(stdscr,menu,log):
    lines=callAndGetLines("/sbin/chkconfig IBSng on")
    if lines:
        log.write("ERROR: Chkconfig returned error.")
        log.write("".join(lines).strip())
    else:
        log.write("SUCCESS: IBSng will start on reboot.")
    return
#######################################
def installSuccess(stdscr,menu,log):
    menu.clear()
    menu.setTitle("Installation Completed")
    log.write("SUCCESS: Installation Completed.")
#    log.write("If you use IBSng please register yourself")
#    log.write("in http://ibs.sf.net/register")
    ch=menu.getOption([("b","Back to main menu",None)],stdscr,menu,log)
    
#######################################
def exit(stdscr,menu,log):
    sys.exit()
#######################################
def clearAll(menu,log):
    menu.clear()
    log.clear()
#######################################
def callAndGetLines(command):
    fd=os.popen("%s 2>&1"%command,"r")
    lines=fd.readlines()
    fd.close()
    return lines
####################################
def callEditor(file_name,log):
    for editor in ["nano -w","mcedit","vi"]:
        ret=os.system("%s %s"%(editor,file_name))
        if ret==0:
            return
    log.write("ERROR: No editor found")
#######################################
class MenuWindow:
    def __init__(self,stdscr):
        self.stdscr=stdscr
        self.width=45
        self.height=12
        self.begin_x=3
        self.begin_y=2
        self.__setupWindow()

    def __setupWindow(self):
        self.window=self.stdscr.subwin(self.height,self.width,self.begin_y,self.begin_x)
        self.window.clear()

    def clear(self):
        self.window.clear()

    def display(self):
        self.window.addstr(self.height-2,5,"==>")
        self.window.refresh()

    def setTitle(self,title):
        """
            set menu title to "title"
        """
        self.window.box()
        self.window.addstr(0,0,title,curses.A_BOLD)
    
    def addOptions(self,options):
        """
            add options to menu options
            options should be a list in format [("key","description")]
        """
        y=1
        for option in options:
            key=option[0]
            desc=option[1]
            self.__addOption(y,key,desc)
            y+=1

    def __addOption(self,y,key,desc):
        self.window.addstr(y,2,key,curses.A_UNDERLINE)
        self.window.addstr(y,5,desc)

    def getChar(self):
        self.window.move(self.height-2,8)
        curses.echo()
        ch=self.window.getch()
        curses.noecho()
        return ch

    def getStr(self):
        self.window.move(self.height-2,8)
        curses.echo()
        _str=self.window.getstr()
        curses.noecho()
        return _str

    def getOption(self,options,stdscr,menu,log):
        """
            options should be in format ("key","desc","method")
        """
        self.addOptions(options)
        self.display()
        while True:
            ch=self.getChar()
            for key,desc,method in options:
                if ord(key)==ch:
                    break
            else:
                curses.beep()
                log.write("Invalid input %s"%chr(ch))
                continue
            break
        if method!=None:
            return apply(method,[stdscr,menu,log])
        else:
            return ch

    def write(self,_str,y=1,x=2):
        self.window.addstr(y,x,_str)

class LogWindow:
    def __init__(self,stdscr):
        self.stdscr=stdscr
        self.begin_x=3
        self.begin_y=16
        self.lasty=1
        self.__setupWindow()

    def __setupWindow(self):
        maxy,maxx=self.stdscr.getmaxyx()
        self.window=self.stdscr.subwin(maxy-self.begin_y-2,maxx-self.begin_x-2,self.begin_y,self.begin_x)
        self.window.scrollok(True)
        self.window.clear()


    def clear(self):
        self.lasty=0
        self.window.clear()

    def write(self,_str):
        """
            write line(s) to log window
        """
        map(self.__write,_str.split("\n"))      
    
    def __write(self,_str):
        self.window.addstr(self.lasty,0,_str)
        if self.lasty<(self.stdscr.getmaxyx()[0]-self.begin_y-3):
            self.lasty+=1
        else:
            self.window.scroll()
        self.display()

    def display(self):
        self.window.refresh()

    
main()
