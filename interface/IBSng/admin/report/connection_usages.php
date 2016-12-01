<?php
require_once ("../../inc/init.php");
require_once (IBSINC."report.php");

require_once ("connection_usages/connection_usages_report_generator_controller.php");

needAuthType(ADMIN_AUTH_TYPE);

$controller = new ConnectionUsageReportGeneratorController();
$controller->display();
?>