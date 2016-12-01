<?php
require_once("init.php");
require_once(XMLRPCINC."xmlrpc.inc");
require_once(IBSINC."auth.php");

class Request
{ /* This is class for all requests
     other requests may inherit from this class but don't forget to call parent::Request() in constructor
  */

    function Request($server_method,$params_arr)
    {
        $this->server_method=$server_method;
        $this->__addAuthParams($params_arr);
        $this->params_arr=$params_arr;
        $this->setDateTypeParam(null);
        $this->ibs_rpc=new IBSxmlrpc();
    }

    function __addAuthParams(&$params_arr)
    {
        $auth_obj=getAuth();
        list($auth_name,$auth_pass,$auth_type)=$auth_obj->getAuthParams();
        $params_arr["auth_name"]=$auth_name;
        $params_arr["auth_pass"]=$auth_pass;
        $params_arr["auth_type"]=$auth_type;
        $params_arr["auth_remoteaddr"]=getClientIPAddress();
    }

    function setDateTypeParam($date_type)
    {/*
        set "date_type" of this request. 
        if $date_type is null, we try to find a "date_type" in request,session and set it as date_type
        if none was set, use system wide default DATE_TYPE(defs.php)
    */
        if(!is_null($date_type))
            $this->params_arr["date_type"]=$date_type;
        else 
            $this->params_arr["date_type"]=getDateType();
            
    }

    function changeParam($key,$value)
    {/* change internal kept params array, set $key value to $value,
        useful when using one request object for multiple server calls
     */
        $this->params_arr[$key]=$value;
    }

    function send()
    {/* Warning: Deprecated, use sendAndRecv instead, just here for backward compatiblity
        send request, and return the response in format ($success(bool),$msg(mix))
        it will call $this->check(), this function should be override by children in case 
        of they need some checking before sending request
     */
        list($success,$msg)=$this->__check();
        if(!$success)
            return array($success,$msg);
        else
            return $this->ibs_rpc->sendRequest($this->server_method,$this->params_arr);
    }
    
    function sendAndRecv()
    {/* send request, and return an Response instance.
        it will call $this->check(), this function should be override by children in case 
        of they need some checking before sending request
     */
        list($success,$ret_val)=$this->__check();
        if($success)
            list($success,$ret_val)=$this->ibs_rpc->sendRequest($this->server_method,$this->params_arr);
        return $this->createResponse($success,$ret_val);
    }
    
    
    function createResponse($success,$ret_val)
    {
        return new Response($success,$ret_val);
    }
    
    function __check()
    {/*Children can override this function to check inputs before sending the request
       This should return an array of (FALSE,$failure_msg) on failure or (TRUE,don't care) on success
     */
        return array(TRUE,null);
    }
}

class Response
{
    function Response($success,$ret_val)
    {
        $this->result=null;
        $this->error=null;
        $this->success=$success;
        if($success)
            $this->result=$ret_val;
        else
            $this->error=$ret_val;
    }
    
    function isSuccessful()
    {/* return True if request was successful
    
    */
        return $this->success;
    }
    
    function getResult()
    {/* return result of request. IF request was failed, return null
    */
        return $this->result;
    }
    
    function getError()
    {/* return error of a failed request. Null if request was successful
    */
        return $this->error;
    }

    function getErrorMsg()
    {
        return $this->error->getErrorMsg();
    }
    
    function setErrorInSmarty(&$smarty)
    {/* 
    */
        if(!is_null($this->error))
            $smarty->set_page_error($this->error->getErrorMsgs());
    }
}

?>