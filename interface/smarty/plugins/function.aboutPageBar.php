<?php
require_once(IBSINC."menu.php");

function smarty_function_aboutPageBar($params,&$smarty)
{/*
    return content of about page bar, based on type parameter
    parameter type(string,required): if set to "title" return title of the about page
                                     if set to "body" returb body of the about page
*/

    global $about_page_body,$about_page_title;
    if($params["type"]=="title")
        return $about_page_title;
    else if ($params["type"]=="body")
        return $about_page_body;
}



?>