from core.server import handlers_manager

def init():
    from core.report import onlines_filter
    onlines_filter.init()

    from core.report.report_handler import ReportHandler
    handlers_manager.getManager().registerHandler(ReportHandler())

    from core.report.report_cleaner import ReportCleaner
    global report_cleaner
    report_cleaner = ReportCleaner()


def getReportCleaner():
    return report_cleaner    
