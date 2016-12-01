from core.ibs_exceptions import *

GENERAL_ERRORS={
    "NO_ERROR_TEXT":"Can't find Error Text",
    "USER_NOT_FOUND":"User not found",
    "NOT_ONLINE":"User %s is not online on %s , %s", #arguments username,ras_ip,port
    "INVALID_AUTH_TYPE":"Invalid Authentication type",
    "INTERNAL_ERROR":"Internal Error",
    "RANGE_ERROR":"Invalid range",
    "RANGE_END_LESS_THAN_START":"%s Range End is equal or less than Start",
    "RANGE_IS_TOO_LARGE":"%s Range is too large",
    "INVALID_CREDIT_LOG_ACTION":"Invalid credit log action",
    "INVALID_DATE_UNIT":"Invalid date unit %s",
    "INVALID_DATE_TYPE":"Invalid date type %s",
    "INVALID_DATE":"Invalid date format %s",
    "ACCESS_DENIED":"Access Denied",
    "INVALID_INT_VALUE":"%s must be an integer",
    "INVALID_BOOL_VALUE":"invalid boolean value %s",
    "INVALID_FLOAT_VALUE":"%s must be a valid floating point",
    "INVALID_STRING_VALUE":"%s must be an string",
    "INVALID_LIST_VALUE":"%s must be a list",
    "INVALID_IP_ADDRESS":"Invalid IP Address %s",
    "INVALID_REL_DATE_UNIT":"Invalid Relative Date Unit %s",
    "INVALID_REL_DATE":"Invalid Relative Date %s",
    "INVALID_TIME_STRING":"Invalid Time String %s",
    "TIME_OUT_OF_RANGE":"Time Out of Range",
    "INVALID_DAY_OF_WEEK":"'%s' is not a valid day of week",
    "INCOMPLETE_REQUEST":"Incomplete request, argument %s not found",
    "FROM_VALUE_INVALID":"Invalid From value %s",
    "TO_VALUE_INVALID":"Invalid To value %s",
    "ATTR_NOT_FOUND":"Attribute %s not found",
    "INVALID_ORDER_BY":"Invalid Order By value %s",
    "INVALID_MAC_ADDRESS":"Mac Address %s is invalid",
    "INVALID_CALLER_ID_PATTERN":"Caller ID pattern %s is invalid",
    "INVALID_RADIUS_TIME":"Radius time %s is invalid"
    
}

