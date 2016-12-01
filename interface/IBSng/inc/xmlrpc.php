<?php
require_once("init.php");
require_once(XMLRPCINC."xmlrpc.inc");
require_once(IBSINC."auth.php");
require_once(IBSINC."lib.php");

class IBSxmlrpc
{
    function IBSxmlrpc($server_ip=XMLRPC_SERVER_IP,$server_port=XMLRPC_SERVER_PORT)
    {
    /*
        $server_ip: xml rpc server ip address
        $server_port: xml rpc serer port
    */
        $this->client=new xmlrpc_client("/",$server_ip,$server_port);
        $this->client->setDebug(FALSE);
    }

    function sendRequest($server_method,$params_arr,$timeout=XMLRPC_TIMEOUT)
    {
    /*
        Send request to $server_method, with parameters $params_arr
        $server_method: method to call ex admin.addNewAdmin
        $params_arr: an array of parameters
    */
        $xml_rpc_msg=$this->__createXmlRpcMsg($server_method,$params_arr);
        $response=$this->__sendXmlRpcRequest($xml_rpc_msg,$timeout);
        $result=$this->__returnResponse($response);
        unset($response);
        return $result;
    }

    function __createXmlRpcMsg($server_method,$params_arr)
    {
        $xml_val=php_xmlrpc_encode($params_arr);
        $xml_msg=new xmlrpcmsg($server_method);
        $xml_msg->addParam($xml_val);
        return $xml_msg;
    }
    
    function __sendXmlRpcRequest($xml_rpc_msg,$timeout)
    {
        return $this->client->send($xml_rpc_msg,$timeout);
    }
    
    function __returnResponse($response)
    {
        if ($response==FALSE)
            return $this->__returnError("Error occured while connecting to server");
        else if ($response->faultCode() != 0)
            return $this->__returnError($response->faultString());
        else
            return $this->__returnSuccess($response->value());
    }

    function __returnError($err_str)
    {
        return array(FALSE,new Error($err_str));
    }
    
    function __returnSuccess($value)
    {
        return array(TRUE,php_xmlrpc_decode($value));
    }
    
}

?>