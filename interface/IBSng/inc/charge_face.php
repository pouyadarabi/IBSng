<?php
require_once("init.php");
require_once("charge.php");

$DAY_OF_WEEKS=array(0=>"Monday", 1=>"Tuesday", 2=>"Wednesday", 3=>"Thursday", 4=>"Friday", 5=>"Saturday", 6=>"Sunday");

function redirectToChargeInfo($charge_name,$extra_param="")
{
    $redirect_str="/IBSng/admin/charge/charge_info.php?charge_name={$charge_name}";
    if($extra_param!="")
        $redirect_str.="&{$extra_param}";
    redirect($redirect_str);
}

function redirectToChargeList($msg="")
{
    redirect("/IBSng/admin/charge/charge_list.php?msg={$msg}");
}

function intSetChargeTypes(&$smarty)
{
    $smarty->assign("charge_types",array("Internet","VoIP"));
}

function intSetDayOfWeeks(&$smarty)
{
    global $DAY_OF_WEEKS;
    $smarty->assign("day_of_weeks",$DAY_OF_WEEKS);
}

function intFindDowsInRequest()
{/*
    find day of weeks in request, and return an array of day names that was is request
*/
    global $DAY_OF_WEEKS;
    $dows=array();
    foreach($DAY_OF_WEEKS as $day_name)
        if(isInRequest($day_name))
            $dows[]=$day_name;

    return $dows;
    
}

function intGetRasPortsRequest($ras)
{/*
    return string "all" or an array of port names that is in request for ras with ip $ras
*/
    if($ras=="_ALL_" or isInRequest("{$ras}_ALL_"))
        return "_ALL_";

    $ports=array();
    foreach ($_REQUEST as $key=>$value)
        if(preg_match("/^{$ras}__(.+)/",$key,$matches))
            $ports[]=$matches[1];
        
    return $ports;          
}

function intSetChargeNames(&$smarty,$type,$var_name="charge_names")
{/* set name of all $type charges in smarty variable "charge_names" 
    $type can be null to return all charge types or (Internet , VoIP)
    $var_name is smarty variable that charge names would be assigned
*/
    $charge_names=new ListCharges($type);
    list($success,$charge_names)=$charge_names->send();
    if (!$success)
    {
        $smarty->set_page_error($charge_names->getErrorMsgs());
        $smarty->assign($var_name,array());
    }
    else
        $smarty->assign($var_name,$charge_names);
}

?>