USER_ACTIONS_ERRORS={
    "INVALID_MULTI_LOGIN":"Invalid Multi Login Value",

    "CREDIT_NOT_FLOAT":"Credit must be a float number",
    "CREDIT_MUST_BE_POSITIVE":"Credit must be positive number",

    "INVALID_CREDIT_ACTION":"Invalid credit change action %s",
    "BAD_NORMAL_USERNAME":"Bad characters in username %s",
    "BAD_VOIP_USERNAME":"Bad characters in username %s",
    "BAD_PASSWORD":"Bad characters in password",
    "BAD_EMAIL":"Invalid email address %s",
    "INVALID_REL_EXP_DATE":"Relative Expiration Date is Invalid",

    "INVALID_USER_COUNT":"Invalid count of users %s",
    "COUNT_NOT_INTEGER":"User count should be positive integer",
    "NORMAL_USER_COUNT_NOT_MATCH":"Internet Usernames count isn't equal to updating users count. Updating %s users while there are %s Internet usernames",
    "VOIP_USER_COUNT_NOT_MATCH":"Voip Usernames count isn't equal to updating users count. Updating %s users while there are %s voip usernames",
    "EMAIL_ADDRESS_COUNT_NOT_MATCH":"Email Address count isn't equal to updating users count. Updating %s users while there are %s email addresses",

    "INVALID_PASSWORD_LENGTH":"Invalid password length %s",
    "ACCESS_TO_SAVED_USER_LIST_DENIED":"You don't have access to saved username/password list",

    "NORMAL_USERNAME_EXISTS":"Internet username(s) %s already exist",
    "VOIP_USERNAME_EXISTS":"VoIP username(s) %s already exist",
    "EMAIL_ADDRESS_EXISTS":"Email Address(es) %s already exist",

    "INVALID_OPERATOR":"Invalid operator %s",
    "DELETE_USER_IS_ONLINE":"Can't delete user with id %s, because he is online",
    "INVALID_ABS_EXP_DATE":"Absolute Expiration Date is Invalid: %s",
    "INVALID_RADIUS_ATTRIBUTE":"Radius Attributes %s is not in radius dictionary",

    "PERSISTENT_LAN_MAC_IP_EXISTS":"Persistent Lan %s already exists",
    "PLAN_MAC_COUNT_NOT_MATCH":"Number of Mac/IP Addresses count isn't equal to updating users count.",
    "RAS_IS_NOT_PERSISTENT_LAN":"Ras %s is not Persistent Lan",
    "DUPLICATE_MAC":"Duplicate Mac %s",

    "CAN_NOT_NEGATE_CREDIT":"Can not negate credit of user %s, current credit is %s",
    "VOIP_CHARGE_EXPECTED":"VoIP Charge Expected, but found charge with type %s",
    "INTERNET_CHARGE_EXPECTED":"Internet Charge Expected, but found charge with type %s",

    "DUPLICATE_USERNAME":"Duplicate Username %s",
    "WRONG_OLD_PASSWORD":"Old password is wrong",
    "INVALID_SESSION_TIMEOUT":"Session Timeout Value is invalid",
    "INVALID_IDLE_TIMEOUT":"Idle Timeout Value is invalid",

    "BAD_CALLER_ID":"Caller ID %s is invalid",
    "CALLER_ID_EXISTS":"Caller ID(s) %s already exist",
    "CALLER_ID_NOT_EXISTS":"Caller ID %s not exists",


    "DUPLICATE_EMAIL_ADDRESS":"Duplicate Email Address %s",


    "MONTHLY_PERIODIC_ACCOUNING_VALUE_INVALID":"Type of monthly periodic accounting should be jalali or gregorian",
    "PERIODIC_ACCOUNING_LIMIT_INVALID":"Periodic accounting limitation value should be integer",
    "DAILY_PERIODIC_ACCOUNING_VALUE_INVALID":"Daily periodic accounting reset days should be positive integer",
    "PERIODIC_ACCOUNING_USAGE_INVALID":"Usage value is invalid",
    "INVALID_ADD_USER_SAVE_ID":"Invalid Add User Save ID",
    "MAIL_QUOTA_NOT_INTEGER":"Mailbox Quota should be positive integer",

    "USER_IDS_COUNT_NOT_MATCH":"Number of given user ids aren't equal to number of generating users",
    
    "INVALID_FAST_DIAL":"Fast Dial String is invalid",
    "INVALID_FAST_DIAL_ENTRY":"Fast Dial entry %s is invalid",
    "INVALID_FAST_DIAL_INDEX":"Fast Dial index %s is invalid",
    
    "INVALID_DESTINATION":"Destination %s is invalid"
}

USER_ERRORS={
    "DUPLICATE_ATTR_REGISTRATION":"Duplicate registration of attribute %s",
    "UNREGISTERED_ATTRIBUTE":"Attribute %s not registered",
    "UNKNOWN_ATTRIBUTE_ACTION":"Unknown attribute action %s",
    "USERID_DOESNT_EXISTS":"User with user id %s does not exists",
    "INVALID_USER_ID":"User id %s is invalid",
    "NORMAL_USERNAME_DOESNT_EXISTS":"User with Internet username %s does not exists",
    "VOIP_USERNAME_DOESNT_EXISTS":"User with VoIP username %s does not exists",
    "ACCESS_TO_USER_DENIED":"You have not access to user id %s",
    "CANT_FIND_INSTANCE":"User %s is not online on %s %s",
    "USER_IN_BLACKLIST":"User ID %s is in load black list",
    "CALLER_ID_DOESNT_EXISTS":"User with caller id %s does not exists"

}

