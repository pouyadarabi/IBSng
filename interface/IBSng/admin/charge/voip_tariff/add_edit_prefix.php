<?php
require_once("../../../inc/init.php");
require_once(IBSINC."voip_tariff_face.php");
require_once(IBSINC."voip_tariff.php");
require_once(IBSINC."csv.php");

needAuthType(ADMIN_AUTH_TYPE);

if(isInRequest("tariff_name","csv"))
    intAddPrefixFromFile($_REQUEST["tariff_name"],$_REQUEST["csv"]);

else if(isInRequest("add","tariff_name","prefix_name","prefix_code","cpm","round_to","min_duration","free_seconds","min_chargable_duration"))
    intAddPrefix($_REQUEST["tariff_name"],$_REQUEST["prefix_name"],$_REQUEST["prefix_code"],$_REQUEST["cpm"],
                 $_REQUEST["free_seconds"],$_REQUEST["min_duration"],$_REQUEST["round_to"],$_REQUEST["min_chargable_duration"]);

else if (isInRequest("edit","tariff_name","old_prefix_name","prefix_id","prefix_name","prefix_code","cpm","round_to","min_duration","free_seconds","min_chargable_duration"))
    intUpdatePrefix($_REQUEST["tariff_name"],$_REQUEST["old_prefix_name"],$_REQUEST["prefix_id"],$_REQUEST["prefix_name"],$_REQUEST["prefix_code"],
                    $_REQUEST["cpm"],$_REQUEST["free_seconds"],$_REQUEST["min_duration"],$_REQUEST["round_to"],$_REQUEST["min_chargable_duration"]);

else if (isInRequest("edit","tariff_name","prefix_id","prefix_name"))
    editInterface($_REQUEST["tariff_name"],$_REQUEST["prefix_id"],$_REQUEST["prefix_name"]);

else if (isInRequest("add","tariff_name"))
    addInterface($_REQUEST["tariff_name"]);

else
    redirectToTarrifList();

function intAddPrefixFromFile($tariff_name,$csv)
{
    $parser=new CSVParser($csv);
    $ret=$parser->readUploadedFile("prefixes_file");
    if($ret!==TRUE)
        addInterface($tariff_name,$ret);
    else
    {
        $parsed=$parser->getArray();
        list($names,$codes,$cpms,$free_seconds,$min_durations,$round_tos,$min_chargable_durations)=intSeperateArrays($tariff_name,$parsed);
        intAddPrefixes($tariff_name,$names,$codes,$cpms,$free_seconds,$min_durations,$round_tos,$min_chargable_durations);
    }
}

function intSeperateArrays($tariff_name,$parsed)
{
    $names=array(); $codes=array(); $cpms=array(); $free_seconds=array(); $min_durations=array();$round_tos=array(); $min_chargable_durations=array();
    $line_no=1;
    foreach($parsed as $line)
    {
        if(sizeof($line)!=7)
            addInterface($tariff_name,"{$line_no}:Invalid Line, expected number of columns was 7, found ".sizeof($line));
        $line_no++;
        $names[]=$line[0]; $codes[]=$line[1]; $cpms[]=$line[2]; $free_seconds[]=$line[3]; 
        $min_durations[]=$line[4]; $round_tos[]=$line[5]; $min_chargable_durations[]=$line[6];
    }    
    return array($names,$codes,$cpms,$free_seconds,$min_durations,$round_tos,$min_chargable_durations);
}

function intAddPrefixes($tariff_name,$prefix_name,$prefix_code,$cpm,$free_seconds,$min_duration,$round_to,$min_chargable_durations)
{
    $req=new AddPrefix($tariff_name,$prefix_name,$prefix_code,$cpm,$free_seconds,$min_duration,$round_to,$min_chargable_durations);
    $resp=$req->sendAndRecv();
    if($resp->isSuccessful())
    {
        $result=$resp->getResult();
        if($result["success"])
            redirectToTariffInfo($tariff_name);
        else
            addInterface($tariff_name,$result["errs"],TRUE);
    }
    else
        addInterface($tariff_name,$resp->getError());
}


