from core.server import handlers_manager

def init():
    from core.charge.voip_tariff.tariff_actions import TariffActions
    global actions_manager
    actions_manager=TariffActions()

    from core.charge.voip_tariff.tariff_loader import TariffLoader
    global tariff_loader
    tariff_loader=TariffLoader()
    tariff_loader.loadAllTariffs()
    
    from core.charge.voip_tariff.tariff_handler import TariffHandler
    handlers_manager.getManager().registerHandler(TariffHandler())
    
def getActionsManager():
    return actions_manager

def getLoader():
    return tariff_loader