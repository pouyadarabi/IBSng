from core.threadpool import thread_main
import time

def sleep():
	time.sleep(60)

for i in range(10):
	thread_main.runThread(sleep,[],"event")
