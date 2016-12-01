<?php
function smarty_function_helpicon($params,&$smarty)
{/* parameter subject(string,required): subject we want to show help about
    parameter category(string,required): category of help(ex. admin,ras,user...)
    parameter alt(string,optional): alt string for link, that will be shown in link tooltip
    parameter body(string,optional): optional string to be shown instead of help icon
    return string, a linked image that will show the help in a new window
*/
    
    if(isset($params["alt"]))
        $alt=$params["alt"];
    else
        $alt="Help on {$params["subject"]}";
        
    if(isset($params["body"]))
        $body=$params["body"];
    else
        $body="<img src=\"/IBSng/images/icon/help_icon.gif\" border=0>";

    return ""; // empty until all helps are written
        
    return <<<EOF
            <a href="javascript:showHelp('{$params["subject"]}','{$params["category"]}')" title="{$alt}" style="text-decoration: none">{$body}</a>
EOF;
}
?>