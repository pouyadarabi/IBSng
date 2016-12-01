<?php
require_once("../inc/init.php");
require_once(IBSINC."graph.php");
require_once(IBSINC."snapshot.php");
require_once(IBSINC."report_lib.php");
require_once("../admin/graph/bw_graph_img_funcs.php");

needAuthType(NORMAL_USER_AUTH_TYPE, VOIP_USER_AUTH_TYPE);
intBWGraph("You");
