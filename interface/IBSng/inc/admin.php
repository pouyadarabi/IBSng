<?php
require_once("init.php");

class AddNewAdmin extends Request
{
    function AddNewAdmin($username,$password1,$password2,$name,$comment)
    {
        $this->password1=$password1;
        $this->password2=$password2;

        parent::Request("admin.addNewAdmin",array("username"=>$username,
                                                  "password"=>$password1,
                                                  "name"=>$name,
                                                  "comment"=>$comment
                                                  )
                        );
    }

    function __check()
    {
        return checkPasswordMatch($this->password1,$this->password2);
    }

}

class GetAdminInfo extends Request
{
    function GetAdminInfo($admin_username)
    {
        parent::Request("admin.getAdminInfo",array("admin_username"=>$admin_username));
    }
}

class GetAllAdminUsernames extends Request
{
    function GetAllAdminUsernames()
    {
        parent::Request("admin.getAllAdminUsernames",array());
    }
}

function getAllAdminInfos()
{
    $admin_infos=array();
    $admin_users_request=new GetAllAdminUsernames();
    list($success,$admin_users)=$admin_users_request->send();
    if(!$success)
        return array(FALSE,$admin_users);
    $admin_info_request=new GetAdminInfo("");
    foreach($admin_users as $username)
    {
        $admin_info_request->changeParam("admin_username",$username);
        list($success,$admin_info)=$admin_info_request->send();
        if(!$success)
            return array(FALSE,$admin_info);
        $admin_infos[]=$admin_info;
    }
    return array(TRUE,$admin_infos);
}

class AdminChangePassword extends Request
{
    function AdminChangePassword($username,$password1,$password2)
    {
        $this->password1=$password1;
        $this->password2=$password2;

        parent::Request("admin.changePassword",array("admin_username"=>$username,
                                                     "new_password"=>$password1
                                                    )
                        );
    }

    function __check()
    {
        return checkPasswordMatch($this->password1,$this->password2);
    }

}

class UpdateAdminInfo extends Request
{
    function UpdateAdminInfo($admin_username,$name,$comment)
    {
        $params_arr=array("admin_username"=>$admin_username,
                          "name"=>$name,
                          "comment"=>removeCR($comment)
                         );
        parent::Request("admin.updateAdminInfo",$params_arr);
    }
}

class ChangeDeposit extends Request
{
    function ChangeDeposit($admin_username,$deposit_change,$comment)
    {
        parent::Request("admin.changeDeposit",array("admin_username"=>$admin_username,
                                                      "deposit_change"=>$deposit_change,
                                                      "comment"=>$comment
                                                      ));
    }
}

class DeleteAdmin extends Request
{
    function DeleteAdmin($admin_username)
    {
        parent::Request("admin.deleteAdmin",array("admin_username"=>$admin_username));
    }
}

class LockAdmin extends Request
{
    function LockAdmin($admin_username,$reason)
    {
        parent::Request("admin.lockAdmin",array("admin_username"=>$admin_username,
                                                "reason"=>$reason));
    }
}

class UnlockAdmin extends Request
{
    function UnlockAdmin($admin_username,$lock_id)
    {
        parent::Request("admin.unlockAdmin",array("admin_username"=>$admin_username,
                                                  "lock_id"=>$lock_id));
    }
}


?>