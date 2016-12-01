import ibs_agi
import os

def init():
    ibs_agi.getStateMachine().registerState("CHANGE_GREETING",changeGreeting)

def changeGreeting():
    """
        record a greeting and put it in users greetings directory
    """
    ibs_agi.getSelectedLanguage().sayPrompt("pre_change_greeting")
    filename="%s%s"%(ibs_agi.getConfig().getValue("user_greetings_root"),ibs_agi.getConfig().getValue("username"))
    ibs_agi.getAGI().appexec("Record","%s.gsm|7|60"%filename)
    ibs_agi.getSelectedLanguage().sayPrompt("change_greeting_success")