function intUpdatePrefix($tariff_name,$old_prefix_name,$prefix_id,$prefix_name,$prefix_code,$cpm,$free_seconds,$min_duration,$round_to,$min_chargable_duration)
{
    $req=new UpdatePrefix($tariff_name,$prefix_id,$prefix_name,$prefix_code,$cpm,$free_seconds,$min_duration,$round_to,$min_chargable_duration);
    $resp=$req->sendAndRecv();
    if($resp->isSuccessful())
    {
        redirectToTariffInfo($tariff_name);
    }
    else
        editInterface($tariff_name,$prefix_id,$old_prefix_name,$resp->getError());
}

function editInterface($tariff_name,$prefix_id,$prefix_name, $err=null)
{
    $smarty=new IBSSmarty();
    intSetPrefixInfo($smarty,$tariff_name,$prefix_id,$prefix_name);
    $smarty->assign("action","edit");
    $smarty->assign("action_title","Edit");
    $smarty->assign("action_icon","ok");
    face($smarty,$tariff_name,$err);
}

function intSetPrefixInfo(&$smarty,$tariff_name,$prefix_id, $prefix_name)
{
    intSetTariffInfo($smarty,$tariff_name,TRUE,"^{$prefix_name}\$");
    $found=False;
    if($smarty->is_assigned("prefixes"))
        foreach($smarty->get_assigned_value("prefixes") as $prefix)
            if ($prefix["prefix_id"]==$prefix_id)
            {
                $found=True;
                $smarty->assign_array($prefix);
                break;
            }
    
    if(!$found)
        $smarty->set_page_error("Prefix Doesn't exist");
}

function intAddPrefix($tariff_name,$prefix_name,$prefix_code,$cpm,$free_seconds,$min_duration,$round_to,$min_chargable_duration)
{
    $req=new AddPrefix($tariff_name,array($prefix_name),array($prefix_code),array($cpm),
                       array($free_seconds),array($min_duration),array($round_to),array($min_chargable_duration));
    $resp=$req->sendAndRecv();
    if($resp->isSuccessful())
    {
        $result=$resp->getResult();
        if($result["success"])
            redirectToTariffInfo($tariff_name);
        else
            addInterface($tariff_name,$result["errs"]);
    }
    else
        addInterface($tariff_name,$resp->getError());
}

function addInterface($tariff_name,$err=NULL,$include_line=FALSE)
{
    $smarty=new IBSSmarty();
    $smarty->assign("action","add");
    $smarty->assign("action_title","Add");
    $smarty->assign("action_icon","add");
    face($smarty,$tariff_name,$err,$include_line);
}

function face(&$smarty,$tariff_name,$errs,$include_line=FALSE)
{
    intAssignError($smarty,$errs,$include_line);
    $smarty->assign("tariff_name",$tariff_name);
    $smarty->display("admin/charge/voip_tariff/add_edit_prefix.tpl");
    exit();
}

function intAssignError(&$smarty,$errs,$include_line)
{
    if(!is_null($errs))
    {
        if(is_array($errs))
        {
            $keys=array();
            $values=array();
            foreach($errs as $err)
            {
                list($key,$value)=explode("|",$err);
                list($line,$key)=explode(":",$key);
                $keys[]=$key;
                if($include_line)
                    $value="{$line}:{$value}";
                $values[]=$value;
            }
            intSetErrors($smarty,$keys);
            $smarty->set_page_error($values);
        }
        else if(is_string($errs))
            $smarty->set_page_error($errs);
        else
            $smarty->set_page_error($errs->getErrorMsgs());
    }
}
function intSetErrors(&$smarty,$err_keys)
{
    $smarty->set_field_errs(array("tariff_name_err"=>array("BAD_TARIFF_NAME"),
                                  "prefix_code_err"=>array("PREFIX_CODE_IS_NOT_DIGIT","PREFIX_CODE_ALREADY_EXIST","DUPLICATE_PREFIX_CODE"),
                                  "cpm_err"=>array("CPM_NOT_NUMERIC","CPM_NOT_POSITIVE"),
                                  "free_secs_err"=>array("FREE_SECONDS_NOT_NUMERIC"),
                                  "min_duration_err"=>array("MIN_DURATION_NOT_NUMERIC"),
                                  "round_to_err"=>array("ROUND_TO_NOT_NUMERIC"),
                                  "prefix_id_err"=>array("TARIFF_DOESNT_HAVE_PREFIX_ID"),
                                  "min_chargable_duration_err"=>array("MIN_CHARGABLE_DURATION_NOT_NUMERIC")
                                   ),$err_keys);
}

?>