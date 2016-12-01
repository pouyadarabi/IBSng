<?php
require_once("init.php");

function tabName2TabID($name)
{
    return str_replace(" ", "_", $name);
}

function tabID2TabName($tab_id)
{
    return str_replace("_", " ", $tab_id);
}

function fixTabName($name)
{
    return str_replace(' ','&nbsp;',$name);
}

function getTabTableID($new)
{
    global $tab_table_id;
    if(!isset($tab_table_id))
        $tab_table_id=0;
    if($new)
        $tab_table_id++;
    return "tab".$tab_table_id;
}
?>