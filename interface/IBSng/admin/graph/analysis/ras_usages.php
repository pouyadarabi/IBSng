<?php
function queryData($conds)
{
    return connectionQueryData($conds,"GetRasUsages");
}

function intShowGraph(&$durations)
{
    connectionDurationShowGraph($durations,"Rases Usage Analysis");
}    

?>