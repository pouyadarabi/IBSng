<?php
require_once ("../../inc/init.php");
require_once (IBSINC."report.php");

needAuthType(ADMIN_AUTH_TYPE);

require_once ("connections_funcs.php");
require_once ("connection_logs/admin_connection_logs_report_generator_controller.php");

$controller = new AdminConnectionLogsReportGeneratorController();
$controller->display();

?>
