<?php
require_once("init.php");

class AddInterface extends Request
{
    function AddInterface($interface_name,$comment)
    {
        parent::Request("bw.addInterface",array("interface_name"=>$interface_name,
                                                    "comment"=>$comment));
    }
}

class AddNode extends Request
{
    function AddNode($interface_name,$parent_id,$rate_kbits,$ceil_kbits)
    {
        parent::Request("bw.addNode",array("interface_name"=>$interface_name,
                                           "parent_id"=>$parent_id,
                                           "rate_kbits"=>$rate_kbits,
                                           "ceil_kbits"=>$ceil_kbits));
    }
}

class AddLeaf extends Request
{
    function AddLeaf($leaf_name,$parent_id,$default_rate_kbits,$default_ceil_kbits,$total_rate_kbits,$total_ceil_kbits)
    {
        parent::Request("bw.addLeaf",array("leaf_name"=>$leaf_name,
                                           "parent_id"=>$parent_id,
                                           "default_rate_kbits"=>$default_rate_kbits,
                                           "default_ceil_kbits"=>$default_ceil_kbits,
                                           "total_rate_kbits"=>$total_rate_kbits,
                                           "total_ceil_kbits"=>$total_ceil_kbits));

    }
}

class AddLeafService extends Request
{
    function AddLeafService($leaf_name,$protocol,$filter,$rate_kbits,$ceil_kbits)
    {
        parent::Request("bw.addLeafService",array("leaf_name"=>$leaf_name,
                                                  "protocol"=>$protocol,
                                                  "filter"=>$filter,
                                                  "rate_kbits"=>$rate_kbits,
                                                  "ceil_kbits"=>$ceil_kbits
                                                  ));
    }
}

class GetInterfaces extends Request
{
    function getInterfaces()
    {
        parent::Request("bw.getInterfaces",array());
    }
}

class GetNodeInfo extends Request
{
    function getNodeInfo($node_id)
    {
        parent::Request("bw.getNodeInfo",array("node_id"=>$node_id));
    }
}

class GetLeafInfo extends Request
{
    function getLeafInfo($leaf_name)
    {
        parent::Request("bw.getLeafInfo",array("leaf_name"=>$leaf_name));
    }
}

class GetTree extends Request
{
    function getTree($interface_name)
    {
        parent::Request("bw.getTree",array("interface_name"=>$interface_name));
    }
}

class DelLeafService extends Request
{
    function DelLeafService($leaf_name,$leaf_service_id)
    {
        parent::Request("bw.delLeafService",array("leaf_name"=>$leaf_name,
                                                  "leaf_service_id"=>$leaf_service_id));
    }
}

class GetAllLeafNames extends Request
{
    function GetAllLeafNames()
    {
        parent::Request("bw.getAllLeafNames",array());
    }
}

class DelNode extends Request
{
    function DelNode($node_id)
    {
        parent::Request("bw.delNode",array("node_id"=>$node_id));
    }
}

class DelLeaf extends Request
{
    function DelLeaf($leaf_name)
    {
        parent::Request("bw.delLeaf",array("leaf_name"=>$leaf_name));
    }
}


class DelInterface extends Request
{
    function DelInterface($interface_name)
    {
        parent::Request("bw.delInterface",array("interface_name"=>$interface_name));
    }
}

class UpdateInterface extends Request
{
    function UpdateInterface($interface_id,$interface_name,$comment)
    {
        parent::Request("bw.updateInterface",array( "interface_id"=>$interface_id,
                                                    "interface_name"=>$interface_name,
                                                    "comment"=>$comment));
    }
}

class UpdateNode extends Request
{
    function UpdateNode($node_id,$rate_kbits,$ceil_kbits)
    {
        parent::Request("bw.updateNode",array("node_id"=>$node_id,
                                              "rate_kbits"=>$rate_kbits,
                                              "ceil_kbits"=>$ceil_kbits));
    }
}

class UpdateLeaf extends Request
{
    function UpdateLeaf($leaf_id,$leaf_name,$default_rate_kbits,$default_ceil_kbits,$total_rate_kbits,$total_ceil_kbits)
    {
        parent::Request("bw.updateLeaf",array("leaf_id"=>$leaf_id,
                                           "leaf_name"=>$leaf_name,
                                           "default_rate_kbits"=>$default_rate_kbits,
                                           "default_ceil_kbits"=>$default_ceil_kbits,
                                           "total_rate_kbits"=>$total_rate_kbits,
                                           "total_ceil_kbits"=>$total_ceil_kbits));

    }
}

class UpdateLeafService extends Request
{
    function UpdateLeafService($leaf_name,$leaf_service_id,$protocol,$filter,$rate_kbits,$ceil_kbits)
    {
        parent::Request("bw.updateLeafService",array("leaf_name"=>$leaf_name,
                                                  "leaf_service_id"=>$leaf_service_id,
                                                  "protocol"=>$protocol,
                                                  "filter"=>$filter,
                                                  "rate_kbits"=>$rate_kbits,
                                                  "ceil_kbits"=>$ceil_kbits
                                                  ));
    }
}

class AddBwStaticIP extends Request
{
    function addBwStaticIP($ip_addr,$tx_leaf_name,$rx_leaf_name)
    {
        parent::Request("bw.addBwStaticIP",array("ip_addr"=>$ip_addr,
                                              "tx_leaf_name"=>$tx_leaf_name,
                                              "rx_leaf_name"=>$rx_leaf_name));
    }
}

class UpdateBwStaticIP extends Request
{
    function UpdateBwStaticIP($static_ip_id,$ip_addr,$tx_leaf_name,$rx_leaf_name)
    {
        parent::Request("bw.updateBwStaticIP",array("ip_addr"=>$ip_addr,
                                              "tx_leaf_name"=>$tx_leaf_name,
                                              "rx_leaf_name"=>$rx_leaf_name,
                                              "static_ip_id"=>$static_ip_id));
    }
}

class DelBwStaticIP extends Request
{
    function DelBwStaticIP($ip_addr)
    {
        parent::Request("bw.delBwStaticIP",array("ip_addr"=>$ip_addr));
    }
}

class GetAllBwStaticIPs extends Request
{
    function GetAllBwStaticIPs()
    {
        parent::Request("bw.getAllBwStaticIPs",array());
    }
}

class GetBwStaticIPInfo extends Request
{
    function GetBwStaticIPInfo($ip_addr)
    {
        parent::Request("bw.getBwStaticIPInfo",array("ip_addr"=>$ip_addr));
    }
}

class GetAllActiveLeaves extends Request
{
    function GetAllActiveLeaves()
    {
        parent::Request("bw.getActiveLeaves",array());
    }
}

class GetLeafCharges extends Request
{
    function GetLeafCharges($leaf_name)
    {
        parent::Request("bw.getLeafCharges",array("leaf_name"=>$leaf_name));
    }
}

?>