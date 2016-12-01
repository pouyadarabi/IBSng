<?php

require_once (IBSINC."generator/generator.php");

class ReportGenerator extends Generator
{
	function ReportGenerator()
	{
		$this->init();
		$this->controller = NULL;
	}

	function init()
	{
    	parent::init();
    	$this->__registered_variables = array();
	}

	/**
	 * register controller
	 * @param Controller $controller
	 * */
	 function registerController (& $controller)
	 {
	     $this->controller = &$controller;
	 }

	/**
	 * register $variable with $value
	 * */
	function registerVar($variable, $value)
	{
		$this->__registered_variables[$variable] = $value;
	}
	
	function getRegisteredVariable($variable)
	{
		if (isset($this->__registered_variables[$variable]))
			return $this->__registered_variables[$variable];
 		toLog("maybe : you must overide this variable '" . $variable . "'\n");
		return "";
	}
}

?>