USER_LOGIN_ERRORS={
    "USER_LOCKED":"User is locked",
    "NO_CHARGE_DEFINED":"User does not have charge for type %s",
    "NO_APPLICABLE_RULE":"No rule can be applied",
    "ABS_EXP_DATE_REACHED":"Absolute expiration date has reached",
    "CREDIT_FINISHED":"Credit has finished",
    "REL_EXP_DATE_REACHED":"Relative expiration date has reached",
    "WRONG_PASSWORD":"Wrong password",
    "MAX_CONCURRENT":"Maximum number of concurrent logins reached",
    "USER_IP_NOT_AVAILABLE":"Client IP Address not available for user %s",
    "MAX_CHECK_ONLINE_FAILS_REACHED":"Maximum check online fails reached",
    "LOGIN_FROM_THIS_MAC_DENIED":"You can not login from this MAC address",
    "LOGIN_FROM_THIS_IP_DENIED":"You can not login from this IP address",
    "LOGIN_FROM_THIS_CALLER_ID_DENIED":"You can not login from this caller id",
    "RAS_DOESNT_ALLOW_MULTILOGIN":"Ras does not allow multi login",
    "NO_PREFIX_FOUND":"Called Number has no defined prefix",
    "CANT_USE_MORE_THAN_ONE_SERVICE":"You can not use VoIP and Internet Services simultaneously",
    "KILLED_BY_ADMIN":"Killed by admin %s",
    "CLEARED_BY_ADMIN":"Cleared by admin %s",
    "NO_VOIP_USERNAME_DEFINED":"No VoIP Username defined for user",
    "PLAN_ATTRIBUTES_CHANGED":"Persistent Lan Attributes has been changed",
    "KILLED_BY_NEG_CREDIT_CHECKER":"Killed by negative credit checker",
    "LOGIN_NOT_ALLOWED":"Login is not allowed at this time because of system maintenance",
    "SYSTEM_SHUTTING_DOWN":"System shutdown",
    "TIMELY_QUOTA_EXCEEDED":"User Timely quota has been exceeded",
    "TRAFFIC_QUOTA_EXCEEDED":"User Traffic quota has been exceeded",
    "INVALID_CALLED_NUMBER":"Called Number is invalid",
    "REMOTE_IP_CONFLICT":"Remote IP Conflict detected",
    
    "INVALID_FAST_DIAL_INDEX":"Invalid Fast Dial Index %s"
}

ADMIN_LOGIN_ERRORS={
    "NO_SUCH_ADMIN":"No such admin %s",
    "INCORRECT_PASSWORD":"Incorrect password",
    "ADMIN_LOCKED":"Admin account is locked",
    "ADDRESS_BANNED":"You are not authorized to login from this address"    
}

ADMIN_ERRORS={
    "ADMIN_ID_INVALID":"Admin ID %s is invalid",
    "ADMIN_USERNAME_INVALID":"Admin Username %s is invalid",
    "ADMIN_USERNAME_TAKEN":"Admin Username %s is already taken",
    "BAD_USERNAME":"Admin Username %s contains illegal characters",
    "BAD_PASSWORD":"Admin Password contains illegal characters",
    "NEGATIVE_DEPOSIT_NOT_ALLOWED":"You don't have enough deposit, you need %s more deposit",#needed deposit
    "DEPOSIT_SHOULD_BE_FLOAT":"Deposit change amount should be numeric",
    "CANNOT_DELETE_SYSTEM":"Admin System can not be deleted",
    "LOCK_ID_SHOULD_BE_INTEGER":"Lock ID Should be Integer",
    "MAIL_DOMAIN_RESTRICTED":"Mail Domain Restricted"
}

PERM_ERRORS={
    "INVALID_PERMISSION_VALUE":"Invalid permission value: %s", #more decriptive message as argument
    "DONT_HAVE_PERMISSION":"Admin doesn't have permission",
    "DUPLICATE_PERM_NAME":"Duplicate permission registration %s",
    "NO_SUCH_PERMISSION":"No Such Permission %s",
    "DEPENDENCY_NOT_SATISFIED":"Dependency Permission %s not satisfied for %s",#1- dependency perm 2- perm
    "ALREADY_HAS_PERMISSION":"Admin already has permission %s",
    "DEPENDENT_PERMISSION":"Permission %s is needed by %s",
    "NO_VALUE_TO_DELETE":"Permission hasn't any value to delete",
    "PERMISSION_NOT_HAVE_THIS_VALUE":"Permission doesn't have value %s",
    "DUPLICATE_TEMPLATE_NAME":"Duplicate Permission Template name %s",
    "INVALID_PERM_TEMPLATE_NAME":"Invalid Permission Template name %s",
    "PERMISSION_ALREADY_HAS_VALUE":"Permission %s already has value %s"
}

