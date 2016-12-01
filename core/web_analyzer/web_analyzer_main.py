from core.server import handlers_manager

def init():
    from core.web_analyzer.web_analyzer_handler import WebAnalyzerHandler
    handlers_manager.getManager().registerHandler(WebAnalyzerHandler())

    from core.web_analyzer.web_analyzer_logger import WebAnalyzerLogger
    global web_analyzer_logger
    web_analyzer_logger = WebAnalyzerLogger()
    
def getAnalyzerLogger():
    return web_analyzer_logger
