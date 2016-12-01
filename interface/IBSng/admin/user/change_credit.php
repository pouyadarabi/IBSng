<?php
require_once("../../inc/init.php");
require_once("change_credit_funcs.php");

needAuthType(ADMIN_AUTH_TYPE);
$smarty=new IBSSmarty();

if(isInRequest("user_id","credit","credit_comment"))
    intChangeCredit($smarty,$_REQUEST["user_id"],$_REQUEST["credit"],$_REQUEST["credit_comment"]);
else if (isInRequest("user_id"))
    intShowChangeCreditFace($smarty,$_REQUEST["user_id"]);
else
    redirectToUserSearch("");

?>