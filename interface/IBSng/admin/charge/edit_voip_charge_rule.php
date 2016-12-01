<?php
require_once("../../inc/init.php");
require_once(IBSINC."ras_face.php");
require_once(IBSINC."charge_face.php");
require_once(IBSINC."charge.php");
require_once(IBSINC."voip_tariff_face.php");
require_once("charge_rule_funcs.php");

needAuthType(ADMIN_AUTH_TYPE);

$smarty=new IBSSmarty();


if(isInRequest("charge_name","charge_rule_id","rule_start","rule_end","tariff_name","ras"))
    intUpdateVoIPRule($smarty,$_REQUEST["charge_name"],$_REQUEST["charge_rule_id"],$_REQUEST["rule_start"],$_REQUEST["rule_end"],
                       $_REQUEST["tariff_name"],$_REQUEST["ras"]);
else if (isInRequest("charge_name","charge_rule_id"))
    intEditVoIPRule($smarty,$_REQUEST["charge_name"],$_REQUEST["charge_rule_id"]);
else
    redirectToChargeList();

function intUpdateVoIPRule(&$smarty,$charge_name,$charge_rule_id,$rule_start,$rule_end,$tariff_name,$ras_ip)
{
    $dows=intFindDowsInRequest();
    $ports=intGetRasPortsRequest(escapeIP($ras_ip));
    $update_req=new UpdateVoIPChargeRule($charge_name,$charge_rule_id,$rule_start,$rule_end,$tariff_name,$ras_ip,$ports,$dows);
    list($success,$err)=$update_req->send();
    if($success)
        redirectToChargeInfo($charge_name,"update_charge_rule_success=1");
    else
    {
        $smarty->set_page_error($err->getErrorMsgs());
        intSetFieldErrors($smarty,$err->getErrorKeys());
        intEditVoIPRule($smarty,$charge_name,$charge_rule_id);
    }
}


function intEditVoIPRule(&$smarty,$charge_name,$charge_rule_id)
{
    list($success,$rule_info)=intGetRuleInfo($charge_name,$charge_rule_id);
    if($success)
        intSetRuleInfo($smarty,$rule_info);
    else
        $smarty->set_page_error($rule_info->getErrorMsgs());

    face($smarty,$charge_name);
}

function face(&$smarty,$charge_name)
{
    intAssignValues($smarty,$charge_name);
    $smarty->display("admin/charge/add_voip_charge_rule.tpl");    
}

function intAssignValues(&$smarty,$charge_name)
{
    intSetDayOfWeeks($smarty);
    intSetRasAndPorts($smarty);

    intAssignTariffNames($smarty);
    intSetRasIPToDescriptionMapping($smarty);

    $smarty->assign("charge_name",$charge_name);
    $smarty->assign("check_all_days",FALSE);
    $smarty->assign("is_editing",TRUE);
    $smarty->assign("tariff_name_selected",requestVal("tariff_name",$smarty->get_assigned_value("tariff_name")));
}

function intSetFieldErrors(&$smarty,$err_keys)
{
    $smarty->set_field_errs(array("rule_start_err"=>array("INVALID_RULE_START_TIME","RULE_END_LESS_THAN_START"),
                                  "rule_end_err"=>array("INVALID_RULE_END_TIME","RULE_END_LESS_THAN_START"),
                                  "dow_err"=>array("INVALID_DAY_OF_WEEK"),
                                  "tariff_err"=>array("TARIFF_NAME_DOESNT_EXISTS")
                                  ),$err_keys);

}
?>