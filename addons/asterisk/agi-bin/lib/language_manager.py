from lib.error import *
import ibs_agi

class LanguageManager:
    def __init__(self):
        self.languages=[]
        self.requested_languages=ibs_agi.getConfig().getValue("requested_languages")
        self.__initLanguages()
    
    def __initLanguages(self):
        for lang in self.requested_languages:
            try:
                languages=__import__("languages.%s"%lang)
                lang_module=getattr(languages,lang)
                lang_class=getattr(lang_module,lang)
                lang_obj=apply(lang_class,[])
                self.languages.append((lang,lang_obj))
            except ImportError:
                logException("Can't find language %s"%lang)
                
    def getAllLanguages(self):
        """
            return a list of tuples, containing all available languages
            return list format is [(lang_code,lang_obj),...]
        """
        return self.languages

    def getLanguage(self, language_code):
        """
            return language object of language_code or None if language is not available
        """
        for (lang_code,lang_obj) in self.getAllLanguages():
            if lang_code==language_code:
                return lang_obj
        return None
    
    def getLanguageByIndex(self, language_index):
        """
            return language in index "language_index"
            may raise an exception if index is invalid
        """
        return self.languages[language_index][1]

    def getSelectedLanguage(self):
        return self.getLanguage(ibs_agi.getConfig().getValue("language"))
        