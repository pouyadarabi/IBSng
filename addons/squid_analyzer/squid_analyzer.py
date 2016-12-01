#!/usr/bin/python -O
"""
    Squid Analyzer is a daemon to feed the IBSng Accounting System
    with user's(ip) visited URLs, captured and manipulated from
    Squid Cache server access log.

    Initialzer for main parts. there is a precedence which must be kept
    for init separate parts:
        1 - Conf Holder
        2 - Event Logger
        2 - Log Watcher
        2 - Filter Module
        3 - Request Wrapper
        4 - Feeder

    These Signals will be handled:
        - SIGUSR1 : inform the analyzer of squid log rotation.
        - SIGUSR2 : the squid_analyzer log file has been rotated.
        - SIGTERM : Quit all operations and exit.
"""
import os,sys
from analyze_conf import *
from analyze_exceptions import *
from analyze_feeder import *

def init():
    feeder = AnalyzeFeeder()
    feeder.doFeed()

def writeToPidFile(pid):
    fd = open('/var/run/squid_analyzer.pid', "w+")
    fd.write(str(pid))
    fd.close()

if __name__ == '__main__':
    print "forking ..."       
    pid=os.fork()
    print "Web Analyzer daemon started with pid=%d"%pid
    if pid == 0:
        try:
            init()
        except:
            logException()
            raise
    else:
        writeToPidFile(pid)
