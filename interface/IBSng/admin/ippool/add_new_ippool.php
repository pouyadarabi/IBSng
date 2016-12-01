<?php
require_once("../../inc/init.php");
require_once(IBSINC."ippool_face.php");
require_once(IBSINC."ippool.php");

needAuthType(ADMIN_AUTH_TYPE);

if(isInRequest("ippool_name","comment"))
    intAddIPpool($_REQUEST["ippool_name"],$_REQUEST["comment"]);
else
    face();

function intAddIPpool($ippool_name,$comment)
{
    $add_new_ippool=new AddNewIPpool($ippool_name,$comment);
    list($success,$err)=$add_new_ippool->send();
    if($success)
        redirectToIPpoolInfo($ippool_name);
    else
        face($err);
}

function face($err=NULL)
{
    $smarty=new IBSSmarty();
    intAssignValues($smarty);
    if(!is_null($err))
    {
        intSetErrors($smarty,$err->getErrorKeys());
        $smarty->set_page_error($err->getErrorMsgs());
    }
    $smarty->display("admin/ippool/add_new_ippool.tpl");    
}

function intAssignValues(&$smarty)
{
    $smarty->assign_array(array("ippool_name"=>requestVal("ippool_name"),
                               "comment"=>requestVal("comment")));
}

function intSetErrors(&$smarty,$err_keys)
{
    $smarty->set_field_errs(array("ippool_name_err"=>array("BAD_IP_POOL_NAME",
                                                           "IP_POOL_NAME_ALREADY_EXISTS")
                                                           ),$err_keys);
}

?>