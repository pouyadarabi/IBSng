<?php

require_once (IBSINC."generator/csv_generator.php");

/**
 * used to crate CSV output
 */
class CSVReportGenerator extends ReportGenerator
{
	/**
	 * @access public
	 */
	function CSVReportGenerator($csv)
	{
        $this->csv = $csv;
		parent :: ReportGenerator();
	}

	function init()
	{
		parent :: init();
		
	}
	
	function registerController (& $controller)
	{
	    parent :: registerController ($controller);
	    $this->csv = &new OutputCSVGenerator($this->csv, $this->controller->output_filename.".csv");
	    $this->doArray(array($this->controller->creator->getRegisteredValue("root_node_name") =>
	    	array_keys($this->controller->getReportSelectors())));
	}

	function doArray($array)
	{
		$this->csv->doArray($array[$this->controller->creator->getRegisteredValue("root_node_name")]);
	}

}
?>