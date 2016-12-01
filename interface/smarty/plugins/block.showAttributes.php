<?php
function smarty_block_showAttributes($params,$content,&$smarty,&$repeat)
{
/*
    create content of attribute table
    parameter title(string,required): name of table title
    parameter form_name(string,required): name of table form
    parameter cols(integer, optional): number of cols of generated table.
*/

	global $attributes;

    if (!isset($attributes) or is_null($content))
    {
    	$attributes = array();
    	return ;
    }

    require_once($smarty->_get_plugin_filepath('function', 'reportToShowCheckBox'));
    require_once($smarty->_get_plugin_filepath('function', 'multiTableTR'));

    $module = isset($params["module"]) ? $params["module"] : "ALL";

    $form_name = $params["form_name"];

    $always_in_form = $params["always_in_form"];
    $container_name = $form_name."_selected";
    $cols = isset($params["cols"]) ? $params["cols"] : 3;

    $ret = "";
    $i = 0;

    foreach ($attributes as $attribute)
    {
    	if (!( $module == $attribute["module"] or
    		   $attribute["module"] == "ALL"   or
    		   $module == "ALL" ))
    		   continue;

    	if ($i % $cols == 0)
    		$ret .= smarty_function_multiTableTR(array(), $smarty);
    		/**
    		 	{reportToShowCheckBox 	name="Internet_Username" output="Internet Username"
							default_checked="TRUE" always_in_form="search"
							value="show__attrs_normal_username" form_name="search_user"
							container_name="attrs_selected"}

    		  
    		 * */
    	$ret .= smarty_function_reportToShowCheckBox(
    				array ( "name" 	 => str_replace (" ", "_", $attribute["name"]),
							"output" => $attribute["name"],
							"default_checked" => $attribute["default_checked"],
							"always_in_form" => $always_in_form,
							"value" => $attribute["value"],
							"form_name" => $form_name,
							"container_name" => $container_name
						)
					, $smarty
				);

  		$i ++;  						
    }

    return $ret;
}
?>