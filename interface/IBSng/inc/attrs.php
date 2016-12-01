<?php
require_once(IBSINC."charge.php");
require_once(IBSINC."csv.php");

//***************************************************** Relative Exp Date


function relExpDatePluginUpdate(&$update_helper)
{
    if(!isInRequest("has_rel_exp"))
        $update_helper->addToDelAttrs("rel_exp_date");
    else
    {
        $update_helper->addToUpdateAttrs("rel_exp_date",$_REQUEST["rel_exp_date"]);
        $update_helper->addToUpdateAttrs("rel_exp_date_unit",$_REQUEST["rel_exp_date_unit"]);
    }
}

//***************************************************** First Login


function firstLoginPluginUpdate(&$update_helper)
{
    if(isInRequest("reset_first_login"))
        $update_helper->addToDelAttrs("first_login");
}


//***************************************************** Absolute Exp Date

function absExpDatePluginUpdate(&$update_helper)
{
    if(!isInRequest("has_abs_exp"))
        $update_helper->addToDelAttrs("abs_exp_date");
    else
    {
        $update_helper->addToUpdateAttrs("abs_exp_date",$_REQUEST["abs_exp_date"]);
        $update_helper->addToUpdateAttrs("abs_exp_date_unit",$_REQUEST["abs_exp_date_unit"]);
    }
}


//**************************************************** Multi Login



function multiLoginPluginUpdate(&$update_helper)
{
    if(!isInRequest("has_multi_login"))
        $update_helper->addToDelAttrs("multi_login");
    else
        $update_helper->addToUpdateAttrs("multi_login",$_REQUEST["multi_login"]);
}

//**************************************************** Group Info

function groupInfoPluginUpdate(&$update_helper)
{
    $update_helper->mustBeInRequest("group_id","group_name","owner_name","comment");
    $update_group_req=new UpdateGroup($_REQUEST["group_id"],$_REQUEST["group_name"],$_REQUEST["comment"],$_REQUEST["owner_name"]);
    list($success,$err)=$update_group_req->send();
    if($success)
    {
        $update_helper->target_id=$_REQUEST["group_name"];
        $update_helper->redirectToTargetInfo();
    }
    else
        $update_helper->showEditInterface($err);
}

//**************************************************** Normal Charge

function normalChargePluginUpdate(&$update_helper)
{
    if(!isInRequest("has_normal_charge"))
        $update_helper->addToDelAttrs("normal_charge");
    else
        $update_helper->addToUpdateAttrs("normal_charge",$_REQUEST["normal_charge"]);
}

//**************************************************** VoIP Charge

function voipChargePluginUpdate(&$update_helper)
{
    if(!isInRequest("has_voip_charge"))
        $update_helper->addToDelAttrs("voip_charge");
    else
        $update_helper->addToUpdateAttrs("voip_charge",$_REQUEST["voip_charge"]);
}



//**************************************************** IPpool
function IPpoolPluginUpdate(&$update_helper)
{
    if(!isInRequest("has_ippool"))
        $update_helper->addToDelAttrs("ippool");
    else
        $update_helper->addToUpdateAttrs("ippool",$_REQUEST["ippool"]);
}

//*************************************************** Assign IP
function assignIPPluginUpdate(&$update_helper)
{
    if(isInRequest("assign_ip"))
        $update_helper->addToUpdateFromRequest("assign_ip");
    else
        $update_helper->addToDelAttrs("assign_ip");
}

//*************************************************** Radius Attrs
function radiusAttrsPluginUpdate(&$update_helper)
{
    if(!isInRequest("has_radius_attrs"))
        $update_helper->addToDelAttrs("radius_attrs");
    else
        $update_helper->addToUpdateAttrs("radius_attrs",$_REQUEST["radius_attrs"]);
}

//************************************* Group Name
function groupNamePluginUpdate(&$update_helper)
{
    if(isInRequest("group_name"))
        $update_helper->addToUpdateAttrs("group_name",$_REQUEST["group_name"]);
}
//************************************* Owner Name

