<?php
require_once ("../../inc/init.php");
require_once (IBSINC."report.php");

needAuthType(ADMIN_AUTH_TYPE);

require_once ("web_analyzer_logs/web_analyzer_logs_report_generator_controller.php");

$report_creator = new WebAnalyzerLogsReportGeneratorController();
$report_creator->display();
?>