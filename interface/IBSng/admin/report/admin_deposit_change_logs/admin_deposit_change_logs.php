<?php
require_once ("../../../inc/init.php");
require_once (IBSINC."report.php");

needAuthType(ADMIN_AUTH_TYPE);

require_once ("admin_deposit_change_logs_report_generator_controller.php");

$report_creator = new AdminDepositChangeLogsReportGeneratorController();
$report_creator->display();
?>