function ownerNamePluginUpdate(&$update_helper)
{
    if(isInRequest("owner_name"))
        $update_helper->addToUpdateAttrs("owner_name",$_REQUEST["owner_name"]);
}
//************************************* Normal Username
function normalAttrsPluginUpdate(&$update_helper)
{
    if(isInRequest("has_normal_username"))
    {
        $update_helper->addToUpdateAttrs("normal_username",$_REQUEST["normal_username"]);
        $update_helper->addToUpdateAttrs("normal_save_usernames",isInRequest("normal_save_user_add"));
        if(isInRequest("generate_password"))
        {
            $update_helper->addToUpdateAttrs("normal_password","");
            $generate_password=0;
            if(isInRequest("password_character"))
                $generate_password+=1;
            if(isInRequest("password_digit"))
                $generate_password+=2;
        
            $update_helper->addToUpdateAttrs("normal_generate_password",$generate_password);
            $update_helper->addToUpdateAttrs("normal_generate_password_len",$_REQUEST["password_len"]);
        }
        else
        {
            $update_helper->addToUpdateAttrs("normal_generate_password",0);
            $update_helper->addToUpdateAttrs("normal_generate_password_len",0);
            $update_helper->addToUpdateAttrs("normal_password",$_REQUEST["password"]);
        }
    }
    else if (isInRequest("has_normal_username_from_file"))
    {
        $parser=new CSVParser(",");
        $usernames=array();
        $passwords=array();
        $ret=$parser->readUploadedFile("normal_username_from_file");
        if($ret===TRUE)
        {
            $parsed=$parser->getArray();
            foreach($parsed as $line)
            {
                if(sizeof($line)==2)
                {
                    $usernames[] = $line[0];
                    $passwords[] = $line[1];
                }
            }
        }

        $update_helper->addToUpdateAttrs("normal_username",join(",",$usernames));
        $update_helper->addToUpdateAttrs("normal_password",join(",",$passwords));

        $update_helper->addToUpdateAttrs("normal_save_usernames",1);
        $update_helper->addToUpdateAttrs("normal_generate_password",0);
        $update_helper->addToUpdateAttrs("normal_generate_password_len",0);
    
    }
    else
        $update_helper->addToDelAttrs("normal_username");
}
//************************************* VoIP Username
function voipAttrsPluginUpdate(&$update_helper)
{
    if(isInRequest("has_voip_username"))
    {
        $update_helper->addToUpdateAttrs("voip_username",$_REQUEST["voip_username"]);
        $update_helper->addToUpdateAttrs("voip_save_usernames",isInRequest("voip_save_user_add"));
        if(isInRequest("voip_generate_password"))
        {
            $update_helper->addToUpdateAttrs("voip_password","");
            $generate_password=0;
            if(isInRequest("voip_password_character"))
                $generate_password+=1;
            if(isInRequest("voip_password_digit"))
                $generate_password+=2;
        
            $update_helper->addToUpdateAttrs("voip_generate_password",$generate_password);
            $update_helper->addToUpdateAttrs("voip_generate_password_len",$_REQUEST["voip_password_len"]);
        }
        else
        {
            $update_helper->addToUpdateAttrs("voip_generate_password",0);
            $update_helper->addToUpdateAttrs("voip_generate_password_len",0);
            $update_helper->addToUpdateAttrs("voip_password",$_REQUEST["voip_password"]);
        }
    }

    else if (isInRequest("has_voip_username_from_file"))
    {
        $parser=new CSVParser(",");
        $usernames=array();
        $passwords=array();
        $ret=$parser->readUploadedFile("voip_username_from_file");
        if($ret===TRUE)
        {
            $parsed=$parser->getArray();
            foreach($parsed as $line)
            {
                if(sizeof($line)==2)
                {
                    $usernames[] = $line[0];
                    $passwords[] = $line[1];
                }
            }
        }

        $update_helper->addToUpdateAttrs("voip_username",join(",",$usernames));
        $update_helper->addToUpdateAttrs("voip_password",join(",",$passwords));

        $update_helper->addToUpdateAttrs("voip_save_usernames",1);
        $update_helper->addToUpdateAttrs("voip_generate_password",0);
        $update_helper->addToUpdateAttrs("voip_generate_password_len",0);
    }
    else
        $update_helper->addToDelAttrs("voip_username");
}

//**************************************************** VoIP Caller ID
function callerIDPluginUpdate(&$update_helper)
{
    if(isInRequest("has_caller_id"))
        $update_helper->addToUpdateAttrs("caller_id",$_REQUEST["caller_id"]);
    else
        $update_helper->addToDelAttrs("caller_id");
}

//************************************************** Lock
function lockPluginUpdate(&$update_helper)
{
    if(isInRequest("lock"))
        $update_helper->addToUpdateAttrs("lock",removeCR($_REQUEST["lock"]));
    else
        $update_helper->addToDelAttrs("lock");
}

//************************************************** save_bw_usage
function saveBWUsagePluginUpdate(&$update_helper)
{
    if(isInRequest("save_bw_usage"))
        $update_helper->addToUpdateAttrs("save_bw_usage",TRUE);
    else
        $update_helper->addToDelAttrs("save_bw_usage");
}

