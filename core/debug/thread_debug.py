from core import defs
import sys,threading

def debug_me():
    if defs.DEBUG_LEVEL>=defs.DEBUG_THREADS:
        sys.settrace(debug_thread_func)
    


def debug_thread_func( frame, event, arg ):

    filename=frame.f_code.co_filename

    if filename.startswith("./") or filename.startswith("/usr/local/IBSng"):
        thread_name=str(threading.currentThread())
        thread_name=thread_name[thread_name.find('(')+1:thread_name.find(',')]
        filename=filename[filename.rfind("/")+1:]
        thread_log_handle=open("/var/log/IBSng/thread_debug_%s.log"%thread_name,"a+")
        thread_log_handle.write("%-10s %-9s %-15s in %-12s:%-5s arg: %-20s\n"%(thread_name,event,frame.f_code.co_name,filename,frame.f_lineno,arg))
        thread_log_handle.close()
        return debug_thread_func
    
    return None
    
