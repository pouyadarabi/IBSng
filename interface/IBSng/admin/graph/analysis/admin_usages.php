<?php
function queryData($conds)
{
    return connectionQueryData($conds,"GetAdminUsages");
}

function intShowGraph(&$durations)
{
    connectionDurationShowGraph($durations,"Admins Usage Analysis");
}    

