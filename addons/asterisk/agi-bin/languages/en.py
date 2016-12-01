from lib.language import Language

class en(Language):
    def __init__(self):
        
        prompts={"get_username":["please","enter","username"],
                  "get_username_again":["please","enter","username","again"],
                  "get_password":["enter","password"],
                  "pre_say_remaining_credit":["your_account_credit"],
                  "post_say_remaining_credit":[],
                  "get_destination":["enter","destination","press_star_for_more_options"],
                  "get_destination_again":["enter","destination","again","press_star_for_more_options"],

                  "pre_language_option":["for_english_language_press"],
                  "post_language_option":[],

                  "pre_say_remaining_time":["you_can_talk_for"],
                  "post_say_remaining_time":["press_star_to_disconnect"],

                  "pre_say_talked_duration":["you_have_talked"],
                  "post_say_talked_duration":[],

                  "pre_say_used_credit":["your_account_decreased"],
                  "post_say_used_credit":[],

                  "credit_finished":["credit_finished"],


                  "incorrect_password":["password","is","incorrect"],
                  "old_password_incorrect":["password","is","incorrect"],
                  "pre_change_greeting":["say_greeting_message","stop_recording"],

                  "pre_get_fast_dial_destination":["enter","destination","to_store_at_index"],
                  "post_get_fast_dial_destination":[],
                  
                  "pre_add_destination_to_fast_dial_success":["destination"],
                  "mid_add_destination_to_dast_dial_success":["stored_at_index"],
                  "post_add_destination_to_dast_dial_success":[],


                  "pre_confirm_fast_dial":["press"],
                  "mid_confirm_fast_dial":["to_call"],
                  "post_confirm_fast_dial":[],

                  "account_locked":["account","is","locked"],
                  "account_in_use":["this","account","is","currently_in_use"],
                  "destination_incorrect":["destination","is","incorrect"],
                  "destination_busy":["destination","is","busy"],


                  "invalid_username":["username","is","invalid"],
                  "invalid_password":["password","is","invalid"],

                  "pre_menu_prompt":["press","number"],
                  "post_menu_prompt":[],

                  "menu_redial":["to","menu_redial"],
                  "menu_fast_dial":["to","menu_fast_dial"],
                  "menu_modify_fast_dial":["to","menu_modify_fast_dial"],
                  "menu_credit_announcement":["for","menu_credit_announcement"],
                  "menu_change_password":["menu_change_password"],
                  "menu_add_callerid_authentication":["menu_add_callerid_authentication"],
                  "menu_delete_callerid_authentication":["menu_delete_callerid_authentication"],
                  "menu_change_greeting":["menu_change_greeting"],
                  "menu_return":["menu_return"]
                }
        
        Language.__init__(self, "en", prompts)
    
    def sayNumberCreateList(self, number):
        number=int(number)
        list=[]
        if number>=1000*1000: #million
            millions=number/(1000*1000)
            rest=number%(1000*1000)
            list+=self.sayNumberCreateList(millions)+["1000000"]
            if rest!=0:
                list+=["and"]+self.sayNumberCreateList(rest)

        elif number >=1000: #thousands
            thousands=number/1000
            rest=number%1000
            list+=self.sayNumberCreateList(thousands)+["1000"]
            if rest!=0:
                list+=["and"]+self.sayNumberCreateList(rest)
        
        elif number >=100: #hundred
            hundreds=number/100
            rest=number%100
            list+=self.sayNumberCreateList(hundreds)+["100"]
            if rest!=0:
                list+=["and"]+self.sayNumberCreateList(rest)
        
        elif number >=20: 
            tenth=number/10
            rest=number%10
            list+=[str(tenth*10)]
            if rest!=0:
                list+=self.sayNumberCreateList(rest)
        else:
            list+=[str(number)]
        
        return list


    def sayCredit(self, credit):
        dollars=int(credit)
        cents=int((credit-dollars)*100)
        list=[]
        
        if dollars==0 and cents==0:
            list+=["0","dollar"]

        if dollars>1:
            list+=self.sayNumberCreateList(dollars)+["dollars"]
        elif dollars==1:
            list+=self.sayNumberCreateList(dollars)+["dollar"]
        
        if cents>1:
            list+=self.sayNumberCreateList(cents)+["cents"]
        elif cents==1:
            list+=self.sayNumberCreateList(cents)+["cent"]
            
        return self.sayFiles(list)

