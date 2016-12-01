<?php
require_once("init.php");

class GetStatistics extends Request
{
    function GetStatistics()
    {
        parent::Request("stat.getStatistics",array());
    }
}

?>