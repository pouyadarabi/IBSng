from core.server import handlers_manager

def init():
    from core.log_console.log_console import LogConsole
    global log_console
    log_console = LogConsole()

    from core.log_console.log_console_handler import LogConsoleHandler
    handlers_manager.getManager().registerHandler(LogConsoleHandler())


def getLogConsole():
    return log_console

