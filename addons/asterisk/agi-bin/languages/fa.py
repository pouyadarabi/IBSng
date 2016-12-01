from lib.language import Language

class fa(Language):
    def __init__(self):
        
        prompts={"get_username":["username&","enter"],
                  "get_username_again":["username&","again","enter"],
                  "get_password":["password&","enter"],
                  "pre_say_remaining_credit":["your_account_credit"],
                  "post_say_remaining_credit":["is"],
                  "get_destination":["enter_destination","enter","more_facilities"],
                  "get_destination_again":["enter_destination","again","enter","more_facilities"],

                  "pre_language_option":["for_farsi_language"],
                  "post_language_option":["press&"],

                  "pre_say_remaining_time":["you_can_talk"],
                  "post_say_remaining_time":["is","star_disconnect"],

                  "pre_say_talked_duration":["you"],
                  "post_say_talked_duration":["talked"],

                  "pre_say_used_credit":[],
                  "post_say_used_credit":["used_credit"],

                  "invalid_username":["username","incorrect"],
                  "credit_finished":["your_account_credit","finished"],


                  "incorrect_password":["password","incorrect"],
                  "old_password_incorrect":["password","incorrect"],
                  "pre_change_greeting":["pre_change_greeting","pound_key"],

                  "pre_get_fast_dial_destination":["for_index"],
                  "post_get_fast_dial_destination":["enter_destination","enter"],
                  
                  "pre_add_destination_to_fast_dial_success":["number"],
                  "mid_add_destination_to_dast_dial_success":["in_index"],
                  "post_add_destination_to_dast_dial_success":["saved"],

                  "authentication_failed":["password","3times_incorrect"],

                  "account_locked":["account","locked"],

                  "destination_incorrect":["destination","incorrect"],
                  

                }
        
        Language.__init__(self, "fa", prompts)
    
    def sayNumberCreateList(self, number):
        number=int(number)
        list=[]
        if number>=1000*1000: #million
            millions=number/(1000*1000)
            rest=number%(1000*1000)
            list+=self.sayNumberCreateList(millions)
            if rest==0:
                list+=["1000000"]
            else:
                list+=["1000000&"]+self.sayNumberCreateList(rest)

        elif number >=1000: #thousands
            thousands=number/1000
            rest=number%1000
            list+=self.sayNumberCreateList(thousands)
            if rest==0:
                list+=["1000"]
            else:
                list+=["1000&"]+self.sayNumberCreateList(rest)
        
        elif number >=100: #hundred
            hundreds=number/100
            rest=number%100
            
            if hundreds in [2,3,5]:
                if rest==0:
                    list+=[str(hundreds*100)]               
                else:
                    list+=[str(hundreds*100)+"&"]

            else:
                list+=self.sayNumberCreateList(hundreds)
                if rest==0:
                    list+=["100"]
                else:
                    list+=["100&"]
            
            if rest!=0:
                list+=self.sayNumberCreateList(rest)
        
        elif number >=20: 
            tenth=number/10
            rest=number%10
            if rest==0:
                list+=[str(tenth*10)]
            else:
                list+=[str(tenth*10)+"&"]
                list+=self.sayNumberCreateList(rest)
        else:
            list+=[str(number)]
        
        return list


    def sayCredit(self, credit):
        return self.sayFiles(self.sayNumberCreateList(credit)+["rial"])

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
            if minutes:
                list+=["hour&"]
            else:
                list+=["hour"]
            
        if minutes:
            list+=self.sayNumberCreateList(minutes)
            if seconds:
                list+=["minute&"]
            else:
                list+=["minute"]

        if seconds:
            list+=self.sayNumberCreateList(seconds)
            list+=["second"]
        
        return self.sayFiles(list)