//************************************************** Persistent Lan
function persistentLanPluginUpdate(&$update_helper)
{
    if(isInRequest("has_plan"))
    {
        $update_helper->addToUpdateFromRequest("persistent_lan_mac");
        $update_helper->addToUpdateFromRequest("persistent_lan_ip");
        $update_helper->addToUpdateFromRequest("persistent_lan_ras_ip");
    }
    else
        $update_helper->addToDelAttrs("persistent_lan_mac");

}

//*************************************************** Comment
function commentPluginUpdate(&$update_helper)
{
    if(isInRequest("comment"))
        $update_helper->addToUpdateAttrs("comment",removeCR($_REQUEST["comment"]));
    else
        $update_helper->addToDelAttrs("comment");
}

function namePluginUpdate(&$update_helper)
{
    if(isInRequest("name"))
        $update_helper->addToUpdateAttrs("name",removeCR($_REQUEST["name"]));
    else
        $update_helper->addToDelAttrs("name");
}

function phonePluginUpdate(&$update_helper)
{
    if(isInRequest("phone"))
        $update_helper->addToUpdateAttrs("phone",removeCR($_REQUEST["phone"]));
    else
        $update_helper->addToDelAttrs("phone");
}

//*************************************************** Limit Mac
function limitMacPluginUpdate(&$update_helper)
{
    if(isInRequest("limit_mac"))
        $update_helper->addToUpdateFromRequest("limit_mac");
    else
        $update_helper->addToDelAttrs("limit_mac");
}

//*************************************************** Limit Station IP
function limitStationIPPluginUpdate(&$update_helper)
{
    if(isInRequest("limit_station_ip"))
        $update_helper->addToUpdateFromRequest("limit_station_ip");
    else
        $update_helper->addToDelAttrs("limit_station_ip");
}

//*************************************************** Session Timeout
function sessionTimeoutPluginUpdate(&$update_helper)
{
    if(isInRequest("session_timeout"))
        $update_helper->addToUpdateFromRequest("session_timeout");
    else
        $update_helper->addToDelAttrs("session_timeout");
}

//*************************************************** Session Timeout
function idleTimeoutPluginUpdate(&$update_helper)
{
    if(isInRequest("idle_timeout"))
        $update_helper->addToUpdateFromRequest("idle_timeout");
    else
        $update_helper->addToDelAttrs("idle_timeout");
}


//*************************************************** Limit CallerID
function limitCallerIDPluginUpdate(&$update_helper)
{
    if(isInRequest("limit_caller_id"))
    {
        $update_helper->addToUpdateFromRequest("limit_caller_id");
        $update_helper->addToUpdateAttrs("limit_caller_id_allow_not_defined",
                                         isInRequest("limit_caller_id_allow_not_defined"));
    }
    else
        $update_helper->addToDelAttrs("limit_caller_id");
}
//*************************************************** Periodic Accounting
function timePAccountingPluginUpdate(&$update_helper,$check_box, $key)
{
    if(isInRequest($check_box))
    {
        $update_helper->addToUpdateFromRequest($key);
        $limit = durationToSeconds($_REQUEST["{$key}_limit"]); //convert to seconds
        $update_helper->addToUpdateAttrs("{$key}_limit", $limit);
    }
    else
        $update_helper->addToDelAttrs($key);
}

function timePAccountingUsagePluginUpdate(&$update_helper, $key)
{
    if(isInRequest("{$key}_usage"))
    {
        $usage = durationToSeconds($_REQUEST["{$key}_usage"]); //convert to seconds
        $update_helper->addToUpdateAttrs("{$key}_usage", $usage);
    }
}

function trafficPAccountingPluginUpdate(&$update_helper, $check_box, $key)
{
    if(isInRequest($check_box))
    {
        $update_helper->addToUpdateFromRequest($key);
        $limit = (float)$_REQUEST["{$key}_limit"] * 1024 * 1024; //convert to bytes
        $update_helper->addToUpdateAttrs("{$key}_limit", $limit);
    }
    else
        $update_helper->addToDelAttrs($key);
}

function trafficPAccountingUsagePluginUpdate(&$update_helper, $key)
{
    if(isInRequest("{$key}_usage"))
    {
        $usage = (float)$_REQUEST["{$key}_usage"] * 1024 * 1024;
        $update_helper->addToUpdateAttrs("{$key}_usage", $usage);
    }
}

function monthlyTimePAccountingPluginUpdate(&$update_helper)
{
    timePAccountingPluginUpdate($update_helper, "has_monthly_time_paccounting", "time_periodic_accounting_monthly");
}

