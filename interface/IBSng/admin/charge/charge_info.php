<?php
require_once("../../inc/init.php");
require_once(IBSINC."charge.php");
require_once(IBSINC."charge_face.php");
require_once(IBSINC."perm.php");

needAuthType(ADMIN_AUTH_TYPE);
$smarty=new IBSSmarty();
$smarty->assign("is_editing",FALSE);


//print_r($_REQUEST);
if (isInRequest("charge_name","charge_rule_id","delete_charge_rule"))
    intDelChargeRule($smarty,$_REQUEST["charge_name"],$_REQUEST["charge_rule_id"]);
else if (isInRequest("charge_id","charge_name","old_charge_name","comment"))
    intUpdateCharge($smarty,$_REQUEST["charge_id"],$_REQUEST["charge_name"],$_REQUEST["old_charge_name"],isset($_REQUEST["visible_to_all"]),$_REQUEST["comment"]);
else if (isInRequest("charge_name","edit"))
    intEditCharge($smarty,$_REQUEST["charge_name"]);
else if (isInRequest("charge_name","delete_charge"))
    intDeleteCharge($smarty,$_REQUEST["charge_name"]);
else if (isInRequest("charge_name"))
    intChargeInfo($smarty,$_REQUEST["charge_name"]);
else
{
    $err=new error("INVALID_INPUT");
    redirectToChargeList($err->getErrorMsg());
}

function intDeleteCharge(&$smarty,$charge_name)
{
    $del_charge_req=new DelCharge($charge_name);
    $resp=$del_charge_req->sendAndRecv();
    if ($resp->isSuccessful())
        redirectToChargeList("Charge Deleted Successfully");
    else
    {
        $resp->setErrorInSmarty($smarty);
        intChargeInfo($smarty,$charge_name);
    }
}

function intDelChargeRule(&$smarty,$charge_name,$charge_rule_id)
{
    $del_rule_req=new DelChargeRule($charge_rule_id,$charge_name);
    list($success,$err)=$del_rule_req->send();
    if ($success)
        $smarty->assign("del_charge_rule_success",TRUE);
    else
        $smarty->set_page_error($err->getErrorMsgs());

    intChargeInfo($smarty,$charge_name);
}

function intUpdateCharge(&$smarty,$charge_id,$charge_name,$old_charge_name,$visible_to_all,$comment)
{
    $update_req=new UpdateCharge($charge_id,$charge_name,$visible_to_all,$comment);
    list($success,$err)=$update_req->send();
    if($success)
    {
        $smarty->assign("update_success",TRUE);
        intChargeInfo($smarty,$charge_name);
    }
    else
    {
        $smarty->set_page_error($err->getErrorMsgs());
        intChargeInfo($smarty,$old_charge_name);
    }
}

function intEditCharge(&$smarty,$charge_name)
{
    $smarty->assign("is_editing",TRUE);
    intChargeInfo($smarty,$charge_name);
}

function intChargeInfo(&$smarty,$charge_name)
{
    $charge_info_req=new GetChargeInfo($charge_name);
    list($success,$info)=$charge_info_req->send();
    if($success)
    {
        $smarty->assign_array($info);
        $smarty->assign("visible_to_all",$info["visible_to_all"]==="t"?"True":"False");
        $smarty->assign("visible_to_all_checked",$info["visible_to_all"]==="t"?"checked":"");           
        intSetRules($smarty,$charge_name);
    }
    else
        $smarty->set_page_error($info->getErrorMsgs());
        
    face($smarty);
}

function intSetRules(&$smarty,$charge_name)
{
    $list_rules_req=new ListChargeRules($charge_name);
    list ($success,$rules)=$list_rules_req->send();
    if($success)
        $smarty->assign("rules",$rules);
    else
    {
        $smarty->assign("rules",array());
        $smarty->set_page_error($rules->getErrorMsgs());
    }
}

function face(&$smarty)
{
    $smarty->assign("can_change",canDo("CHANGE CHARGE"));
    $smarty->display("admin/charge/charge_info.tpl");
}


?>
