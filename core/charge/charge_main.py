from core.server import handlers_manager


def init():
    from core.charge.voip_tariff import tariff_main
    tariff_main.init()

    from core.charge.charge_loader import ChargeLoader
    global charge_loader
    charge_loader=ChargeLoader()
    charge_loader.loadAllCharges()
    
    from core.charge.charge_actions import ChargeActions
    global charge_actions
    charge_actions=ChargeActions()

    from core.charge.charge_handler import ChargeHandler
    handlers_manager.getManager().registerHandler(ChargeHandler())
    
def getLoader():
    return charge_loader

def getActionManager():
    return charge_actions