DEFS_ERRORS={
    "INVALID_DEFINITION_NAME":"Invalid Definition Name %s",
    "UNSUPPORTED_TYPE":"%s has unsupported type %s" #1-def name 2- type
}

GROUP_ERRORS={
    "GROUP_ID_INVALID":"Group id %s is invalid",
    "GROUP_NAME_INVALID":"Group name %s is invalid",
    "GROUP_NAME_TAKEN":"Group name %s already exists",
    "ACCESS_TO_GROUP_DENIED":"You don't have access to group %s",
    "GROUP_CHANGE_DENIED":"You can't change group %s",
    "GROUP_USED_IN_USER":"Group %s used in users '%s' "
}

CHARGE_ERRORS={
    "INVALID_CHARGE_ID":"Invalid Charge ID %s",
    "INVALID_CHARGE_NAME":"Invalid Charge Name %s",
    "CHARGE_NAME_EXISTS":"Charge name %s already exists",
    "RULE_HAS_OVERLAP":"New Rule has overlap with %s",
    "INVALID_RULE_ID_IN_CHARGE":"Invalid charge_rule_id '%s' in %s",
    "INVALID_CHARGE_TYPE":"Invalid charge type %s",
    "ACCESS_TO_CHARGE_DENIED":"You don't have access to charge %s",
    "INVALID_RULE_START_TIME":"Invalid Rule Start Time: %s",#err msg
    "INVALID_RULE_END_TIME":"Invalid Rule End Time: %s",#err msg
    "INVALID_DAY_OF_WEEK":"Charge Rule Day of week error: %s",
    "ASSUMED_KPS_NOT_INTEGER":"Assumed Kps should be an integer",
    "ASSUMED_KPS_NOT_POSITIVE":"Assumed KPS should be positive integer",
    "BANDWIDTH_LIMIT_NOT_INTEGER":"Bandwidth Limit should be an integer",
    "BANDWIDTH_LIMIT_NOT_POSITIVE":"Bandwidth Limit should be positive integer",
    "CPM_NOT_NUMERIC":"Charge Per Minute should be numeric",
    "CPM_NOT_POSITIVE":"Charge Per Minute should be positive integer",
    "CPK_NOT_NUMERIC":"Charge Per Kilobyte should be numeric",
    "CPK_NOT_POSITIVE":"Charge Per Kilobyte should be positive integer",
    "ANOTHER_CHARGE_TYPE_REQUIRED":"Charge Type of %s is required",
    "NO_PORT_SELECTED":"No Port is selected",
    "RULE_END_LESS_THAN_START":"Rule End time is less than or equal to Start time",
    "INVALID_CHARGE_RULE_ID":"Invalid Charge Rule ID %s",
    "CHARGE_RULE_NOT_IN_CHARGE":"Charge Rule with ID %s is not in charge %s",
    "CHARGE_USED_IN_USER":"Charge %s is used in user(s) with id(s) '%s' ",
    "CHARGE_USED_IN_GROUP":"Charge %s is used in group(s) '%s' ",
    "BW_LEAF_NAMES_SHOULD_BOTH_SET":"Bandwidth leafs should both be disabled or both be enabled"

}

RAS_ERRORS={
    "DUPLICATE_TYPE_REGISTRATION":"Duplicate Registration of ras type %s",
    "RAS_TYPE_NOT_REGISTERED":"Ras type %s is not registered",

    "INVALID_RAS_IP":"Invalid Ras IP %s",
    "INVALID_RAS_ID":"Invalid Ras ID %s",
    "INVALID_RAS_DESCRIPTION":"Invalid Ras Description %s",

    "RAS_IP_ALREADY_EXISTS":"Ras IP %s Already Exists",
    "RAS_DESCRIPTION_ALREADY_EXISTS":"Ras Description %s Already Exists",
    
    
    "RAS_USED_IN_RULE":"Ras used in charge rule %s, delete the charge rule first",
    "INVALID_PORT_NAME":"Invalid Port Name %s",
    "RAS_ALREADY_HAS_PORT":"Ras already has port with name %s",
    "INVALID_PORT_TYPE":"Invalid Port Type %s",
    "RAS_DONT_HAVE_PORT":"Ras doesn't have port %s",
    "RAS_DONT_HAVE_ATTR":"Ras doesn't have attribute %s",
    "NO_SUCH_INACTIVE_RAS":"There's no Inactive ras with ip %s",
    "RAS_IS_INACTIVE":"Ras with ip %s is inactive, you should reactive it instead of adding",
    "RAS_ALREADY_HAVE_IPPOOL":"Ras already have ippool %s",
    "RAS_DONT_HAVE_IPPOOL":"Ras doesn't have IPpool %s",
    "RAS_HAS_ONLINE_USERS":"Ras has online users"
}

