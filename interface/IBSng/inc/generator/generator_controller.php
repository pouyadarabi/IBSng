<?php


/**
 * 
 * */

class GeneratorController
	{
    function GeneratorController()
    {
        $this->init();
        $this->smarty = new IBSSmarty();
		$this->creator = $this->getCreator();
		$this->creator->registerController($this);
		$this->generator = $this->getGenerator();
    }

    function init()
    {
        $this->__generators = array ();
    }

    /**
     * display output view
     * */
    function display()
	{
    	$this->creator->create();
    }

	/**
	 * get report result and needed variable from it.
	 * */
	function extractVarsFromResults (& $results)
	{
	}

	/**
	 * abstract function getCreator()
	 * TODO: you must overide this function
	 * @return Creator
	 * */
	function getCreator ()
	{
	    return NULL;
	}

	/**
	 * abstract function getGenerator()
	 * TODO: you must overide this function
	 * @return Generator
	 * */
	function getGenerator ()
	{
	    return NULL;
	}

	/**
	 * for any variable of REQUEST if it start with $selector_expression then is added to return array.
	 * example :
	 * 		getReportSelectors("show__") return an array that contains this variables 
	 * 		"show__details_username", "show__derails_userid", ... that this variables come from
	 * 		REQUEST.
	 * 
	 * @param string $begin_expression like this : show__details_ each var that start with this 
	 * 		expression will be selected 
	 * @return array 
	 * */
	function getReportSelectors($begin_expression = "show__") {
		$selectors = array ();
		$search_replace = array ("_" => " ", "SLASH" => "/");

		// searching in REQUEST and find selectors each selector start with $selector_start
		foreach ($_REQUEST as $field_name => $field_formula)
			if (ereg("^" . $begin_expression . ".*", $field_formula))
				$selectors[str_replace( array_keys($search_replace),
						  	array_values($search_replace),
						  	$field_name)] = $field_formula;

		return $selectors;
	}

    /**
     * map $generator_name with it's function
     * @param $generator_name string name of generator (WEB for example)
     * @param $generator_function string function name (createWebGenerator for example)
     * */
    function registerGenerator($generator_name, $generator_function)
    {
        $this->__generators = array_merge(array($generator_name => $generator_function), $this->__generators);
    }
	
	function getGenerators ()
	{
	    return $this->__generators;
	}
}
?>