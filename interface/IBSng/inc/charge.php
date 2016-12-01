<?php
require_once("init.php");

class AddNewCharge extends Request
{
    function AddNewCharge($name,$charge_type,$visible_to_all,$comment)
    {
        parent::Request("charge.addNewCharge",array("name"=>$name,
                                                 "comment"=>$comment,
                                                 "charge_type"=>$charge_type,
                                                 "visible_to_all"=>($visible_to_all==TRUE)?"t":"f"
                                                 ));
    }
}

class UpdateCharge extends Request
{
    function UpdateCharge($charge_id,$charge_name,$visible_to_all,$comment)
    {
        parent::Request("charge.updateCharge",array("charge_id"=>$charge_id,
                                                 "charge_name"=>$charge_name,
                                                 "comment"=>$comment,
                                                 "visible_to_all"=>($visible_to_all==TRUE)?"t":"f"
                                                 ));
    }
}


class GetChargeInfo extends Request
{
    function GetChargeInfo($charge_name,$charge_id=null)
    {/*
        $charge_name : name of charge to get info, can be null if you want to set $charge_id
        $charge_id: id of charge to get info, can be null if you want to use $charge_name
    */
        $params=array();
        if(!is_null($charge_name))
            $params["charge_name"]=$charge_name;
        else if (!is_null($charge_id))
            $params["charge_id"]=$charge_id;

        parent::Request("charge.getChargeInfo",$params);
    }
}


class AddInternetChargeRule extends Request
{
    function AddInternetChargeRule($charge_name,$rule_start,$rule_end,$cpm,$cpk,
                            $assumed_kps,$bandwidth_limit_kbytes,$tx_leaf_name,$rx_leaf_name,$ras,$ports,$dows)
    {
        parent::Request("charge.addInternetChargeRule",array("charge_name"=>$charge_name,
                                                             "rule_start"=>$rule_start,
                                                             "rule_end"=>$rule_end,
                                                             "cpm"=>$cpm,
                                                             "cpk"=>$cpk,
                                                             "assumed_kps"=>$assumed_kps,
                                                             "bandwidth_limit_kbytes"=>$bandwidth_limit_kbytes,
                                                             "tx_leaf_name"=>$tx_leaf_name,
                                                             "rx_leaf_name"=>$rx_leaf_name,
                                                             "ras"=>$ras,
                                                             "ports"=>$ports,
                                                             "dows"=>$dows
                                                             ));
    }
}

class ListChargeRules extends Request
{
    function ListChargeRules($charge_name)
    {
        parent::Request("charge.listChargeRules",array("charge_name"=>$charge_name));
    }
}

class ListCharges extends Request
{
    function ListCharges($charge_type=null)
    {
        if(is_null($charge_type))
            $params=array();
        else
            $params=array("charge_type"=>$charge_type);

        parent::Request("charge.listCharges",$params);
    }
}

class UpdateInternetChargeRule extends Request
{
    function UpdateInternetChargeRule($charge_name,$charge_rule_id,$rule_start,$rule_end,$cpm,$cpk,
                            $assumed_kps,$bandwidth_limit_kbytes,$tx_leaf_name,$rx_leaf_name,$ras,$ports,$dows)
    {
        parent::Request("charge.updateInternetChargeRule",array("charge_name"=>$charge_name,
                                                             "charge_rule_id"=>$charge_rule_id,
                                                             "rule_start"=>$rule_start,
                                                             "rule_end"=>$rule_end,
                                                             "cpm"=>$cpm,
                                                             "cpk"=>$cpk,
                                                             "assumed_kps"=>$assumed_kps,
                                                             "bandwidth_limit_kbytes"=>$bandwidth_limit_kbytes,
                                                             "tx_leaf_name"=>$tx_leaf_name,
                                                             "rx_leaf_name"=>$rx_leaf_name,
                                                             "ras"=>$ras,
                                                             "ports"=>$ports,
                                                             "dows"=>$dows
                                                             ));
    }
}

class DelChargeRule extends Request
{
    function DelChargeRule($charge_rule_id,$charge_name)
    {
        parent::Request("charge.delChargeRule",array("charge_rule_id"=>$charge_rule_id,
                                                     "charge_name"=>$charge_name));
    }
}

class DelCharge extends Request
{
    function DelCharge($charge_name)
    {
        parent::Request("charge.delCharge",array("charge_name"=>$charge_name));
    }
}

class AddVoIPChargeRule extends Request
{
    function AddVoIPChargeRule($charge_name,$rule_start,$rule_end,$tariff_name,$ras,$ports,$dows)
    {
        parent::Request("charge.addVoIPChargeRule",array("charge_name"=>$charge_name,
                                                             "rule_start"=>$rule_start,
                                                             "rule_end"=>$rule_end,
                                                             "tariff_name"=>$tariff_name,
                                                             "ras"=>$ras,
                                                             "ports"=>$ports,
                                                             "dows"=>$dows
                                                             ));
    }
}

class UpdateVoIPChargeRule extends Request
{
    function UpdateVoIPChargeRule($charge_name,$charge_rule_id,$rule_start,$rule_end,$tariff_name,$ras,$ports,$dows)
    {
        parent::Request("charge.updateVoIPChargeRule",array("charge_name"=>$charge_name,
                                                             "charge_rule_id"=>$charge_rule_id,
                                                             "rule_start"=>$rule_start,
                                                             "rule_end"=>$rule_end,
                                                             "tariff_name"=>$tariff_name,
                                                             "ras"=>$ras,
                                                             "ports"=>$ports,
                                                             "dows"=>$dows
                                                             ));
    }
}


?>
