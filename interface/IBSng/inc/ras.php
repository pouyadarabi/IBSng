<?php
require_once("init.php");

class AddNewRas extends Request
{
    function AddNewRas($ras_ip,$ras_description,$ras_type,$radius_secret,$comment)
    {
        parent::Request("ras.addNewRas",array("ras_ip"=>$ras_ip,
                                              "ras_description"=>$ras_description,
                                              "ras_type"=>$ras_type,
                                              "radius_secret"=>$radius_secret,
                                              "comment"=>$comment));
    }
}

class GetRasInfo extends Request
{
    function GetRasInfo($ras_ip)
    {
        parent::Request("ras.getRasInfo",array("ras_ip"=>$ras_ip));
    }
}

class GetActiveRasIPs extends Request
{
    function GetActiveRasIPs()
    {
        parent::Request("ras.getActiveRasIPs",array());
    }
}

class GetRasDescriptions extends Request
{
    function GetRasDescriptions()
    {
        parent::Request("ras.getRasDescriptions",array());
    }
}

class GetInActiveRases extends Request
{
    function GetInActiveRases()
    {
        parent::Request("ras.getInActiveRases",array());
    }
}

class GetRasTypes extends Request
{
    function GetRasTypes()
    {
        parent::Request("ras.getRasTypes",array());
    }
}

class GetRasAttributes extends Request
{
    function GetRasAttributes($ras_ip)
    {
        parent::Request("ras.getRasAttributes",array("ras_ip"=>$ras_ip));
    }
}

class GetRasPorts extends Request
{
    function GetRasPorts($ras_ip)
    {
        parent::Request("ras.getRasPorts",array("ras_ip"=>$ras_ip));
    }
}

class UpdateRasInfo extends Request
{
    function UpdateRasInfo($ras_id,$ras_ip,$ras_description,$ras_type,$radius_secret,$comment)
    {
        parent::Request("ras.updateRasInfo",array("ras_id"=>$ras_id,
                                              "ras_ip"=>$ras_ip,
                                              "ras_description"=>$ras_description,
                                              "ras_type"=>$ras_type,
                                              "radius_secret"=>$radius_secret,
                                              "comment"=>$comment));
    }
}



class UpdateRasAttributes extends Request
{
    function UpdateRasAttributes($ras_ip,$attrs)
    {
        parent::Request("ras.updateAttributes",array("ras_ip"=>$ras_ip,
                                              "attrs"=>$attrs));
    }
}

class ResetRasAttributes extends Request
{
    function ResetRasAttributes($ras_ip)
    {
        parent::Request("ras.resetAttributes",array("ras_ip"=>$ras_ip));
    }
}

class AddRasPort extends Request
{
    function AddRasPort($ras_ip,$port_name,$type,$phone,$comment)
    {
        parent::Request("ras.addPort",array("ras_ip"=>$ras_ip,
                                                    "port_name"=>$port_name,
                                                    "phone"=>$phone,
                                                    "type"=>$type,
                                                    "comment"=>$comment
                                                    ));
    }
}

class GetPortTypes extends Request
{
    function GetPortTypes()
    {
        parent::Request("ras.getPortTypes",array());
    }
}

class DelRasPort extends Request
{
    function DelRasPort($ras_ip,$port_name)
    {
        parent::Request("ras.delPort",array("ras_ip"=>$ras_ip,
                                                    "port_name"=>$port_name
                                                    ));
    }
}

class GetRasPortInfo extends Request
{
    function GetRasPortInfo($ras_ip,$port_name)
    {
        parent::Request("ras.getRasPortInfo",array("ras_ip"=>$ras_ip,
                                                    "port_name"=>$port_name
                                                    ));
    }
}

class UpdateRasPort extends Request
{
    function UpdateRasPort($ras_ip,$port_name,$type,$phone,$comment)
    {
        parent::Request("ras.updatePort",array("ras_ip"=>$ras_ip,
                                                    "port_name"=>$port_name,
                                                    "phone"=>$phone,
                                                    "type"=>$type,
                                                    "comment"=>$comment
                                                    ));
    }
}


class DeActiveRas extends Request
{
    function DeActiveRas($ras_ip)
    {
        parent::Request("ras.deActiveRas",array("ras_ip"=>$ras_ip));
    }
}

class ReActiveRas extends Request
{
    function ReActiveRas($ras_ip)
    {
        parent::Request("ras.reActiveRas",array("ras_ip"=>$ras_ip));
    }
}

class GetRasIPpools extends Request
{
    function GetRasIPpools($ras_ip)
    {
        parent::Request("ras.getRasIPpools",array("ras_ip"=>$ras_ip));
    }
}

class AddIPpoolToRas extends Request
{
    function AddIPpoolToRas($ras_ip,$ippool_name)
    {
        parent::Request("ras.addIPpoolToRas",array("ras_ip"=>$ras_ip,
                                                   "ippool_name"=>$ippool_name
                                                   ));
    }
}

class DelIPpoolFromRas extends Request
{
    function DelIPpoolFromRas($ras_ip,$ippool_name)
    {
        parent::Request("ras.delIPpoolFromRas",array("ras_ip"=>$ras_ip,
                                                     "ippool_name"=>$ippool_name
                                                     ));
    }
}

function getAllActiveRasInfos()
{
    /*
        return a list of associative dictionaries containing all active ras informations
    */
    $ras_infos=array();
    $ras_ips_request=new GetActiveRasIPs();
    list($success,$ras_ips)=$ras_ips_request->send();
    if(!$success)
        return array(FALSE,$ras_ips);
    $ras_info_request=new GetRasInfo("");
    foreach($ras_ips as $ras_ip)
    {
        $ras_info_request->changeParam("ras_ip",$ras_ip);
        list($success,$ras_info)=$ras_info_request->send();
        if(!$success)
            return array(FALSE,$ras_info);
        $ras_infos[]=$ras_info;
    }
    return array(TRUE,$ras_infos);
}

?>