<?php
require_once("../../inc/init.php");
require_once("change_credit_funcs.php");

needAuthType(ADMIN_AUTH_TYPE);
$smarty=new IBSSmarty();

if(isInRequest("user_id","credit","credit_comment"))
    intChangeCredit($smarty,requestVal("user_id"),requestVal("credit"),requestVal("credit_comment"));
else if (isInRequest("user_id"))
    intShowChangeCreditFace($smarty,requestVal("user_id"));
else
    redirectToUserSearch("");
