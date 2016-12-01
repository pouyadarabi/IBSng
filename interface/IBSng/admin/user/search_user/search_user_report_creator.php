<?php


/**
 * 
 * search_user_report_creator.php
 * 
 * */

require_once ("search_user_report_generator_controller.php");
require_once (IBSINC."generator/report_generator/report_creator.php");

class SearchUserReportCreator extends ReportCreator
{
	function SearchUserReportCreator()
	{
		parent :: ReportCreator();
	}

	function init()
	{
		parent :: init();

		$this->register("formula_prefixes", array ("show__attrs_", "show__basic_"));
	}

	/**
	 * collecting conditions
	 */
	function collectConditions()
	{
		return collectConditions();
	}

	function getRequest (& $conds, $from, $to, $order_by, $desc)
	{
	    return new SearchUser ($conds, $from, $to, $order_by, $desc);
	}

	function & getReports(& $respons_results)
	{
		if ($respons_results == NULL)
			$respons_results = array(0, array());

		list ($count, $user_ids) = $respons_results;
		$user_infos = getUsersInfoByUserID($this->controller->smarty, $user_ids);

		$this->controller->smarty->assign("result_count", $count);
		$this->controller->smarty->assign("show_results", TRUE);
		$this->controller->smarty->assign("user_ids", $user_ids);

		// return report sortedly
		// sort user_infos base on user_id
		$user_reports = array ();
		foreach ($user_ids as $user_id)
			$user_reports[] = $user_infos[$user_id];

		return $user_reports;
	}

	/**
	 * get value of $two_dimension_array[$row][$column]
	 * if value doesn't exist return ""
	 * 
	 * @param array[][] $two_dimension_array
	 * @param mixed $row row of array
	 * @param mixed $column column of array
	 * @return mixed value of $two_dimension_array[$row][$column] (return "" as default)
	 * */
	function getValueFromTwoDimArray($two_dimension_array, $row, $column)
	{
		$ret_value = "";
		if (isset ($two_dimension_array[$row][$column]) and !is_null($two_dimension_array[$row][$column]))
			$ret_value = $two_dimension_array[$row][$column];

		return $ret_value;
	}

	/**
	 * get value of $attribute_name in $row_report
	 * @param mixed $row_report
	 * @param string $field_name_index
	 * */
	function getFieldValue($user_attrs, $attribute_name)
	{
		$attr_value = "";

		if (ereg("^show__attrs_.*", $attribute_name))
		{
			$attribute_name = str_replace("show__attrs_", "", $attribute_name);

			if ($attribute_name == "any_username")
			{
				$attr_value = $this->getValueFromTwoDimArray($user_attrs, "attrs", "normal_username");
				if ($attr_value == "")
					$attr_value = $this->getValueFromTwoDimArray($user_attrs, "attrs", "voip_username");
			}
			else
			{
				$attr_value = $this->getValueFromTwoDimArray($user_attrs, "attrs", $attribute_name);

				// value of attribute not found in user list 
				// search in attributes of group
				if ($attr_value == "")
					$attr_value = $this->getGroupAttrValue($user_attrs, $attribute_name);
			}
		}
		else
			if (ereg("^show__basic_.*", $attribute_name))
			{
				$attribute_name = array (str_replace("show__basic_", "", $attribute_name));
				$attr_value = $this->getValueFromTwoDimArray($user_attrs, "basic_info", $attribute_name[0]);
			}
		return $attr_value == "" ? "-" : $attr_value;
	}
	/**
	 * get Group attribute value
	 * 
	 * @param mixed $user_attrs attributes of user
	 * @param string $attr_name name of attribute
	 * @return $mixed value of attrValue ($attr_name)
	 * */
	function getGroupAttrValue($user_attrs, $attribute_name)
	{
		$attr_value = "";
		$group_name = $this->getValueFromTwoDimArray($user_attrs, "basic_info", "group_name");
		List ($success, $group_info) = getGroupInfoWithCache($group_name);
		if ($success)
			$attr_value = $this->getValueFromTwoDimArray($group_info, "attrs", $attribute_name);

		// if generator is web generator then adding "G-"(with red color) prefix to $attr_value
        if ($attr_value != "" and $this->controller->getViewOuputSelectedName() == "WEB")
			$attr_value = "<font size=1 color='#800000'>G-</font>".$attr_value;

		return $attr_value;
	}
}
?>