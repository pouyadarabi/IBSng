<?php
require_once("../../inc/init.php");
require_once(IBSINC."admin.php");
require_once(IBSINC."admin_face.php");

needAuthType(ADMIN_AUTH_TYPE);
$smarty=new IBSSmarty();

if(isInRequest("admin_username","deposit","deposit_comment"))
    intChangeDeposit($smarty,$_REQUEST["admin_username"],$_REQUEST["deposit"],$_REQUEST["deposit_comment"]);
else if (isInRequest("admin_username"))
    intShowChangeDepositFace($smarty,$_REQUEST["admin_username"]);
else
    redirectToAdminList();

function intChangeDeposit(&$smarty,$admin_username,$deposit,$deposit_comment)
{
    $req=new ChangeDeposit($admin_username,$deposit,$deposit_comment);
    $resp=$req->sendAndRecv();
    if($resp->isSuccessful())
        $smarty->assign("change_successfull",TRUE);
    else
    {
        $resp->setErrorInSmarty($smarty);
        intSetErrors($smarty,$resp->getError());
    }
    intShowChangeDepositFace($smarty,$admin_username);
}

function intShowChangeDepositFace(&$smarty,$admin_username)
{
    $smarty->assign("admin_username",$admin_username);
    $smarty->display("admin/admins/change_deposit.tpl");
}

function intSetErrors(&$smarty,$err)
{
    $err_keys=$err->getErrorKeys();
    $smarty->set_field_errs(array("deposit_err"=>array("DEPOSIT_SHOULD_BE_FLOAT","INVALID_FLOAT_VALUE"),
                                  "admin_username_err"=>array("ADMIN_USERNAME_INVALID")
                                 ),$err_keys);
}

?>