<?php

require_once (IBSINC . "generator/report_generator/report_generator_controller.php");
require_once ("connection_logs_web_report_generator.php");

class ConnectionLogsReportGeneratorController extends ReportGeneratorController
{
    function ConnectionLogsReportGeneratorController()
    {
        parent :: ReportGeneratorController();
    }

    function init()
    {
        parent :: init();

        $this->output_filename = "connection_logs_reports";
        $this->view_default_selected_name = "WEB";
    }
}