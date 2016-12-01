from core.lib.general import *
import os
import imp


def init():
    global plugin_loader
    plugin_loader=PluginLoader()
    
def loadPlugins(directory):
    """
        load plugins in "directory"
    """
    return plugin_loader.initPlugins(directory)

class PluginLoader:
    def initPlugins(self,directory):
        """
            directory(text): directory path to search for plugins
            
            return all loaded module object
            
            call init function of all *.py files in "directory"
            they must register themselves somewhere
            ex. user plugins should user plugins.registerUserPlugin
        """
        py_files=self.__getPyFiles(directory)
        modules=self.__loadModules(py_files,directory)
        self.__callInits(modules)
        return modules

    def __callInits(self, modules):
        """
            call init function of all modules in "modules" dic
        """
        for obj in modules.itervalues():
            try:
                obj.init()
            except AttributeError: #no init defined
                pass
            except:
                logException(LOG_ERROR,"PluginLoader.__callInits")
    
    def __loadModules(self,file_list,directory):
        """
            load and import all files in "file_list" in path "directory"
            return a dic of loaded modules in format {module_name:module_obj}
        """
        modules={}
        for file_name in file_list:
            file=None
            try:
                module_name=file_name[:-3] #remove trailing .py
                (file,pathname,desc)=imp.find_module(module_name,[directory])
                modules[module_name]=imp.load_module(module_name,file,pathname,desc)
            except:
                if file!=None:
                    file.close()
                logException(LOG_ERROR,"PluginLoader.__loadModules")
        return modules

    def __getPyFiles(self,directory):
        """
            return list of all .py files in directory
        """
        return filter(lambda name: name.endswith(".py"),self.__getFilesList(directory))

    def __getFilesList(self,directory):
        """
            return list of all files in "directory"
        """
        try:
            return os.listdir(directory)
        except OSError:
            logException(LOG_ERROR,"PluginLoader.__getFilesList")
            return []