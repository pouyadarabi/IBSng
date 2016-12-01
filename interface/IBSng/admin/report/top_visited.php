<?php
require_once("../../inc/init.php");
require_once(IBSINC."report.php");
require_once("top_visited_funcs.php");

needAuthType(ADMIN_AUTH_TYPE);
$smarty=new IBSSmarty();
session_write_close();
intShowTopVisitedURLs($smarty);

?>