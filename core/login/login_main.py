from core.login.login_handler import LoginHandler
from core.server import handlers_manager

def init():
    handlers_manager.getManager().registerHandler(LoginHandler())
