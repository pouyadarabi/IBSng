<?php


/**
 * 
 * */

require_once (IBSINC . "generator/creator.php");

class ReportCreator extends Creator {
	function ReportCreator() {
		// initilized variables
		$this->init();
	}

	function create() {
		// Reports
		$reports = array ();

		if ($this->canShowReports())
		{
		    $response_results = $this->getResonseResults();
		    $this->controller->extractVarsFromResults($response_results);
		    $reports = $this->getReports($response_results);
		}

		$generator = & $this->controller->getWebGenerator();

		if (!$this->getRegisteredValue("error_occured"))
		{
			if (!isset ($this->conds["fast_mode"]))
			{
				$generator = & $this->controller->generator; 
				$this->doFormatting($generator, $reports);
			}
			else
				$generator->doFastModeFromating();
		}

		// show information
		$generator->dispose();
	}

	/**
	 * formating report with Formatter($gen)
	 * 
	 * @param Generator $gen formatter
	 * @param mixed $reports object that must be formt
	 * */
	function doFormatting(& $gen, & $reports) {
		foreach ($reports as $report)
			/**
			 * filtering $report
			 * to get information that must be shown 
			 * */
			$gen->doArray($this->__getFilteredOutputReport($report));
	}

	/**
	 * this method initializes variables
	 * */
	function init() {
		parent :: init();

		// register informations
		$this->register("formula_prefixes", array ("show__"));
		$this->register("root_node_name", "report_root");
		$this->register("element_node_name", "elements");
		$this->register("error_occured", FALSE);
		$this->register("error_mesg", "");

		// collect conditions
		$this->conds = & $this->collectConditions();
	}


	/**
	 * this method get result (one row of results) 
	 * and return reported information(needed information for output viewing)
	 * @param mixed $result given information
	 * @return mixed needed information for reporting
	 * */
	function __getFilteredOutputReport(& $result_row) {
		// filtering information
		$report = array (
			$this->getRegisteredValue("root_node_name"
		) => $this->getReportInformationFromRow($result_row), "other" => $this->getUsefulInformation($result_row));
		return $report;
	}

	/**
	 * get viewing information from $log (filtering $log to get all needed information)
	 * @access public
	 * @return mixed reporeted log (any thing that needed for viewing)
	 * */
	function getReportInformationFromRow($row) {
		$report_log = array ();

		foreach ($this->controller->getReportSelectors() as $formual => $field_name) {
			// cut substr that is finish with '|' from $field_name_index
			if (($pos = strpos($field_name, "|")) !== false)
				$field_name = substr($field_name, 0, $pos);

			// get field value from log
			$report_row = $this->getFieldFromRow($row, $field_name);

			// cut first substr that is finish with ','
			if (($pos = strpos($field_name, ",")) !== false)
				$field_name = substr($field_name, 0, $pos);

			// delete prefix from field_name.
			// it contains any thing like this show__info_ 
			$field_name = deletePrefixFromFormula($this->getRegisteredValue("formula_prefixes"), $field_name);

			// collecting
			$report_log[$field_name] = $report_row;
		}

		return $report_log;
	}

	/**
	 * get value of field ($field_name_index) in object ($row_report)
	 * @param mix $row_report
	 * @param string $field_name_index like foo1,foo2,foo3
	 * */
	function getFieldFromRow($row_report, $field_name_index) {
		$ret = array ();
		// separate variables with ','
		// foo1,foo2,foo3 => foo1 foo2 foo3
		$field_name_indexs = explode(",", $field_name_index);

		// get value of each field
		foreach ($field_name_indexs as $field_name)
			// get value of field
			$ret[] = $this->getFieldValue($row_report, $field_name);

		return implode(" ", $ret);

	}

	/**
	 * getting useful information
	 * */
	function getUsefulInformation($report) {
		return array ();
	}

	/**
	 * can I show results
	 * @return boolean TRUE means that show result
	 * */
	function canShowReports() {
		return isInRequest("show_reports");
	}

	/**
	 * example :
	 *   register("inRequestVariable", "search")
	 * 
	 * register variable with it's value
	 * @param string $var
	 * @param mix $value value for $var
	 * */
	function register($var, $value) {
		$this->variables[$var] = $value;
	}

	/**
	 * get registered value of $var
	 * 
	 * TODO if it is possible throw an Exception when there is no variable associate for $var
	 * @param string $var
	 * @return mixed if there is no associated variable for $var return "NotAssignedValue"
	 * */

	function getRegisteredValue($var) {
		if (isset ($this->variables[$var]) and !is_null($this->variables[$var]))
			return $this->variables[$var];

		toLog("Undefine property : " . $var . " you must overide this variable in drived class\n");
		return "NotAssignedValue";
	}

	/**
	 * abstract function collectconditions() 
	 * this methods must be overrided
	 * @return mixed conditions
	 * */
	 function collectConditions()
	 {
	     return array();
	 }

	 /**
	  * extract report rows from array recieved from server
	  * getting reports
	  * @return mixed reports
	  * */
	 function & getReports(& $request_results)
	 {
	     $ret = array ();

	     if ($request_results != null) 
	     	if (isset($request_results["report"])) 
	     		$ret = &$request_results["report"];

	     return $ret;
	 }
	 	 
	 /**
	  * Call the request , and prepare the results. The request is acquired via getRequest method.
	  * returns array of results recieved from server, or null if error happened
	  * */
	 function getResonseResults ()
	 {
	    $report_helper = new ReportHelper();
	    $req = $this->getRequest($this->conds, $report_helper->getFrom(), $report_helper->getTo(), $report_helper->getOrderBy(), $report_helper->getDesc());
		$resp = $req->sendAndRecv();

		$error_occured = false;
		$results = null;

		if ($resp->isSuccessful())
			$results = $resp->getResult();
		else {
			// not successfule reponce so ...
			$resp->setErrorInSmarty($this->controller->smarty);
			$this->register("error_mesg", $resp->getErrorMsg());
			$error_occured = true;
		}
		$this->register("error_occured", $error_occured);

		return $results;        
	 }

	/*
	*Children should overide this and return an instance of Request class.
	*
	*/
    
	function getRequest($conditions, $from, $to, $order_by, $desc)
	{
	    return NULL;
	}

	 /**
	  * abstract function getFieldValue ($row_report, $attribute_name)
	  * get value of field
	  * @param mixed $row_report
	  * @param string $attribute_name name of attribute
	  * */
	  function getFieldValue($row_report, $attribute_name)
	  {
	      return NULL;
	  }
}
?>