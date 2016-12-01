import signal
import sys

def timeoutExit(signum, frame): #@UnusedVariable
    sys.exit(-1)

def setupSigHandler():
    signal.signal(signal.SIGALRM, timeoutExit)

def shouldExitIn(timeout):
    """
        Make sure that script will exit at "timeout" seconds from now
    """
    setupSigHandler()
    signal.alarm(timeout)
