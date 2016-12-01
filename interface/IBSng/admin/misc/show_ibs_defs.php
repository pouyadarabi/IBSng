<?php
require_once("../../inc/init.php");
require_once(IBSINC."ibs_defs.php");

needAuthType(ADMIN_AUTH_TYPE);


if (isInRequest("action"))
    intSaveDefs();
else
    intShowDefs();

function intSaveDefs()
{
    $defs_arr=findDefsInRequest();
    $save_defs_req=new SaveDefs($defs_arr);
    list($success,$err)=$save_defs_req->send();
    if($success)
        intShowDefs(TRUE);
    else
        intShowDefs(FALSE,$err);
}

function findDefsInRequest()
{
    $def_arr=array();
    foreach($_REQUEST as $key=>$value)
    {
        $value=trim($value);
        if (preg_match("/^def_(.*)$/",$key,$matches))
        {
            $def_var=$matches[1];
            if(preg_match("/^(.*)__(.*)__/",$def_var,$matches))
            {
                $def_var=$matches[1];
                $index=$matches[2];

                if(!isset($def_arr[$def_var]))
                    $def_arr[$def_var]=array();

                if($value=="")
                    continue;
                $def_arr[$def_var][]=$value;
            }
            else
                $def_arr[$def_var]=$value;
        }
    }
    return $def_arr;
}

function intShowDefs($save_success=FALSE,$err=null)
{
    $smarty=new IBSSmarty();
    intSetVars($smarty,$save_success,$err);
    intSetDefs($smarty);
    $smarty->display("admin/misc/show_ibs_defs.tpl");
}

function intSetVars(&$smarty,$save_success,$err)
{
    $smarty->assign("save_success",$save_success);
    if(!is_null($err))
        $smarty->set_page_error($err->getErrorMsgs());
}

function intSetDefs(&$smarty)
{
    $get_defs_req=new GetAllDefs();
    list($success,$defs_arr)=$get_defs_req->send();
    if($success)
        $smarty->assign("defs_arr",$defs_arr);
    else
    {
        $smarty->set_page_error($defs_arr->getErrorMsgs());
        $smarty->assign("defs_arr",array());
    }
}



?>