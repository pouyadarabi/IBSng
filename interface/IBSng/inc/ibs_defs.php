<?php
require_once("init.php");

class GetAllDefs extends Request
{
    function getAllDefs()
    {
        parent::Request("ibs_defs.getAllDefs",array());
    }
}

class SaveDefs extends Request
{
    function SaveDefs($defs)
    {
        parent::Request("ibs_defs.saveDefs",array("defs"=>$defs));
    }

}

?>