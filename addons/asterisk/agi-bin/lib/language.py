import ibs_agi
from lib.error import *

class Language:

    MENU_STATES={1:"REDIAL_LAST_NUMBER",
                2:"FAST_DIAL",
                3:"MODIFY_FAST_DIAL",
                4:"CREDIT_ANNOUNCEMENT",
                5:"CHANGE_PASSWORD",
                6:"ADD_CALLERID_AUTHENTICATION",
                7:"DELETE_CALLERID_AUTHENTICATION",
                8:"CHANGE_GREETING"}

    MENU_PROMPTS={1:"menu_redial",
                 2:"menu_fast_dial",
                 3:"menu_modify_fast_dial",
                 4:"menu_credit_announcement",
                 5:"menu_change_password",
                 6:"menu_add_callerid_authentication",
                 7:"menu_delete_callerid_authentication",
                 8:"menu_change_greeting"}
    
    def __init__(self, language_code, prompts):
        """
            language_code(string): two letter language code
        """
        self.language_code=language_code
        self.prompts=prompts #prompt_name:[list of files] language should use this
        self.default_prompts={"get_username":[],
                      "get_username_again":[],
                      "get_password":[],
                      "pre_say_remaining_credit":[],
                      "post_say_remaining_credit":[],
                      "get_destination":[],
                      "get_destination_again":[],
        
                      "pre_language_option":[],
                      "post_language_option":[],

                      "pre_say_remaining_time":[],
                      "post_say_remaining_time":[],
                      
                      "pre_say_talked_duration":[],
                      "post_say_talked_duration":[],

                      "pre_say_used_credit":[],
                      "post_say_used_credit":[],
                      
                      "no_digit_entered":["no_digit_entered"],

                      "get_old_password":["enter_old_password"],
                      "get_new_password":["enter_new_password"],
                      "old_password_incorrect":["incorrect_password"],
                      "change_password_failure":["change_password_failure"],
                      "change_password_success":["change_password_success"],

  
                      "invalid_callerid":["invalid_callerid"],
                      "add_callerid_authentication_success":["add_callerid_authentication_success"],
                      "add_callerid_authentication_failure":["add_callerid_authentication_failure"],


                      "delete_callerid_authentication_success":["delete_callerid_authentication_success"],
                      "delete_callerid_authentication_failure":["delete_callerid_authentication_failure"],
                      "delete_callerid_authentication_not_exists":["delete_callerid_authentication_not_exists"],
                

                      "pre_change_greeting":["pre_change_greeting"],
                      "change_greeting_success":["change_greeting_success"],
                      "change_greeting_failure":["change_greeting_failure"],


                      "enter_fast_dial_index":["enter_fast_dial_index"],
                      "pre_get_fast_dial_destination":[],
                      "post_get_fast_dial_destination":[],

                      "add_destination_to_fast_dial_failure":["add_destination_to_fast_dial_failure"],

                      "pre_add_destination_to_fast_dial_success":["destination"],
                      "mid_add_destination_to_dast_dial_success":["in_index"],
                      "post_add_destination_to_dast_dial_success":["saved"],
                      
                      "pre_confirm_fast_dial":["key"],
                      "mid_confirm_fast_dial":["for_calling"],
                      "post_confirm_fast_dial":["press"],
                      
                      "authentication_failed":["authentication_failed"],

                      #error prompts

                      "destination_busy":["destination_busy"],
                      "destination_noanswer":["destination_out_of_service"],
                      
                      "destination_incorrect":["destination_incorrect"],
                      "destination_out_of_service":["destination_out_of_service"],

                      "invalid_username":["invalid_username"],
                      "incorrect_password":["incorrect_password"],
                      "account_in_use":["account_in_use"],
                      "credit_finished":["credit_finished"],
                      "account_expired":["account_expired"],
                      "login_from_caller_id_denied":["login_from_caller_id_denied"],
                      "account_locked":["account_locked"],
                      "unknown_problem":["unknown_problem"],
                      
                      #menu prompts
                      "pre_menu_prompt":["number"],
                      "post_menu_prompt":["for"],
                      
                      "menu_redial":["menu_redial"],
                      "menu_fast_dial":["menu_fast_dial"],
                      "menu_modify_fast_dial":["menu_modify_fast_dial"],
                      "menu_credit_announcement":["menu_credit_announcement"],
                      "menu_change_password":["menu_change_password"],
                      "menu_add_callerid_authentication":["menu_add_callerid_authentication"],
                      "menu_delete_callerid_authentication":["menu_delete_callerid_authentication"],
                      "menu_change_greeting":["menu_change_greeting"],
                      "menu_return":["menu_return"]

                    } #prompt_name:[list of files]


    def getLanguageCode(self):
        return self.language_code

    def _getLanguageRoot(self):
        return "%s%s/"%(ibs_agi.getConfig().getValue("sounds_root"),self.getLanguageCode())

    def _getFilePath(self, filename):
        return "%s%s"%(self._getLanguageRoot(),filename)

    #######################
    def sayNumber(self, number, escape=ibs_agi.ALL_ESCAPE):
        """
            say number until one of escape digits pressed. return the digit pressed
            return empty string if no digits was pressed until end of prompt
        """
        number=long(number)
        return self.sayFiles(self.sayNumberCreateList(number))

    def sayNumberCreateList(self, number):
        """
            number(integer): number that list will be created for    
        
            should return a list of file names that should be played in order
            to say number
        """
        return []

    def sayDigit(self, digit, escape=ibs_agi.ALL_ESCAPE):
        """
            Say Digit
        """
        return ibs_agi.getAGI().stream_file(self._getFilePath(digit),escape)
        
    def sayDigits(self, digits, escape=ibs_agi.ALL_ESCAPE):
        """
            say all digits one by one. return key pressed or empty string
        """
        for digit in digits:
            ret=self.sayDigit(digit)
            if ret:
                return ret
        return ""

    ######################
    def sayGreeting(self):
        return self.sayFile("greeting")

    def sayLanguageOption(self, lang_index):
        for f in [lambda:self.sayPrompt("pre_language_option"),
                  lambda:self.sayDigit(lang_index),
                  lambda:self.sayPrompt("post_language_option")]:
            digit=f()
            if digit:
                return digit

        return ''

    ######################

    def sayTime(self, time_seconds):
        """
            say time represented by "time_seconds"
            WARNING: both "hour" and "hours" sound files should exists even if they are same
        """
        time_seconds=int(time_seconds)
        hours=time_seconds/3600
        rest=time_seconds%3600
        minutes=rest/60
        seconds=rest%60
        
        list=[]
        if hours:
            list+=self.sayNumberCreateList(hours)
            if hours==1:
                list+=["hour"]
            else:
                list+=["hours"]
            
        if minutes:
            list+=self.sayNumberCreateList(minutes)
            if minutes==1:
                list+=["minute"]
            else:
                list+=["minutes"]

        if seconds:
            list+=self.sayNumberCreateList(seconds)
            if seconds==1:
                list+=["second"]
            else:
                list+=["seconds"]
        
        return self.sayFiles(list)

    def sayCredit(self, credit):
        """
            say money repesented by credit
        """
        return self.sayFiles(self.sayNumberCreateList(credit)+["money_unit"])

    #####################################

    def sayFile(self, filename, escape=ibs_agi.ALL_ESCAPE):
        """
            say file "filename". can be esacped by "escape" digits.
            return the digit pressed for escape or empty string if no digit pressed
        """
        return ibs_agi.getAGI().stream_file(self._getFilePath(filename), escape)
    
    def sayFiles(self, file_list, escape=ibs_agi.ALL_ESCAPE):
        """
            say all files in file_list
        """
        for filename in file_list:
            digit=self.sayFile(filename, escape)
            if digit!='':
                return digit
        return ''

    def sayFilesAndCollect(self, file_list, max_digits, timeout=4000, end_of_collect="#", escape=ibs_agi.ALL_ESCAPE):
        digit=self.sayFiles(file_list, escape)
        digits=digit
        while len(digits)<max_digits:
            digit=ibs_agi.getAGI().wait_for_digit(timeout)
            if not digit or digit == end_of_collect:#timeout
                break
            digits+=digit
        return digits


    ####################################
    
    def __getPromptFiles(self, prompt_name):
        try:
            return self.prompts[prompt_name]
        except KeyError:
            return self.default_prompts[prompt_name]

    def sayPrompt(self, prompt_name, escape=ibs_agi.ALL_ESCAPE):
        """
            say list of files in a prompt
        """
        return self.sayFiles(self.__getPromptFiles(prompt_name), escape)

    def sayPromptAndCollect(self, prompt_name, max_digits, timeout=4000, end_of_collect="#", escape=ibs_agi.ALL_ESCAPE):
        return self.sayFilesAndCollect(self.__getPromptFiles(prompt_name), max_digits, timeout, end_of_collect, escape)


    #####################################
    
    def _getErrorPrompt(self, error_key):
        error_to_prompt_mapping={"VOIP_USERNAME_DOESNT_EXISTS":"invalid_username",
            "WRONG_PASSWORD":"incorrect_password",
            "NO_VOIP_USERNAME_DEFINED":"invalid_username",
            "NO_APPLICABLE_RULE":"destination_incorrect",
            "NO_PREFIX_FOUND":"destination_incorrect",
            "MAX_CONCURRENT":"account_in_use",
            "CANT_USE_MORE_THAN_ONE_SERVICE":"account_in_use",
            "RAS_DOESNT_ALLOW_MULTILOGIN":"account_in_use",
            "CREDIT_FINISHED":"credit_finished",
            "ABS_EXP_DATE_REACHED":"account_expired",
            "REL_EXP_DATE_REACHED":"account_expired",
            "LOGIN_FROM_THIS_CALLER_ID_DENIED":"login_from_caller_id_denied",
            "USER_LOCKED":"account_locked",
            "NO_CHARGE_DEFINED":"destination_incorrect",
            "UNKNOWN_ERROR":"unknown_problem"
            }

        try:
            prompt=error_to_prompt_mapping[error_key]
        except KeyError:
            prompt=error_to_prompt_mapping["UNKNOWN_ERROR"]
            
        return prompt

    def sayError(self, error_key, escape=ibs_agi.ALL_ESCAPE):
        return self.sayPrompt( self._getErrorPrompt(error_key), escape)

    ############################################ Menu related
    def sayMenu(self):
        """
            say menu and return digit entered for selection
            may return invalid digit or empty if no digit entered
        """
        for i in range(1,len(self.MENU_PROMPTS)+1):
            digit=self.sayMenuPrompt(i)
            if digit:
                return digit
        return self.sayPrompt("menu_return")

    def sayMenuPrompt(self, _index):
        """
            say prompt for _index of menu
            
            _index(int):
        """
        return self.sayFiles(self._sayMenuPromptCreateFileList(_index))

    def _sayMenuPromptCreateFileList(self, _index):
        return self.__getPromptFiles("pre_menu_prompt") + [_index] + self.__getPromptFiles("post_menu_prompt") + self._getMenuIndexFiles(_index)

    def _getMenuIndexFiles(self, _index):
        """
            return a list of files for _index of menu
        """
        return self.__getPromptFiles(self.MENU_PROMPTS[_index])

    def getMenuIndexState(self, _index):
        """
            return state related to menu
            may raise KeyError
        """
        return self.MENU_STATES[_index]
    
