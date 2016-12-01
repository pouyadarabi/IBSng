import ibs_agi

def init():
    ibs_agi.getStateMachine().registerState("CHOOSE_LANGUAGE",chooseLanguage)

def chooseLanguage():
    if ibs_agi.getConfig().getValue("language")!="": #language already selected 
        return 
    elif len(ibs_agi.getLangManager().getAllLanguages())==1:
        lang_obj=ibs_agi.getLangManager().getLanguageByIndex(0)
    else:
        digit=''
        while not digit:
            i=0
            for lang_code,lang_obj in ibs_agi.getLangManager().getAllLanguages():
                digit=lang_obj.sayLanguageOption(i+1)
                if digit:
                    break
                i+=1

            if not digit:
                digit=ibs_agi.getAGI().wait_for_digit(5000)
            
            if not digit:
                ibs_agi.getLangManager().getLanguageByIndex(0).sayPrompt("no_digit_entered")
                continue
            else:
                try:
                    lang_obj=ibs_agi.getLangManager().getLanguageByIndex(int(digit)-1)
                except IndexError:
                    continue

                break

    ibs_agi.getConfig().setValue("language",lang_obj.getLanguageCode())

    