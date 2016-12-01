<?php
require_once("init.php");

class AddNewUsers extends Request
{
    function AddNewUsers($count,$credit,$owner_name,$group_name,$credit_comment)
    {
        parent::Request("user.addNewUsers",array("count"=>$count,
                                                 "credit"=>$credit,
                                                 "owner_name"=>$owner_name,
                                                 "group_name"=>$group_name,
                                                 "credit_comment"=>$credit_comment
                                                 ));
    }
}

class GetUserInfo extends Request
{
    function GetUserInfo($user_id=null,$normal_username=null,$voip_username=null)
    {
        if (!is_null($user_id))
            $request=array("user_id"=>$user_id);
        else if (!is_null($normal_username))
            $request=array("normal_username"=>$normal_username);
        else if (!is_null($voip_username))
            $request=array("voip_username"=>$voip_username);
        parent::Request("user.getUserInfo",$request);
    }
}

class UpdateUserAttrs extends Request
{
    function UpdateUserAttrs($user_id,$attrs,$to_del_attrs)
    {
        parent::Request("user.updateUserAttrs",array("user_id"=>$user_id,
                                                       "attrs"=>$attrs,
                                                       "to_del_attrs"=>$to_del_attrs));
    }
}

class CheckNormalUsernameForAdd extends Request
{
    function CheckNormalUsernameForAdd($username,$current_username)
    {
        parent::Request("normal_user.checkNormalUsernameForAdd",array("normal_username"=>$username,
                                                               "current_username"=>$current_username));
    }
}

class CheckVoIPUsernameForAdd extends Request
{
    function CheckVoIPUsernameForAdd($username,$current_username)
    {
        parent::Request("voip_user.checkVoIPUsernameForAdd",array("voip_username"=>$username,
                                                               "current_username"=>$current_username));
    }
}

class ChangeUserCredit extends Request
{
    function ChangeUserCredit($user_id,$credit,$credit_comment)
    {
        parent::Request("user.changeCredit",array("user_id"=>$user_id,
                                                  "credit"=>$credit,
                                                  "credit_comment"=>$credit_comment));
    }
}

class DelUser extends Request
{
    function DelUser($user_id,$comment,$del_connection_logs,$del_audit_logs)
    {
        parent::Request("user.delUser",array("user_id"=>$user_id,
                                             "delete_comment"=>$comment,
                                             "del_connection_logs"=>$del_connection_logs,
                                             "del_audit_logs"=>$del_audit_logs));
    }
}

class KillUser extends Request
{
    function KillUser($user_id,$ras_ip,$unique_id_val,$kill)
    {
        parent::Request("user.killUser",array("user_id"=>$user_id,
                                              "ras_ip"=>$ras_ip,
                                              "unique_id_val"=>$unique_id_val,
                                              "kill"=>$kill
                                              ));
    }    
}

class SearchAddUserSaves extends Request
{
    function SearchAddUserSaves(&$conds,$from,$to,$order_by,$desc)
    {
        parent::Request("addUserSave.searchAddUserSaves",array("conds"=>$conds,
                                                               "from"=>$from,
                                                               "to"=>$to,
                                                               "order_by"=>$order_by,
                                                               "desc"=>$desc));
    }    
}

class DeleteAddUserSaves extends Request
{
    function DeleteAddUserSaves($add_user_save_ids)
    {
        parent::Request("addUserSave.deleteAddUserSaves",array("add_user_save_ids"=>$add_user_save_ids));
    }
}

function getUsersInfoByUserID(&$smarty,$user_ids)
{/*return a list of user_infos of users with id in $user_ids
 */ 
    if(sizeof($user_ids)==0)
        return array();

    $req=new GetUserInfo(join(",",$user_ids));
    $resp=$req->sendAndRecv();
    if($resp->isSuccessful())
        return $resp->getResult();
    else
    {
        $resp->setErrorInSmarty($smarty);
        return array();
    }
}

class ChangeNormalPassword extends Request
{
    function ChangeNormalPassword($username,$password1,$password2,$old_password="")
    { /* username will be ignored for user requests
         old_password will be ignored for admin requests
    */
        $this->password1=$password1;
        $this->password2=$password2;

        parent::Request("normal_user.changePassword",array("normal_username"=>$username,
                                                     "password"=>$password1,
                                                     "old_password"=>$old_password
                                                        )
                        );
    }

    function __check()
    {
        return checkPasswordMatch($this->password1,$this->password2);
    }

}

class ChangeVoIPPassword extends Request
{
    function ChangeVoIPPassword($username,$password1,$password2,$old_password="")
    { /* username will be ignored for user requests
         old_password will be ignored for admin requests
    */
    
        $this->password1=$password1;
        $this->password2=$password2;

        parent::Request("voip_user.changePassword",array("voip_username"=>$username,
                                                     "password"=>$password1,
                                                     "old_password"=>$old_password
                                                        )
                        );
    }

    function __check()
    {
        return checkPasswordMatch($this->password1,$this->password2);
    }

}

class CalcApproxDuration extends Request
{
    function CalcApproxDuration($user_id)
    {
        parent::Request("user.calcApproxDuration",array("user_id"=>$user_id));
    }
}


?>