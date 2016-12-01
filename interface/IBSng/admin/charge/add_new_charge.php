<?php
require_once("../../inc/init.php");
require_once(IBSINC."charge_face.php");
require_once(IBSINC."charge.php");

needAuthType(ADMIN_AUTH_TYPE);

if(isInRequest("charge_name","charge_type","comment"))
    intAddCharge($_REQUEST["charge_name"],$_REQUEST["charge_type"],isInRequest("visible_to_all"),$_REQUEST["comment"]);
else
    face();

function intAddCharge($charge_name,$charge_type,$visible_to_all,$comment)
{
    $add_charge_req=new AddNewCharge($charge_name,$charge_type,$visible_to_all,$comment);
    list($success,$err)=$add_charge_req->send();
    if($success)
        redirectToChargeInfo($charge_name);
    else
        face($err);
}

function face($err=NULL)
{
    $smarty=new IBSSmarty();
    intAssignValues($smarty);
    intSetChargeTypes($smarty);
    if(!is_null($err))
    {
        intSetErrors($smarty,$err->getErrorKeys());
        $smarty->set_page_error($err->getErrorMsgs());
    }
    $smarty->display("admin/charge/add_new_charge.tpl");    
}

function intAssignValues(&$smarty)
{
    $smarty->assign_array(array("charge_name"=>requestVal("charge_name"),
                               "charge_type"=>requestVal("charge_type"),
                               "visible_to_all"=>checkBoxValue("visible_to_all"),
                               "comment"=>requestVal("comment")
                              ));
}

function intSetErrors(&$smarty,$err_keys)
{
    $smarty->set_field_errs(array("charge_name_err"=>array("CHARGE_NAME_EXISTS"),
                                  "charge_type_err"=>array("RAS_TYPE_NOT_REGISTERED")
                                    ),$err_keys);

}

?>