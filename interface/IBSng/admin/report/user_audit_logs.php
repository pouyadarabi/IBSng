<?php

require_once("../../inc/init.php");
require_once(IBSINC."report.php");
require_once("user_audit_logs/user_audit_logs_report_generator_controller.php");

needAuthType(ADMIN_AUTH_TYPE);

$controller = new UserAuditLogsReportGeneratorController();
$controller->display();
?>