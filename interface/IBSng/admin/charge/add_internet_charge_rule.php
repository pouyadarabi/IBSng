<?php
require_once("../../inc/init.php");
require_once(IBSINC."ras_face.php");
require_once(IBSINC."charge_face.php");
require_once(IBSINC."charge.php");
require_once(IBSINC."bw_face.php");


needAuthType(ADMIN_AUTH_TYPE);

if(isInRequest("charge_name","rule_start","rule_end","cpm","cpk","assumed_kps","bandwidth_limit_kbytes","tx_leaf_name","rx_leaf_name","ras"))
    intAddInternetRule($_REQUEST["charge_name"],$_REQUEST["rule_start"],$_REQUEST["rule_end"],
                       $_REQUEST["cpm"],$_REQUEST["cpk"],$_REQUEST["assumed_kps"],$_REQUEST["bandwidth_limit_kbytes"],
                       $_REQUEST["tx_leaf_name"],$_REQUEST["rx_leaf_name"],$_REQUEST["ras"]);
else if (isInRequest("charge_name"))
    face($_REQUEST["charge_name"],TRUE);
else
    redirectToChargeList();



function intAddInternetRule($charge_name,$rule_start,$rule_end,$cpm,$cpk,
                            $assumed_kps,$bandwidth_limit_kbytes,$tx_leaf_name,$rx_leaf_name,$ras_ip)
{
    $dows=intFindDowsInRequest();
    $ports=intGetRasPortsRequest(escapeIP($ras_ip));
    $add_req=new AddInternetChargeRule($charge_name,$rule_start,$rule_end,$cpm,$cpk,
                            $assumed_kps,$bandwidth_limit_kbytes,$tx_leaf_name,$rx_leaf_name,$ras_ip,$ports,$dows);
    list($success,$err)=$add_req->send();
    if($success)
        redirectToChargeInfo($charge_name);
    else
        face($charge_name,FALSE,$err);    
}


function face($charge_name,$first_view,$err=null)
{ /*
    first_view(bool): if this is the first time we show the page,  it's true, else it's false and it means      
                      form submitted last time, and we had an error
  */
    $smarty=new IBSSmarty();
    intAssignValues($smarty,$charge_name,$first_view);

    if(!is_null($err))
    {
        intSetFieldErrors($smarty,$err->getErrorKeys());
        $smarty->set_page_error($err->getErrorMsgs());
    }

    $smarty->display("admin/charge/add_internet_charge_rule.tpl");    
}

function intAssignValues(&$smarty,$charge_name,$first_view)
{
    intSetDayOfWeeks($smarty);
    intSetRasAndPorts($smarty);

    intAssignBwLeafNames($smarty);
    intSetRasIPToDescriptionMapping($smarty);


    $smarty->assign("ras_selected",requestVal("ras","_ALL_"));
    $smarty->assign("charge_name",$charge_name);
    $smarty->assign("check_all_days",$first_view);
    $smarty->assign("is_editing",FALSE);
    $smarty->assign("rule_id","N/A");


    $smarty->assign("tx_leaf_selected",requestVal("tx_leaf_name"));
    $smarty->assign("rx_leaf_selected",requestVal("rx_leaf_name"));


}

function intSetFieldErrors(&$smarty,$err_keys)
{
    $smarty->set_field_errs(array("rule_start_err"=>array("INVALID_RULE_START_TIME","RULE_END_LESS_THAN_START"),
                                  "rule_end_err"=>array("INVALID_RULE_END_TIME","RULE_END_LESS_THAN_START"),
                                  "dow_err"=>array("INVALID_DAY_OF_WEEK"),
                                  "cpm_err"=>array("CPM_NOT_NUMERIC","CPM_NOT_POSITIVE"),
                                  "cpm_err"=>array("CPK_NOT_NUMERIC","CPK_NOT_POSITIVE"),
                                  "cpm_err"=>array("CPK_NOT_NUMERIC","CPK_NOT_POSITIVE"),
                                  "assumed_kps_err"=>array("ASSUMED_KPS_NOT_INTEGER","ASSUMED_KPS_NOT_POSITIVE"),
                                  "bw_limit_err"=>array("BANDWIDTH_LIMIT_NOT_INTEGER","BANDWIDTH_LIMIT_NOT_POSITIVE"),
                                  "rx_leaf_err"=>array("BW_LEAF_NAMES_SHOULD_BOTH_SET","INVALID_LEAF_NAME"),
                                  "tx_leaf_err"=>array("BW_LEAF_NAMES_SHOULD_BOTH_SET","INVALID_LEAF_NAME")
                                  ),$err_keys);

}
