<?php
require_once("../../inc/init.php");
require_once(IBSINC."report.php");
require_once(IBSINC."user.php");
require_once(IBSINC."user_face.php");
require_once(IBSINC."csv.php");


needAuthType(ADMIN_AUTH_TYPE);
$smarty=new IBSSmarty();
session_write_close();

if(isInRequest("add_user_save_id","delete"))
    intDeleteAddUserSave($smarty,$_REQUEST["add_user_save_id"]);
if(isInRequest("add_user_save_id","csv"))
    intShowAddUserSaveCSV($_REQUEST["add_user_save_id"],$_REQUEST["csv"]);
else if(isInRequest("add_user_save_id"))
    intShowAddUserSave($smarty,$_REQUEST["add_user_save_id"]);
else
    redirectToSearchAddUserSaves("Invalid Input");

function intDeleteAddUserSave(&$smarty,$add_user_save_id)
{
    $req=new DeleteAddUserSaves(array($add_user_save_id));
    $resp=$req->sendAndRecv();
    if($resp->isSuccessful())
        redirectToSearchAddUserSaves("Add User Save Deleted Successfully");
    else
    {
        $resp->setErrorInSmarty($smarty);
        intShowAddUserSave($smarty,$add_user_save_id);
    }
}

function intShowAddUserSaveCSV($add_user_save_id,$csv)
{
    $csv=new CSVGenerator($csv);
    $csv->sendHeader("add_user_save_{$add_user_save_id}.csv");
    $info=intGetAddUserSaveInfo($add_user_save_id);
    foreach($info["details"][0] as $idx=>$user_id)
        $csv->doLine($user_id,$info["details"][1][$idx],$info["details"][2][$idx]);
}

function intShowAddUserSave(&$smarty,$add_user_save_id)
{
    intSetInfo($smarty,$add_user_save_id);
    $smarty->display("admin/user/add_user_save_details.tpl");
}

function intSetInfo(&$smarty,$add_user_save_id)
{
    $info=intGetAddUserSaveInfo($add_user_save_id);
    $smarty->assign_array($info);
}

function intGetAddUserSaveInfo($add_user_save_id)
{
    $conds=array("add_user_save_id"=>$add_user_save_id);
    $req=new SearchAddUserSaves($conds,
                                0,
                                1,
                                "add_date",
                                True);
    $resp=$req->sendAndRecv();
    if($resp->isSuccessful())
    {
        $result=$resp->getResult();
        if($result["total_rows"]!=1)
            redirectToSearchAddUserSaves("Add User Save ID Not Found");
        return $result["result"][0];
    }
    else
        redirectToSearchAddUserSaves($resp->getError());
}

?>