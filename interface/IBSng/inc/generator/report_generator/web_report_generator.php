<?php
require_once (IBSINC."generator/report_generator/report_generator.php");
require_once (IBSINC."generator/report_generator/modifiers.php");

class WebReportGenerator extends ReportGenerator
{
	function WebReportGenerator()
	{
		parent :: ReportGenerator();
		session_write_close();
		$this->init();
	}

	function init()
	{
		parent :: init();
		$this->smarty_generation_mode = "normal_mode";
		$this->initSmartyValues();
		$this->registerVar("smarty_file_name", "must_be_overided");
		$this->all_reports = array ();
	}

    /**
     * initialize Smarty values and values that will be shown and prefixes ...
     * */
    function initSmartyValues()
    {
        $this->foreach_item = "\$row";
        $this->generated_tpl_header_name = "generated_tpl_header"; 
        $this->generated_tpl_body_name ="generated_tpl_body";
    }

	function doArray($array)
	{
		$this->all_reports[] = &$array;
	}

	function createReportBodyTable()
	{
		$ret = "";
		foreach ($this->controller->getReportSelectors() as $field_name => $formula_name)
			$ret .= $this->getFieldForBodyTpl(deletePrefixFromFormula($this->controller->creator->getRegisteredValue("formula_prefixes"), $formula_name));

		return $ret;
	}

	function createReportHeaderTable()
	{
		$ret = "";

		foreach ($this->controller->getReportSelectors() as $field_name => $formula_name)
			$ret .= $this->getFieldForHeaderTpl($field_name);

		return $ret;
	}

	function getFieldForBodyTpl($footer_field)
	{
		$footer_field = ereg_replace(",[a-zA-Z0-9_]+", "", $footer_field);       
		return "{listTD} {{$this->foreach_item}.".$this->controller->creator->getRegisteredValue("root_node_name").".{$footer_field}} {/listTD}\n";
	}

	function getFieldForHeaderTpl($header_field)
	{
		return "{listTD} <nobr>{$header_field}</nobr> {/listTD}\n";
	}

	function getListTd($tag)
	{
		return "{listTD} {{$tag}} {/listTD}\n";
	}

	function getMathIncrementEquation($assign, $attribute)
	{
		return "{math equation=\"x + y\" assign={$assign} x=`\$row.".$this->controller->creator->getRegisteredValue("root_node_name").".$attribute` y=`\${$assign}` }\n";
	}

	function getMathIncrementEquationFromRow($assign, $attribute)
	{
		return "{math equation=\"x + y\" assign={$assign} x=`\$row.$attribute` y=`\${$assign}` }\n";
	}

	function displaySmarty()
	{
		$this->controller->smarty->display($this->getRegisteredVariable("smarty_file_name"));
	}

	function doFastModeFromating()
	{
		$this->smarty_generation_mode = "fast_mode";
	}
	

    /**
     * set output formatter's name
     * @param array $options array of WEB, XML, ... for example
     * @param array $default default value for output formatter
     * */
    function setViewOptions()
    {
        $options = array_keys($this->controller->getGenerators());
        $default = array_flip($options);

        $default = $default[$this->controller->view_default_selected_name];
	    $this->controller->smarty->assign("view_options", $options);
        $this->controller->smarty->assign("view_by_default", requestVal("view_options", $default));
    }

	function dispose()
	{
		if ($this->smarty_generation_mode == "normal_mode")
		{
        	$this->controller->smarty->assign("{$this->generated_tpl_body_name}", $this->createReportBodyTable());
        	$this->controller->smarty->assign("{$this->generated_tpl_header_name}", $this->createReportHeaderTable());
		}
		$this->controller->smarty->assign("fast_mode", ($this->smarty_generation_mode == "fast_mode"));
        $this->controller->smarty->assign("root_node_name", $this->controller->creator->getRegisteredValue("root_node_name"));
        $this->controller->smarty->assign("number_of_selections", count($this->controller->getReportSelectors()));
        $this->setViewOptions();
        $this->assignReports();
		$this->displaySmarty();
	}

    /**
     * assign Reports to Smarty
     * */
    function assignReports()
    {
        $this->controller->smarty->assign_by_ref("reports", $this->all_reports);
    }
}

/**
 * 
 * $formala_prefixes array of prefixes
 * for deleting prefix of one formula
 * show__details__formula_name == deleting==> formaula_name
 * it is used for deletePrefixFromFormula($this->formula_prefixes, $formula_name)
 * 
 * */

function deletePrefixFromFormula($prefixes, $formula_name)
{
    return str_replace($prefixes, "", $formula_name);
}

?>