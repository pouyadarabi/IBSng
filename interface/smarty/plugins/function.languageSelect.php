<?php
function smarty_function_languageSelect($params,&$smarty)
{/*return html select of Available languages
*/
    require_once $smarty->_get_plugin_filepath('function', 'html_options');
    global $valid_languages;


    $outputs = array();
    $values = array();

    foreach($valid_languages as $code=>$output)
    {
        $outputs[] = $output;
        $values[] = $code;
    }


    $select_arr=array("output"=>$outputs,"values"=>$values,"name"=>"lang","selected"=>getLang());
    return smarty_function_html_options($select_arr, $smarty);
}
?>