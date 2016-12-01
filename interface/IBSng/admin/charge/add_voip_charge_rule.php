<?php
require_once("../../inc/init.php");
require_once(IBSINC."ras_face.php");
require_once(IBSINC."charge_face.php");
require_once(IBSINC."charge.php");
require_once(IBSINC."voip_tariff_face.php");


needAuthType(ADMIN_AUTH_TYPE);

if(isInRequest("charge_name","rule_start","rule_end","tariff_name","ras"))
    intAddVoIPRule($_REQUEST["charge_name"],$_REQUEST["rule_start"],$_REQUEST["rule_end"],
                       $_REQUEST["tariff_name"],$_REQUEST["ras"]);
else if (isInRequest("charge_name"))
    face($_REQUEST["charge_name"],TRUE);
else
    redirectToChargeList();

function intAddVoIPRule($charge_name,$rule_start,$rule_end,$tariff_name,$ras_ip)
{
    $dows=intFindDowsInRequest();
    $ports=intGetRasPortsRequest(escapeIP($ras_ip));
    $add_req=new AddVoIPChargeRule($charge_name,$rule_start,$rule_end,$tariff_name,$ras_ip,$ports,$dows);
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
    $smarty->display("admin/charge/add_voip_charge_rule.tpl");
}

function intAssignValues(&$smarty,$charge_name,$first_view)
{
    intSetDayOfWeeks($smarty);
    intSetRasAndPorts($smarty);

    intAssignTariffNames($smarty);
    intSetRasIPToDescriptionMapping($smarty);

    $smarty->assign("ras_selected",requestVal("ras","_ALL_"));
    $smarty->assign("charge_name",$charge_name);
    $smarty->assign("check_all_days",$first_view);
    $smarty->assign("is_editing",FALSE);
    $smarty->assign("rule_id","N/A");
    $smarty->assign("tariff_name_selected",requestVal("tariff_name"));
}

function intSetFieldErrors(&$smarty,$err_keys)
{
    $smarty->set_field_errs(array("rule_start_err"=>array("INVALID_RULE_START_TIME","RULE_END_LESS_THAN_START"),
                                  "rule_end_err"=>array("INVALID_RULE_END_TIME","RULE_END_LESS_THAN_START"),
                                  "dow_err"=>array("INVALID_DAY_OF_WEEK"),
                                  "tariff_err"=>array("TARIFF_NAME_DOESNT_EXISTS")
                                  ),$err_keys);

}
