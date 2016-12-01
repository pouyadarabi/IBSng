<?php
function smarty_function_reportPages($params,&$smarty)
{/*
    parameter total_results(integer,requrired): total number of results
    parameter file_path(string,optional): set the file path that will be used in page urls
    parameter pages_to_show(integer,optional): set number of pages we want to show the user on page select, default 12
    parameter do_post(boolean, optional): post form "post_form" instead of using get arguments
    parameter ignore_in_url(string, optional): comma separated list of url keys that should be ignored in creating the url
*/
    $file_path=isset($params["file_path"])?$params["file_path"]:$_SERVER["PHP_SELF"];
    $pages_to_show=isset($params["pages_to_show"])?(int)$params["pages_to_show"]:12;
    $total_pages=calcTotalPages($params["total_results"],getRPP());
    $cur_page=min(getCurrentPage(),$total_pages);

    $ignore_url=array("page");
    if(isset($params["ignore_in_url"]))
        $ignore_url=array_merge($ignore_url,explode(",",$params["ignore_in_url"]));
    
    if(isset($params["do_post"]) and $params["do_post"]=="TRUE")
    {
        $link=$file_path;
        $url=convertRequestToUrl($ignore_url,TRUE);
        $do_post = TRUE;
    }
    else
    {
        $url_params=convertRequestToUrl($ignore_url);
        $link="{$file_path}?{$url_params}";
        $do_post = FALSE;
    }

    $pages=createReportPagesArray($link,$cur_page,$total_pages,$pages_to_show, $do_post);
    $ret=createReportPagesTable($pages,$cur_page,$link,$total_pages, $do_post);
    if($do_post)
        $ret = prependPostForm($ret, $url, $link);
    return $ret;
}

function prependPostForm($ret, $inputs, $link)
{
    $script = <<<END
    
    <script language="javascript">

        function setupReportPagesForm()
        {
            var form_text = '<form id="report_pages" name="report_pages" method=POST action="{$link}#show_results">' +
                        '{$inputs}'+
                        '<input type=hidden name=page value=1>'+
                        '</form>';

            var span = document.createElement('span');
            span.innerHTML = form_text;

            document.body.insertBefore(span, null);
        }
    
        function reportPagesSubmitPage(page_no)
        {
            var form = document.report_pages;//document.getElementById('report_pages');
            form.page.value=page_no;
            form.submit();
        }

        addToWindowOnloads( setupReportPagesForm );
        
    </script>
END;
    return $script.$ret;
}

function createReportPagesTable($pages,$cur_page,$link,$total_pages, $do_post)
{
    $page_nos=array_keys($pages);
    $ret="<table><tr>";
    
    $ret.=linkedPageTD(pageImage("first"),createReportPageLink($link,1,$do_post),"First Page");
        
    if(in_array($cur_page-1,$page_nos))
        $ret.=linkedPageTD(pageImage("back"),$pages[$cur_page-1],"Back");
    
    foreach($pages as $page=>$complete_link)
        if($page==$cur_page)
        {
            $ret.=<<<END
            <td>
                <font class="page_num">{$page}</font>
            </td>
END;
        }
        else
            $ret.=linkedPageTD($page,$complete_link,"Page {$page}");
        
    if(in_array($cur_page+1,$page_nos))
        $ret.=linkedPageTD(pageImage("next"),$pages[$cur_page+1],"Next");

    $ret.=linkedPageTD(pageImage("last"),createReportPageLink($link,$total_pages,$do_post),"Last Page");

    $ret.="</tr></table>";
    return $ret;
}

function pageImage($type)
{
    return "<img border=0 src='/IBSng/images/arrow/arrow-{$type}.gif'>";
}

function linkedPageTD($face,$link,$title)
{
    return <<<END
        <td>
            <a class="page_num" href="{$link}" title="{$title}">{$face}</a>
        </td>
END;
}

function getCurrentPage()
{
    $page=(int)requestVal("page",1);
    if($page<=0)
        $page=1;
    return $page;
}

function getRPP()
{
    $rpp=(int)requestVal("rpp",30);
    if($rpp<=0)
        return 30;
    return $rpp;
}

function createReportPagesArray($link,$cur_page,$total_pages,$pages_to_show, $do_post)
{/* return an array of  page_no=>page_link */
    $pages=array();
    $to_show_pages=calcToShowPages($total_pages,$cur_page,$pages_to_show);
    foreach($to_show_pages as $page_no)
        $pages[$page_no]=createReportPageLink($link,$page_no, $do_post);
    return $pages;
}

function createReportPageLink($link,$page_no,$do_post)
{
    if($do_post)
        return "javascript: reportPagesSubmitPage({$page_no});";
    else
        return $link."&page={$page_no}#show_results";
}       

function calcToShowPages($total_pages,$cur_page,$pages_to_show)
{/*
    return a range of page numbers that should be showed
    $pages_to_show should be an even number or else it will be floored to
*/
    $neigh_pages=floor($pages_to_show/2);
    $pre_default_pages=min($cur_page-1,$neigh_pages);
    $post_default_pages=min($total_pages-$cur_page,$neigh_pages);
    $pre_pages=min(max($pre_default_pages,$pre_default_pages+($neigh_pages-($total_pages-$cur_page))),$cur_page-1);
    $post_pages=min(max($post_default_pages,$post_default_pages+($neigh_pages-$cur_page)),$total_pages-$cur_page);
    return range($cur_page-$pre_pages,$cur_page+$post_pages);
}

function calcTotalPages($total_results,$rpp)
{
    if($total_results==0)
        return 1;
    return (int)floor(($total_results-1)/$rpp)+1;
}

?>