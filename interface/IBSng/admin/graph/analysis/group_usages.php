<?php

function queryData($conds)
{
    return connectionQueryData($conds,"GetGroupUsages");
}

function intShowGraph(&$durations)
{
    connectionDurationShowGraph($durations,"Groups Usage Analysis");
}    
?>
