<?php
require_once("../../../inc/init.php");
require_once(IBSINC."voip_tariff_face.php");
require_once(IBSINC."voip_tariff.php");
require_once(IBSINC."perm.php");
require_once(IBSINC."csv.php");

needAuthType(ADMIN_AUTH_TYPE);

$smarty=new IBSSmarty();

if(isInRequest("csv","tariff_name"))
    intDownloadPrefixes($smarty,$_REQUEST["tariff_name"],$_REQUEST["csv"]);

else if (isInRequest("del_prefix_checkbox","tariff_name"))
    intDelPrefixCheckBox($smarty,$_REQUEST["tariff_name"]);

else if(isInRequest("del_prefix","tariff_name"))
    intDelPrefix($smarty,$_REQUEST["tariff_name"],$_REQUEST["del_prefix"]);

else if(isInRequest("del_tariff","tariff_name"))
    intDelTariff($smarty, $_REQUEST["tariff_name"]);

else if(isInRequest("tariff_name"))
    intShowTariffInfo($smarty,$_REQUEST["tariff_name"]);
else
    redirectToTariffList();

function intDelTariff(&$smarty, $tariff_name)
{
    $req=new DeleteTariff($tariff_name);
    $resp=$req->sendAndRecv();
    if($resp->isSuccessful())
        redirectToTariffList();
    else
    {
        $resp->setErrorInSmarty($smarty);
        intShowTariffInfo($smarty,$tariff_name);
    }

}

function intDownloadPrefixes(&$smarty,$tariff_name,$separator)
{
    $req=new GetTariffInfo($tariff_name,TRUE);
    $resp=$req->sendAndRecv();
    if($resp->isSuccessful())
    {
        $result=$resp->getResult();
        $csv=new CSVGenerator($separator);
        $csv->sendHeader("voip_tariff_{$tariff_name}.csv");
        foreach($result["prefixes"] as $prefix)
            $csv->doLine($prefix["prefix_name"],$prefix["prefix_code"],$prefix["cpm"],
                         $prefix["free_seconds"],$prefix["min_duration"],$prefix["round_to"],
                         $prefix["min_chargable_duration"]);
    }
    else
    {
        $resp->setErrorInSmarty($smarty);
        intShowTariffInfo($smarty,$tariff_name);
    }

}

function intDelPrefixCheckBox(&$smarty,$tariff_name)
{
    $prefixes=array();
    foreach($_REQUEST as $key=>$value)
        if(preg_match("/^del_prefix_[0-9]+/",$key))
            $prefixes[]=$value;
    if(sizeof($prefixes)==0)
    {
        $smarty->set_page_error("No prefix selected");
        intShowTariffInfo($smarty,$tariff_name);
    }
    else
        intDelPrefix($smarty,$tariff_name,join(",",$prefixes));
}

function intDelPrefix(&$smarty,$tariff_name,$prefix)
{
    $req=new DeletePrefix($tariff_name,$prefix);
    $resp=$req->sendAndRecv();
    if($resp->isSuccessful())
        $smarty->assign("delete_prefix_success",TRUE);
    else
        $resp->setErrorInSmarty($smarty);
    intShowTariffInfo($smarty,$tariff_name);    
}

function intShowTariffInfo(&$smarty,$tariff_name)
{
    $name_regex=intGetStartsWith();
    if (is_null($name_regex))
        intSetTariffInfo($smarty,$tariff_name,FALSE);
    else
        intSetTariffInfo($smarty,$tariff_name,TRUE,$name_regex);
        
        
    $smarty->assign("start_withs",intGetStartsWithChars());
    $smarty->assign("can_change",canDo("CHANGE VOIP TARIFF"));
    $smarty->display("admin/charge/voip_tariff/tariff_info.tpl");
}

function intGetStartsWith()
{// get selected character to show, or null if no character selected
    if(isInRequest("name_regex"))
        return $_REQUEST["name_regex"];
    else if(isInRequest("starts_with"))
        return "^{$_REQUEST["starts_with"]}";
    else
        return null;
}

function intGetStartsWithChars()
{
    $chars=array(array("All",""));
    for($i=97;$i<=122;$i++)
        $chars[]=array(chr($i),"^[".chr($i).strtoupper(chr($i))."]");
    
    $chars[]=array("Others","^[^a-zA-Z]");
    return $chars;
}

?>