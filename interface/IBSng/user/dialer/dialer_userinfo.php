<?php
require_once("../../inc/init.php");
require_once(IBSINC."dialer.php");
require_once(IBSINC."user.php");
require_once(IBSINC."xml.php");

needDialerAuth();

intUserInfo();

function intUserInfo()
{
    $resp = intGetUserInfo();
    if($resp->isSuccessful())
        print answerDialer(TRUE,encodeUserInfo($resp->getResult()));
    else
    {
        $err_obj=$resp->getError();
        print answerDialer(FALSE,"",$err_obj->getErrorMsg());
    }
}

function intGetUserInfo()
{
    $normal_username=getAuthUsername();
    $req=new GetUserInfo(null,$normal_username);
    $resp=$req->sendAndRecv();
    return $resp;
}

function encodeUserInfo($user_info)
{
    $encoded_str="";
    foreach($user_info["attrs"] as $attr_name=>$attr_value)
        $encoded_str.=encodeAttr($attr_name,$attr_value);

    foreach($user_info["basic_info"] as $attr_name=>$attr_value)
        $encoded_str.=encodeAttr($attr_name,$attr_value);

    return $encoded_str;
}

function encodeAttr($attr_name,$attr_value)
{
    $attr_value=cdataWrap($attr_value);
    return "<attribute><name>{$attr_name}</name><value>{$attr_value}</value></attribute>";
}

?>