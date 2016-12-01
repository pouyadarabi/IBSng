<?php
function smarty_function_edit_attr_link($params,&$smarty)
{/* return html code for a link to edit attribute
    parameter template_name (string,required): tell which template_name to pass to edit_attr page
    
    NOTE: target and target_id should be defined in smarty object. 
          These are normally done in group_info or user_info pages automatically.

*/
    $target=$smarty->get_assigned_value("target");
    $target_id=$smarty->get_assigned_value("target_id");
    $template_name=$params["template_name"];
    return <<<END
<a href="/IBSng/admin/user/edit_attr.php?target={$target}&target_id={$target_id}&template_name={$template_name}">
        Edit
</a>
END;
}

?>