function monthlyTimePAccountingUsagePluginUpdate(&$update_helper)
{
    timePAccountingUsagePluginUpdate($update_helper, "time_periodic_accounting_monthly");
}

function monthlyTrafficPAccountingPluginUpdate(&$update_helper)
{
    trafficPAccountingPluginUpdate($update_helper, "has_monthly_traffic_paccounting", "traffic_periodic_accounting_monthly");
}

function monthlyTrafficPAccountingUsagePluginUpdate(&$update_helper)
{
    trafficPAccountingUsagePluginUpdate($update_helper, "traffic_periodic_accounting_monthly");
}

function dailyTimePAccountingPluginUpdate(&$update_helper)
{
    timePAccountingPluginUpdate($update_helper, "has_daily_time_paccounting", "time_periodic_accounting_daily");
}

function dailyTimePAccountingUsagePluginUpdate(&$update_helper)
{
    timePAccountingUsagePluginUpdate($update_helper, "time_periodic_accounting_daily");
}

function dailyTrafficPAccountingPluginUpdate(&$update_helper)
{
    trafficPAccountingPluginUpdate($update_helper, "has_daily_traffic_paccounting", "traffic_periodic_accounting_daily");
}

function dailyTrafficPAccountingUsagePluginUpdate(&$update_helper)
{
    trafficPAccountingUsagePluginUpdate($update_helper, "traffic_periodic_accounting_daily");
}

//*************************************************** Mailbox 
function mailQuotaPluginUpdate(&$update_helper)
{
    if(isInRequest("mail_quota"))
    {
        $mail_quota=(int)$_REQUEST["mail_quota"]*1024*1024; // convert to bytes
        $update_helper->addToUpdateAttrs("mail_quota",$mail_quota);
    }
    else
        $update_helper->addToDelAttrs("mail_quota");
}

function emailAddressPluginUpdate(&$update_helper)
{
    if(isInRequest("has_email_address"))
        $update_helper->addToUpdateFromRequest("email_address");
    else
        $update_helper->addToDelAttrs("email_address");
}

//*************************************************** Fast Dial
function fastDialPluginUpdate(&$update_helper)
{
    if(isInRequest("has_fast_dial"))
    {

        $update_helper->addToUpdateAttrs("fast_dial",
                                         array($_REQUEST["fast_dial0"],
                                               $_REQUEST["fast_dial1"],
                                               $_REQUEST["fast_dial2"],
                                               $_REQUEST["fast_dial3"],
                                               $_REQUEST["fast_dial4"],
                                               $_REQUEST["fast_dial5"],
                                               $_REQUEST["fast_dial6"],
                                               $_REQUEST["fast_dial7"],
                                               $_REQUEST["fast_dial8"],
                                               $_REQUEST["fast_dial9"]));
    }
    else
        $update_helper->addToDelAttrs("fast_dial");
}

//*************************************************** VoIP Preferred Language
function voipPreferredLanguagePluginUpdate(&$update_helper)
{
    if(isInRequest("voip_preferred_language"))
        $update_helper->addToUpdateFromRequest("voip_preferred_language");
    else
        $update_helper->addToDelAttrs("voip_preferred_language");
}


//************************** UNUSED CODE
function relExpParser(&$parsed_arr,&$smarty,&$attrs)
{
    if(!isset($attrs["rel_exp_date"]))
    {
        $parsed_arr["has_rel_exp"]=FALSE;
        $parsed_arr["rel_exp_date_unit"]=null;
        $parsed_arr["rel_exp_date"]=null;
    }
    else
    {
        $parsed_arr["has_rel_exp"]=TRUE;
        $rel_exp=(int)$attrs["rel_exp_date"];
        list($rel_exp,$rel_exp_unit)=calcRelativeDateFromHours($rel_exp);
        $parsed_arr["rel_exp_date_unit"]=$rel_exp_unit;
        $parsed_arr["rel_exp_date"]=$rel_exp;
    }
}

function multiLoginParser(&$parsed_arr,&$smarty,&$attrs)
{
    assignToParsedIfExists($parsed_arr,$attrs,"multi_login");
}

function normalChargeParser(&$parsed_arr,&$smarty,&$attrs)
{
    if(isset($attrs["normal_charge"]))
    { //translate charge_id to charge_name
        $charge_info_req=new GetChargeInfo(null,$attrs["normal_charge"]);
        list($success,$info)=$charge_info_req->send();
        if($success)
            $parsed_arr["normal_charge"]=$info["charge_name"];
        else
            $smarty->set_page_error($info->getErrorMsgs());
    }
}

?>
