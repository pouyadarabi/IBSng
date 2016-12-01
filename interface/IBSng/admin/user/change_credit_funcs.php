<?php
require_once(IBSINC."user.php");
require_once(IBSINC."user_face.php");
require_once(IBSINC."user_search.php");

function intChangeCredit(&$smarty,$user_id,$credit,$credit_comment)
{
    $req=new ChangeUserCredit($user_id,$credit,$credit_comment);
    $resp=$req->sendAndRecv();
    if($resp->isSuccessful())
        $smarty->assign("change_successfull",TRUE);
    else
    {
        $resp->setErrorInSmarty($smarty);
        intSetErrors($smarty,$resp->getError());
    }
    intShowChangeCreditFace($smarty,$user_id);
}

function intShowChangeCreditFace(&$smarty,$user_id)
{
    $smarty->assign("user_id",$user_id);
    $smarty->display("admin/user/change_credit.tpl");
}

function intSetErrors(&$smarty,$err)
{
    $err_keys=$err->getErrorKeys();
    $smarty->set_field_errs(array("credit_err"=>array("CREDIT_NOT_FLOAT","INVALID_FLOAT_VALUE","CAN_NOT_NEGATE_CREDIT")),$err_keys);
}

?>