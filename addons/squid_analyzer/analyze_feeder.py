import signal, time

from analyze_conf import *
from analyze_exceptions import *
from analyze_filters import *
from analyze_request import *

from log_watcher import SquidLogWatcher
from analyze_lib import synchTime



class AnalyzeFeeder:
    def __init__(self):
        self.logManipulator = LogPrepare()
        self.requester = RequestWrapper()
        self.squidLogWatcher = SquidLogWatcher()
        self.exit = False

        self.setSignalHandler()
        if getConf("SYNCH_TIME"):
            toLog("Synching local time with IBSng server time ...")
            synchTime(getConf("IBSNG_SERVER_IP"))
        
    def setSignalHandler(self):
        signal.signal(signal.SIGUSR1, self.__signalHandler)
        signal.signal(signal.SIGUSR2, self.__signalHandler)
        signal.signal(signal.SIGTERM, self.__signalHandler)

    def __signalHandler(self,signum, frame):
        if signum == signal.SIGUSR1 : # squid log got rotated
            self.squidLogWatcher.rotateHandler()

        elif signum == signal.SIGUSR2: # analyzer log got rotated
            toLog('reopenfd')

        elif signum == signal.SIGTERM : # stop all
            toLog('sigTerm recieved, force quiting ...')
            self.quit()

    def quit(self):
        toLog('quit call on feed')
        self.exit = True
        self.squidLogWatcher.quitMonitor()
        self.requester.quitSendLoop()
        self.requester.join()

    def doFeed(self):
        
        if getConf('DEBUG'):
            toLog("Starting main feed loop ...")
        while not self.exit:
            try:
                time.sleep(getConf("FEED_DELAY"))
                data = self.squidLogWatcher.getNextLines(getConf("LINES_PER_READ"))
                if getConf('DEBUG')==2:
                    toLog('captured %s lines from logWrapper'%len(data))

                if(len(data)):
                    data = self.logManipulator.prepare(data)
                    if getConf('DEBUG')==2:
                        toLog(' %s ip records prepared'%len(data))
                    feedback = self.requester.putInQueue(data)
            except:
                logException()

        toLog("over all are finished, babye ;)")
