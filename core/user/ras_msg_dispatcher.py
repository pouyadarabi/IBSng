from core.ibs_exceptions import *
from core.user import user_main
from core.log_console.console_main import getLogConsole

class RasMsgDispatcher:

    def dispatch(self,ras_msg):
        dispatch_methods={"INTERNET_AUTHENTICATE":self._internetAuthenticate,
                          "INTERNET_STOP":self._internetStop,
                          "INTERNET_UPDATE":self._internetUpdate,
                          "PERSISTENT_LAN_AUTHENTICATE":self._planAuthenticate,
                          "PERSISTENT_LAN_STOP":self._planStop,
                          "VOIP_AUTHENTICATE":self._voipAuthenticate,
                          "VOIP_AUTHORIZE":self._voipAuthorize,
                          "VOIP_STOP":self._voipStop,
                          "VOIP_UPDATE":self._voipUpdate
                         }

        action=ras_msg.getAction()
        return apply(dispatch_methods[action],[ras_msg])

    def _internetAuthenticate(self,ras_msg):
        getLogConsole().logAuthRasMsg(ras_msg)

        try:
            user_main.getOnline().internetAuthenticate(ras_msg)

            getLogConsole().logAuthRasMsgSuccess(ras_msg)

            return True

        except IBSError,e:
            user_main.getDialerErrors().applyToRasMsg(ras_msg, e)

            getLogConsole().logAuthRasMsgFailure(ras_msg, e)

            return False
            

    def _internetStop(self, ras_msg):
        getLogConsole().logStopRasMsg(ras_msg)

        return user_main.getOnline().internetStop(ras_msg)
        
    def _internetUpdate(self,ras_msg):
        getLogConsole().logUpdateRasMsg(ras_msg)

        return user_main.getOnline().updateUser(ras_msg)

    def _planAuthenticate(self,ras_msg):
        getLogConsole().logAuthRasMsg(ras_msg)
        try:

            user_main.getOnline().persistentLanAuthenticate(ras_msg)

            getLogConsole().logAuthRasMsgSuccess(ras_msg)

            return True
        except IBSError, e:
            getLogConsole().logAuthRasMsgFailure(ras_msg, e)

            return False

    def _planStop(self,ras_msg):
        getLogConsole().logStopRasMsg(ras_msg)

        return user_main.getOnline().persistentLanStop(ras_msg)

    def _voipAuthenticate(self,ras_msg):
        getLogConsole().logAuthRasMsg(ras_msg)

        try:
            user_main.getOnline().voipAuthenticate(ras_msg)

            getLogConsole().logAuthRasMsgSuccess(ras_msg)

            return user_main.getVoIPErrors().applySuccess(ras_msg)
        except IBSError, e:
            getLogConsole().logAuthRasMsgFailure(ras_msg, e)

            return user_main.getVoIPErrors().applyFailure(ras_msg, e)

    def _voipAuthorize(self,ras_msg):
        getLogConsole().logAuthRasMsg(ras_msg)

        try:
            user_main.getOnline().voipAuthorize(ras_msg)

            getLogConsole().logAuthRasMsgSuccess(ras_msg)

            return user_main.getVoIPErrors().applySuccess(ras_msg)

        except IBSError, e:
            getLogConsole().logAuthRasMsgFailure(ras_msg, e)

            return user_main.getVoIPErrors().applyFailure(ras_msg, e)
            
    def _voipStop(self,ras_msg):
        getLogConsole().logStopRasMsg(ras_msg)

        return user_main.getOnline().voipStop(ras_msg)

    def _voipUpdate(self,ras_msg):
        getLogConsole().logUpdateRasMsg(ras_msg)

        try:
            user_main.getOnline().updateUser(ras_msg)
            user_main.getVoIPErrors().applySuccess(ras_msg)
        except IBSError, e:
            user_main.getVoIPErrors().applyFailure(ras_msg, e)
            
