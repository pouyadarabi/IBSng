<?php
function intGetRuleInfo($charge_name,$charge_rule_id)
{
    $list_rules_req=new ListChargeRules($charge_name);
    list($success,$rules)=$list_rules_req->send();
    if(!$success)
        return array(FALSE,$rules);
    foreach($rules as $rule)
        if ($rule["rule_id"]==$charge_rule_id)
            return array(TRUE,$rule);

    redirectToChargeList("Invalid Rule ID");
}

function intSetRuleInfo(&$smarty,$rule_info)
{
    $smarty->assign_array($rule_info);
    intSetDayOfWeeksParams($smarty,$rule_info);
    intSetRasParams($smarty,$rule_info);
}

function intSetDayOfWeeksParams(&$smarty,$rule_info)
{
    foreach($rule_info["day_of_weeks"] as $dow)
        $smarty->assign($dow,"checked");
}

function intSetRasParams(&$smarty,$rule_info)
{
    $smarty->assign("ras_selected",requestVal("ras",$rule_info["ras"]));
    if($rule_info["ras"]!="_ALL_")
        foreach ($rule_info["ports"] as $port_name)
            $smarty->assign("{$rule_info["ras"]}_{$port_name}","checked");
}
?>