<?php
require_once("../../inc/init.php");
require_once(IBSINC."ippool.php");
require_once(IBSINC."ippool_face.php");
require_once(IBSINC."perm.php");

needAuthType(ADMIN_AUTH_TYPE);
$smarty=new IBSSmarty();
intIPpoolList($smarty);

function intSetAllIPpoolInfos(&$smarty)
{/*     Assign all ippool infos into smarty variable "$ippool_infos"
        or set a page error if error occured
*/
    list($success,$ippool_infos)=getIPpoolInfos();
    if(!$success)
    {
        $smarty->set_page_error($ippool_infos->getErrorMsgs());
        $smarty->assign("ippool_infos",array());
    }
    else
    {
        array_map("intMakeIPtext",$ippool_infos);
        $smarty->assign("ippool_infos",$ippool_infos);
    }
}

function intMakeIPtext(&$ippool_info)
{
    $ippool_info["ips_text"]=join(", ",$ippool_info["ip_list"]);
}       

function intIPpoolList(&$smarty)
{
    intSetAllIPpoolInfos($smarty);
    face($smarty);
}

function face(&$smarty)
{
    intSetErrors($smarty);
    $smarty->display("admin/ippool/ippool_list.tpl");
}

function intSetErrors(&$smarty)
{
    if(isInRequest("msg"))
        $smarty->set_page_error(array($_REQUEST["msg"]));
}


?>