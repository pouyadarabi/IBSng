<?php
function smarty_function_redirectToPage($params,&$smarty)
{/*
    create a javascript counter to redirect user to a page upon timer expiry or user click
    
    param url(string,required): url of page that we'll redirected to
    param page_name(string,required): name of the page we'll redirected to
    
    param timer(integer,optional): timer number of seconds

*/
    $timer=isset($params["timer"])?$params["timer"]:5;
    
    return <<<END

<font style="font-size:10pt" face="tahoma" color="#333333">
<B>
    You'll redirect to <a class="link_in_body" href="{$params["url"]}">{$params["page_name"]}</a> 
    Page in <b><font color="#9a1100"><span id="redir_timer">&nbsp;</span></font></b> Seconds
</b>    
</font>

<script language="javascript">
	window.redir_timer={$timer};
    window.url="{$params["url"]}";
    
    addToWindowOnloads( updateTimer );

    function updateTimer()
    {
        window.redir_timer-=1;
        span_obj=document.getElementById("redir_timer");
        span_obj.childNodes[0].nodeValue=window.redir_timer;
        if(window.redir_timer==0)
            window.location=url;
        else
            setTimeout("updateTimer()",1000);
    }
</script>
    
END;
}
?>