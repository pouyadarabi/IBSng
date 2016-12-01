from core.server import handlers_manager

def init():
    from core.util.util_handler import UtilHandler
    handlers_manager.getManager().registerHandler(UtilHandler())

