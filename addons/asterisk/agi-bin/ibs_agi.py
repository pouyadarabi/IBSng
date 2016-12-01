#!/usr/bin/python
import sys
from lib.error import *
import signal

USERNAME_LENGTH=6
MAX_PASSWORD_LENGTH=6
MAX_DESTINATION_DIGITS=16

ASTERISK_PASSWORD="asterisk"
REQUESTED_LANGUAGES=["en"]

SOUNDS_ROOT="/var/lib/asterisk/ivr/"
USER_GREETINGS_ROOT="/var/lib/asterisk/greetings/"
LOG_FILE="/var/log/IBSng/ibs_agi.log"
STATE_PLUGINS="/var/lib/asterisk/agi-bin/states"

IBSNG_SERVER=("127.0.0.1",1235)

ALL_ESCAPE='1234567890*#'

def init():
    initSignalHandlers()
    initConfig()
    initAGI()
    initLanguageManager()
    initStateMachine()
    try:
        getStateMachine().start()
    except SystemExit:
        if getConfig().getValue("debug"):
            toLog("Exit on user hangup")
    except:
        logException()
#######################
def initSignalHandlers():
    signal.signal(signal.SIGHUP, signal.SIG_IGN)
    signal.signal(signal.SIGTERM, signal.SIG_IGN)
    signal.signal(signal.SIGINT, signal.SIG_IGN)
    signal.signal(signal.SIGSEGV, signal.SIG_IGN)

#######################
def initAGI():
    global agi
    from lib.agilib import agilib
    agi=agilib.AGI()

def getAGI():
    return agi
    
def initConfig():
    global config
    config=Config()
    
def getConfig():
    return config
    
def initLanguageManager():
    global lang_manager
    from lib.language_manager import LanguageManager
    lang_manager=LanguageManager()

def getLangManager():
    return lang_manager
    
def getSelectedLanguage():
    return getLangManager().getSelectedLanguage()


def initStateMachine():
    global state_machine
    from lib.state_machine import StateMachine
    state_machine=StateMachine("MAIN")
    from lib.plugin_loader import PluginLoader
    plugin_loader=PluginLoader()
    plugin_loader.initPlugins(getConfig().getValue("state_plugins"))

def getStateMachine():
    return state_machine
#######################

class Config:
    def __init__(self):
        self.language=''
        self.username=''
        self.password=''
        self.caller_id=''
        self.unique_id=''
        self.channel=''

        self.asterisk_password=ASTERISK_PASSWORD
        self.IBSng_server=IBSNG_SERVER
        
        self.username_length=USERNAME_LENGTH
        self.max_password_length=MAX_PASSWORD_LENGTH
        self.max_destination_digits=MAX_DESTINATION_DIGITS
        self.all_escape=ALL_ESCAPE
        self.requested_languages=REQUESTED_LANGUAGES

        self.sounds_root=SOUNDS_ROOT
        self.user_greetings_root=USER_GREETINGS_ROOT
        self.log_file=LOG_FILE
        self.state_plugins=STATE_PLUGINS

        self.retry=3
        self.dial_timeout=60

        self.pre_authenticated=False
        self.authenticated=False
        self.authorized=False

        self.debug=True

        
    def getValue(self,name):
        return getattr(self,name)

    def setValue(self, name, value):
        setattr(self,name,value)
    
    def getDialString(self, destination):
        return "H323/3344#%s@192.168.1.10|%s|H"%(destination,self.getValue("dial_timeout"))
#       return "SIP/33344#%s@192.168.1.10|%s|H"%(destination,self.getValue("dial_timeout"))
