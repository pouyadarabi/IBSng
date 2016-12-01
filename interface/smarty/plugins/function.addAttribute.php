<?php
function smarty_function_addAttribute($params,&$smarty)
{
/*
    add attribute to one generated table
    parameter name(string,required): name of variable that must be added to generated table
    parameter value(string,required): value of attribute
    parameter default_check(string,required): default value of attribute checkbux 
*/
	global $attributes;

    if (!isset($attributes))
    	return ;

	$module = isset ($params["module"]) ? $params["module"] : "ALL";
	$replace_values = array ("/" => "SLASH");

 
    $attributes[] = array(
						"name" => str_replace( array_keys ($replace_values),
											   array_values ($replace_values),
											   $params["name"]),
    					"value" => $params["value"],
    					"default_checked" => $params["default_checked"],
    					"module" => $module);
}
?>