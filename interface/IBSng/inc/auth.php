<?php
require_once("init.php");
require_once(IBSINC."xmlrpc.php");
require_once(IBSINC."smarty.php");

define("ADMIN_AUTH_TYPE","ADMIN");
define("NORMAL_USER_AUTH_TYPE","NORMAL_USER");
define("VOIP_USER_AUTH_TYPE","VOIP_USER");
define("ANONYMOUS_AUTH_TYPE","ANONYMOUS");

function auth_init()
{
    if(!sessionIsSet("auth"))
        createAnonymousAuth();
}

function doLogout()
{
    session_unset();
    auth_init();
    face();
}


function createAnonymousAuth()
{
    new Auth("anonymous","anonymous",ANONYMOUS_AUTH_TYPE);
}

function getAuth()
{
    return sessionGetVar("auth");
}

function getAuthUsername()
{
    $auth=getAuth();
    return $auth->getAuthUsername();
}

function needAuthType()
{
    $auth_obj=getAuth();
    $auth_obj->needAuthType(func_get_args());
}

function adminAuth($auth_name,$auth_pass)
{
    return doAuth($auth_name,$auth_pass,ADMIN_AUTH_TYPE);
}

function doAuth($auth_name,$auth_pass,$auth_type)
{
    $auth_obj=new Auth($auth_name,$auth_pass,$auth_type);
    return array($auth_obj->successful(),$auth_obj->getAuthMsg());
}

function showAccessDenied($auth_type)
{
    switch($auth_type)
    {
        case ADMIN_AUTH_TYPE:
            $url="/IBSng/admin";
            $role="admin";
            break;

        case NORMAL_USER_AUTH_TYPE:
        case VOIP_USER_AUTH_TYPE:
            $url="/IBSng/user";
            $role="user";
            break;

        default:
            $url="/IBSng/admin";
            $role="";
            break;

    }
    $smarty=new IBSSmarty();
    $smarty->assign_array(array("url"=>$url,"role"=>$role));
    $smarty->display("access_denied.tpl");
    exit();
}


class Auth
{
    
    function Auth($auth_name,$auth_pass,$auth_type)
    {
        $this->auth_name=$auth_name;
        $this->auth_pass=$auth_pass;
        $this->auth_type=$auth_type;
        list($success,$msg)=$this->__authenticateUser();
        $this->__saveResult($success,$msg);
        if ($success)
            $this->__addToSession();

    }

    function __authenticateUser()
    {/*
        Authenticate the user, based on $this->auth_name , $this->auth_pass, $this->auth_type
        return array of (is_successfull,msg)

        NOTE: all visitors have anonymous auth_type until they login with another auth_type
     */
        if($this->auth_type!=ANONYMOUS_AUTH_TYPE)
        {
            $this->__checkPrevAuthType();
            list($success,$msg)=$this->__sendAuthRequest();
            return array($success,$msg);
        }
        else
            return array(TRUE,"");      
    }

    
    function __checkPrevAuthType()
    {/* Check if user has previously auth object in session
        When user tries an auth request, he must be anononymous, cause authenticated user
        doesn't need to authenticate again, so this means logout (clear authentication) user when he tries 
        to login again
     */
        if (sessionIsSet("auth"))
        {
            $prev_auth=sessionGetVar("auth");
            if($prev_auth->getAuthType()!=ANONYMOUS_AUTH_TYPE)
                createAnonymousAuth();
        }
    }
    
    function __addToSession()
    {
        sessionRegister("auth",$this);
    }


    function __sendAuthRequest()
    {
        $request=new Request("login.login",array("login_auth_name"=>$this->auth_name,
                                                 "login_auth_pass"=>$this->auth_pass,
                                                 "login_auth_type"=>$this->auth_type));
        return $request->send();
                                    
    }

    function getAuthUsername()
    {
        return $this->auth_name;
    }

    function getAuthType()
    {
        return $this->auth_type;
    }

    function getAuthParams()
    {/*
        return an array of (auth_name,auth_pass,auth_type)
        
     */
        return array($this->auth_name,$this->auth_pass,$this->auth_type);
    }
    
    function needAuthType($auth_types)
    {
        /* called when a page need authenticated user with on of types $auth_types
           print an access denied message and exit when user is not authenticated with that 
           auth_type
           $auth_types: array of auth types
        */
        if(!in_array($this->auth_type,$auth_types))
            showAccessDenied($auth_types[0]);

    }
    
    function __saveResult($success,$msg)
    {
        $this->success=$success;
        $this->msg=$msg;
    }

    function successful()
    {/* was authentication successful? or authentication failed */
    
        return $this->success;
    }
    
    function getAuthMsg()
    {/* return message recieved from server while authentication, normally useful when it fails*/
        return $this->msg;
    }


}

?>