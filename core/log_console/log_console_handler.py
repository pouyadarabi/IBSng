from core.server import handler
from core.log_console import console_main

class LogConsoleHandler(handler.Handler):
    def __init__(self):
        handler.Handler.__init__(self, "log_console")
        self.registerHandlerMethod("getConsoleBuffer")

    def getConsoleBuffer(self, request):
        request.needAuthType(request.ADMIN)
        requester=request.getAuthNameObj()
        requester.canDo("SEE CONNECTION LOGS")
        return console_main.getLogConsole().getBufferFormatted(request.getDateType())