<?php
/*
    Create skelton of a report condition table

    param title(string, required) title of generated table
    param form_name(string, required) form_name
*/

function smarty_block_addAttributeSkel($params,$content,&$smarty,&$repeat)
{
    if (is_null($content))
    	return ;

	$title = $params ["title"];
	$form_name = $params["form_name"];

	$inc_params = array(
		"smarty_include_tpl_file" => "admin/report/skel_conditions.tpl",
     		"smarty_include_vars" =>  array( 
     		"name" => $form_name,
     		"form_name" =>  $form_name,
     		"title" =>  $title,
     		"file_value" =>  $content)
     	);
   		  
	$smarty->_smarty_include($inc_params);
}
?>