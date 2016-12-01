<?php

require_once (IBSINC."generator/report_generator/report_generator_controller.php");
require_once ("search_user_web_report_generator.php");

class SearchUserReportGeneratorController extends ReportGeneratorController
{
	function UserConnectionLogsReportGeneratorController()
	{
		parent :: ReportGeneratorController();
	}

	function init()
	{
		parent :: init();
		$this->output_filename = "search_user";
		$this->registerGenerator("WEB", "createSearchUserWebGenerator");
		$this->view_default_selected_name = "WEB";		
	}

    function getCreator ()
    {
        return new SearchUserReportCreator();
    }

	/**
	 * get report selectors
	 * @return array selectors
	 * */
	function getReportSelectors()
	{
		return array_merge(array ("User ID" => "show__basic_user_id|createLinkConnectionLogsUserID"), parent :: getReportSelectors());
	}


}

/**
 * get geneartor for web
 * */
function createSearchUserWebGenerator()
{
	return  new SearchUserWebReportGenerator();
}
?>