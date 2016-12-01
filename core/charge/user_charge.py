import time
class UserCharge:
    """
        Instances of this class will keep charge related information
        inf user object, normally with name "charge_info"
        no charging logic here! just variable manipulations
    """
    def __init__(self):
        self.credit_prev_usage=0 #previous usage of logged off users
        self.credit_prev_usage_instance=[] #previous usage of currently online instances
        self.effective_rules=[]
        self.rule_start=[]
        self.accounting_started=[] #has accounting started? keep start time in seconds from epoch here


    def login(self,instance):
        self.effective_rules.append(None)
        self.rule_start.append(0)
        self.credit_prev_usage_instance.append(0)
        self.accounting_started.append(0)

    def logout(self,instance):
        _index=instance-1
        del(self.effective_rules[_index])
        del(self.rule_start[_index])
        del(self.credit_prev_usage_instance[_index])
        del(self.accounting_started[_index])

    def setEffectiveRule(self, instance, effective_rule):
        _index=instance-1
        self.effective_rules[_index] = effective_rule
        self.rule_start[_index] = time.time()

class InternetUserCharge(UserCharge):
    def __init__(self):
        UserCharge.__init__(self)
        self.rule_start_inout=[]

    def login(self,instance):
        UserCharge.login(self,instance)
        self.rule_start_inout.append([0,0])

    def logout(self,instance):
        UserCharge.logout(self,instance)
        del(self.rule_start_inout[instance-1])
        
class VoIPUserCharge(UserCharge):
    def __init__(self):
        UserCharge.__init__(self)
        self.prefix_id=[]
        self.remaining_free_seconds=[]

    def login(self,instance):
        UserCharge.login(self,instance)
        self.prefix_id.append(0)
        self.remaining_free_seconds.append(-1)

    def logout(self,instance):
        UserCharge.logout(self,instance)
        del(self.prefix_id[instance-1])
        del(self.remaining_free_seconds[instance-1])
