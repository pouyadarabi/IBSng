<?php

function smarty_block_setAboutPage($params,$content,&$smarty,&$repeat)
{
/*
    set page about side bar text. return nothing so nothing will be printed
    parameter title(string,required): title of the about page
*/
    if(!is_null($content))
    {
        global $about_page_body,$about_page_title;
        $about_page_body=$content;
        $about_page_title=$params["title"];
    }
    
}
?>