<?php

require_once (IBSINC."generator/xml_generator.php");
require_once (IBSINC."generator/report_generator/xml_report_generator.php");


/**
 * used to crate CSV output
 */

class XmlReportGenerator extends ReportGenerator
{
	/**
	 * @access public
	 */
	function XmlReportGenerator()
	{
        parent :: ReportGenerator ();
	}
	
	function registerController (& $controller)
	{
	    parent::registerController ($controller);

		$root = $this->controller->creator->getRegisteredValue("root_node_name");
		$element = $this->controller->creator->getRegisteredValue("element_node_name");
		
		HeaderGenerator :: assignHeader("XML");
        $this->xml_doc = new XmlGenerator($root, $element);
        print $this->xml_doc->init();
	}

	function doArray($array)
	{
		print $this->xml_doc->doArray($array[$this->controller->creator->getRegisteredValue("root_node_name")]);
	}

	function dispose()
	{
		print $this->xml_doc->dispose();
	}
}
?>