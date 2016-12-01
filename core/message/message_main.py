from core.server import handlers_manager


def init():
    from core.message import message_actions
    global message_action_manager
    message_action_manager = message_actions.MessageActions()

    from core.message.message_handler import MessageHandler
    handlers_manager.getManager().registerHandler(MessageHandler())

def getActionsManager():
    return message_action_manager


