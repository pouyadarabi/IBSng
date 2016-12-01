<?php
require_once("../../inc/init.php");
require_once(IBSINC."graph.php");
require_once(IBSINC."snapshot.php");
require_once(IBSINC."report_lib.php");
require_once("bw_graph_img_funcs.php");

needAuthType(ADMIN_AUTH_TYPE);

if(isInRequest("user_id", "username"))
    intBWGraph($_REQUEST["username"]);
else
{
    toLog("bw_graph_img : Invalid Request");
    exit();
}

