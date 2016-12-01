<?php

require_once (IBSINC."generator/generator_controller.php");

require_once (IBSINC."generator/report_generator/report_generator.php");
require_once (IBSINC."generator/report_generator/csv_report_generator.php");
require_once (IBSINC."generator/report_generator/xml_report_generator.php");

class ReportGeneratorController extends GeneratorController
{
	function ReportGeneratorController()
	{
		parent :: GeneratorController ();
	}

	function init()
	{
		parent :: init();

		$this->output_filename = "reports";
		$this->view_default_selected_name = "XML";
		$this->registerGenerator("XML", "createXmlGenerator");
		$this->registerGenerator("CSV (TAB)", "createTabCSVGenerator");
		$this->registerGenerator("CSV (Semi Colon)", "createSemiColonCSVGenerator");
		$this->registerGenerator("CSV (Comma)", "createCommaCSVGenerator");
	}

	function getWebGenerator ()
	{
	    $generators = $this->getGenerators();
	    $generator = NULL;

	    if (isset ($generators["WEB"]))
	    {
	        $generator = & $generators["WEB"]();
	        $generator->registerController($this);
	    }
	    	
	    return $generator;
	}

    /**
     * view output
     * */
    function getViewOuputSelectedName()
    {
        $generators_name = array_keys($this->getGenerators());
        $generator_index = isset($_REQUEST["view_options"]) ? $_REQUEST["view_options"] : NULL;
        $ret = $this->view_default_selected_name;

        if ($generator_index !== NULL)
        	$ret = $generators_name[(int)$generator_index];

        return $ret;
    }

	function getGenerator()
	{
		$gen = NULL;

		$gen_func = $this->__generators[$this->getViewOuputSelectedName()];
		eval("\$gen = {$gen_func} ();");
		$gen->registerController ($this);

		return $gen;
	}
}

function createXmlGenerator()
{
	return new XmlReportGenerator();
}

function createTabCSVGenerator()
{
	return new CSVReportGenerator("TAB");
}

function createCommaCSVGenerator()
{
	return new CSVReportGenerator(",");
}

function createSemiColonCSVGenerator()
{
	return new CSVReportGenerator(";");
}
?>