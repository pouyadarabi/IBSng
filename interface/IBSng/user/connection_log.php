<?php

require_once ("../inc/init.php");
require_once (IBSINC."report.php");

require_once ("connection_logs/user_connection_logs_report_generator_controller.php");

needAuthType(NORMAL_USER_AUTH_TYPE,VOIP_USER_AUTH_TYPE);

$controller = new UserConnectionLogsReportGeneratorController();
$controller->display();
?>