<?php

function smarty_block_sortableHeader($params,$content,&$smarty,&$repeat)
{
/*
    Create a Sortable header, used for reports. this is done by making a new request link, with order_by and desc attribute 
    values changed.
    

    parameter name(string,required): name that will be present in order_by if our link clicked
    parameter default(string,optional): if set to TRUE and order_by is not present in request, we assume we're the default
                                        order by
    parameter default_desc(string,optional): defaultly! are we desc?

    parameter order_by_key(string,optional): order_by request key, default is order_by
    parameter desc_key(string,optional): desc request key, default is desc
                                        

*/
    if(!is_null($content))
    {
        $order_by_key=isset($params["order_by_key"])?$params["order_by_key"]:"order_by";
        $desc_key=isset($params["desc_key"])?$params["desc_key"]:"desc";

        $request_url=$_SERVER["PHP_SELF"]."?".convertRequestToUrl(array($order_by_key,$desc_key));
        
        $ret="";
        $desc="&{$desc_key}=1";
        if( isInRequest($order_by_key) and $_REQUEST[$order_by_key]==$params["name"] )
        {
            $ret.=currentSortImage(isInRequest($desc_key));
            if(isInRequest($desc_key))
                $desc="";
        }
        else if( !isInRequest($order_by_key) and isset($params["default"]) and $params["default"]=="TRUE" )
        {
            $ret.=currentSortImage($params["default_desc"]=="TRUE");
            if($params["default_desc"]=="TRUE")
                $desc="";
        }
        
        $ret.=<<<END
    <a class="Header_Top_links" href="{$request_url}&{$order_by_key}={$params["name"]}{$desc}">
        {$content}
    </a>
END;
        return $ret;

    }
}

function currentSortImage($is_desc)
{
    if($is_desc)
        return "<img src='/IBSng/images/arrow/sort_down.gif' border=0>";
    else
        return "<img src='/IBSng/images/arrow/sort_up.gif' border=0>";
}

?>