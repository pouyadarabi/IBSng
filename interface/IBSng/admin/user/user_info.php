<?php
require_once("../../inc/init.php");
require_once("user_info_funcs.php");
require_once(IBSINC."large_url.php");


needAuthType(ADMIN_AUTH_TYPE);

$smarty=new IBSSmarty();
largeUrlRestore("user_id_multi");

if(isInRequest("user_id"))
    intShowSingleUserInfo($smarty,$_REQUEST["user_id"]);

else if (isInRequest("normal_username"))
    intShowSingleUserInfo($smarty,null,$_REQUEST["normal_username"]);

else if (isInRequest("user_id_multi"))
    intShowMultiUserInfo($smarty,$_REQUEST["user_id_multi"]);

else if (isInRequest("normal_username_multi"))
    intShowMultiNormalUserInfo($smarty,$_REQUEST["normal_username_multi"]);

else if (isInRequest("voip_username_multi"))
    intShowMultiVoIPUserInfo($smarty,$_REQUEST["voip_username_multi"]);
else
    intShowSingleUserInfoInput($smarty);



?>