IPPOOL_ERRORS={
    "NO_FREE_IP":"All %s IP Pool IPs are used",
    "IP_NOT_IN_USED_POOL":"IP %s is not in 'used list' of IP Pool %s",
    "INVALID_IP_POOL_ID":"Invalid IP Pool id %s",
    "INVALID_IP_POOL_NAME":"Invalid IP Pool name %s",
    "BAD_IP_POOL_NAME":"Bad IP Pool name %s. IP Pool name should only contain alphanumeric and _(underline)",
    "IP_POOL_NAME_ALREADY_EXISTS":"IP Pool name %s already exists",
    "IP_ALREADY_IN_POOL":"IP %s already exists in IP Pool",
    "IP_NOT_IN_POOL":"IP %s does not exist in IP Pool",
    "IPPOOL_USED_IN_RAS":"IP Pool Used In ras %s, delete it from ras first",
    "IPPOOL_USED_IN_USER":"IP Pool Used In user(s) %s",
    "IPPOOL_USED_IN_GROUP":"IP Pool Used In group(s) %s",
    "IP_IS_USED":"IP %s is used by users"

}

BANDWIDTH_ERRORS={
    "NO_FREE_ID":"No ID is available from pool %s",
    "INVALID_INTERFACE_ID":"Interface ID %s is invalid",
    "INVALID_INTERFACE_NAME":"Interface Name %s is invalid",
    "INVALID_NODE_ID":"Node ID %s is invalid",
    "INVALID_LEAF_ID":"Leaf ID %s is invalid",
    "INVALID_LEAF_NAME":"Leaf Name %s is invalid",
    "LEAF_ID_NOT_FOUND":"Leaf with id %s not found",
    "NODE_ID_NOT_FOUND":"Node with id %s not found",
    "INTERFACE_NAME_ALREADY_EXISTS":"Interface %s already defined",
    "INVALID_INTERFACE_NAME":"Invalid Interface name %s",
    "INTERFACE_HAS_ROOT_NODE":"Interface %s already has root node",
    "INVALID_LIMIT_KBITS":"Limits Kbit/s '%s' should be greater than zero integer",
    "INVALID_LEAF_NAME":"Invalid Leaf name %s",
    "INVALID_TOTAL_LIMIT_KBITS":"Total Limit Kbit/s '%s' should be an integer, both should be positive, or both should be negative(disabled)",
    "LEAF_NAME_ALREADY_EXISTS":"Leaf name %s already defined",
    "INVALID_PROTOCOL":"Invalid Protocol %s",
    "LEAF_HAS_THIS_FILTER":"Leaf %s already has filter %s %s",
    "INVALID_FILTER":"Invalid Filter %s",
    "LEAF_DOESNT_HAVE_SERVICE":"Leaf %s doesn't have service with id %s",
    "NODE_HAS_CHILDREN":"Node has children, delete them first",
    "LEAF_USED_IN_CHARGE":"Leaf used in charge %s",
    "CANT_DELETE_ROOT_NODE":"You can't delete root node, delete interface instead",
    "LEAF_HAS_SERVICES":"Leaf has services, delete them first",
    "INVALID_STATIC_IP_ID":"BW StaticIP ID %s is invalid",
    "INVALID_STATIC_IP":"BW StaticIP %s is invalid",
    "STATIC_IP_EXISTS":"BW StaticIP %s is already exists in %s",
    "LEAF_USED_IN_STATIC_IP":"Leaf is used in StaticIP %s"
}

