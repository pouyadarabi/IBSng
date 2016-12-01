<?php
function smarty_function_editCheckBox($params,&$smarty)
{/*
    parameter edit_tpl_name(string,required): edit tpl name that if this check box is checked ,
                                              will be included in list of tpls that will be edited
*/
    $id=getAttrEditCheckboxID();
    return <<<END
    <input type=checkbox name="attr_edit_checkbox_{$id}" value="{$params["edit_tpl_name"]}" class=checkbox style="height: 12px">
END;
}


function getAttrEditCheckboxID()
{/*
    return a unique id for each attr edit check box
*/
    global $attr_edit_checkbox_id;
    if (!isset($attr_edit_checkbox_id))
        $attr_edit_checkbox_id=0;
    else
        $attr_edit_checkbox_id+=1;
    return $attr_edit_checkbox_id;
}
?>