import ibs_agi
import os
from lib.error import *

def init():
    ibs_agi.getStateMachine().registerState("GREETING",greeting)

def greeting():
    say_language_greeting=sayUserGreeting()
    
    if say_language_greeting:
        ibs_agi.getLangManager().getLanguageByIndex(0).sayGreeting()

def sayUserGreeting():
    """
        say user greeting if available
        return True if greeting was not available for user
        return False if greeting was played
    """
    if ibs_agi.getConfig().getValue("authenticated"):
        filename="%s%s"%(ibs_agi.getConfig().getValue("user_greetings_root"),ibs_agi.getConfig().getValue("username"))
        try:
            os.stat("%s.gsm"%filename)
        except OSError:
            return True
        else:
            ibs_agi.getAGI().stream_file(filename,ibs_agi.ALL_ESCAPE)
            return False

    return True