VOIP_TARIFF_ERRORS={
    "BAD_TARIFF_NAME":"Invalid Tariff name %s",
    "TARIFF_NAME_ALREADY_EXISTS":"Tariff name %s already exists",
    "TARIFF_USED_IN_CHARGE":"Tariff used in charge %s",
    "PREFIX_COUNT_NOT_EQUAL":"Prefix parameter counts are not equal",
    "PREFIX_CODE_IS_NOT_DIGIT":"Prefix code '%s' is not digit",
    "FREE_SECONDS_NOT_NUMERIC":"Free seconds is not numeric or is negative",
    "MIN_DURATION_NOT_NUMERIC":"Minimum duration is not numeric or is negative",
    "ROUND_TO_NOT_NUMERIC":"Round to seconds is not numeric or is negative",
    "MIN_CHARGABLE_DURATION_NOT_NUMERIC":"Minimum Chargable Duration is not numeric or is negative",
    "PREFIX_CODE_ALREADY_EXIST":"Prefix Code '%s' already exists in tariff %s",
    "DUPLICATE_PREFIX_CODE":"Prefix code %s is duplicate",
    "TARIFF_DOESNT_HAVE_PREFIX_ID":"Tariff %s doesn't have prefix id %s",
    "TARIFF_DOESNT_HAVE_PREFIX_CODE":"Tariff %s doesn't have prefix code %s",
    "NO_PREFIX_TO_DELETE":"No prefix to delete",
    "TARIFF_NAME_DOESNT_EXISTS":"Tariff name %s doesn't exists",
    "TARIFF_ID_DOESNT_EXISTS":"Tariff id %s doesn't exists",
}


PLUGIN_ERRORS={
    "INVALID_HOOK":"Invalid Hook name %s"
}

REPORT_ERRORS={
    "INVALID_CLEAN_TABLE":"Table %s is not available for cleaning",
    "INVALID_AUTO_CLEAN_TABLE_DATE":"Auto clean date %s for table %s is invalid",
    "INVALID_SNAPSHOT_NAME":"Invalid Snapshot name %s"
}

MESSAGE_ERRORS={
    "INVALID_MESSAGE_LENGTH":"Empty or too big message",
    "INVALID_MESSAGE_ID":"Message ID %s is invalid",
    "CANT_DELETE_SEND_TO_ALL":"Can't delete send to all message",
    "INVALID_MESSAGE_TABLE":"Invalid message table %s"
}

IAS_ERRORS={
    "INVALID_EVENT_ID":"Invalid Event ID"
}

def errorText(event,error,add_error_key=True):
    """
        return "error" text representation in "event"
    
        event(str): is a text that shows which dictionary we use for errors
        error(str): is key of error that we want text for
        add_error_key(boolean): should we add the error key to the returning string?
                                if set to True the return value format will be error_key|error_string
        
        NOTE: there may be %s is retuened strings in such cases you must use % operator 
               after the returned string and overrid %s values
    """
    try:
        error_map={"USER_ACTIONS":USER_ACTIONS_ERRORS,
                   "USER":USER_ERRORS,
                   "USER_LOGIN":USER_LOGIN_ERRORS,
                   "GENERAL":GENERAL_ERRORS,
                   "PLUGINS":PLUGIN_ERRORS,
                   "ADMIN_LOGIN":ADMIN_LOGIN_ERRORS,
                   "ADMIN":ADMIN_ERRORS,
                   "PERMISSION":PERM_ERRORS,
                   "DEFS":DEFS_ERRORS,
                   "GROUPS":GROUP_ERRORS,
                   "CHARGES":CHARGE_ERRORS,
                   "RAS":RAS_ERRORS,
                   "IPPOOL":IPPOOL_ERRORS,
                   "BANDWIDTH":BANDWIDTH_ERRORS,
                   "VOIP_TARIFF":VOIP_TARIFF_ERRORS,
                   "REPORTS":REPORT_ERRORS,
                   "MESSAGES":MESSAGE_ERRORS,
                   "IAS":IAS_ERRORS
                  }
                   
        err_str=error_map[event][error]

        if add_error_key:
            err_str="%s|%s"%(error,err_str)
        return err_str

    except:
        logException(LOG_ERROR,"errorText: can't find error for %s,%s"%(event,error))
        raise GeneralException(GENERAL_ERRORS["NO_ERROR_TEXT"])

def getErrorKey(str_error):
    """
        return key of error in "str_error" or empty string if str_error has no key
    """
    try:
        return str_error[:str_error.index("|")]
    except ValueError:
        return ""

def getErrorText(str_error):
    """
        return text of error in "str_error". Error Key is deleted from returning string
    """
    try:
        return str_error[str_error.index("|")+1:]
    except ValueError:
        return str_error
