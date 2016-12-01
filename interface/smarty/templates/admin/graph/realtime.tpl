{include file="admin_header.tpl" title="Real Time Graphs" selected="Real Time Graphs"} 
{include file="err_head.tpl"} 


<form name="scale_form">
{addEditTable title="Real Time Graph" action_icon="ok" action_onclick="updateRefresh()" nofoot=TRUE}
    {addEditTD type="left"}
	Refresh Every 
    {/addEditTD}
    {addEditTD type="right"}
	{html_options name="refresh" values=$refresh_times output=$refresh_times selected=$refresh_default id="refresh"}
	Seconds <font size=1>(<span id="timer">&nbsp;</span> seconds remaining)</font>
    {/addEditTD}

    {addEditTD type="left"}
	Scale
    {/addEditTD}
    {addEditTD type="right"}
	{scaleSelect name="scale" default="minute" default_request="scale"}
    {/addEditTD}
{/addEditTable}
</form>

<img src="#" id="graph" name="graph">

<script>
var url = "/IBSng/admin/graph/realtime/{$url}";
var refresh = {$refresh_default};
{literal}

if(url.indexOf("?") == -1)
    url+="?";
else
    url+="&";

document.scale_form.scale.onchange=new Function("reloadGraph(false)");

reloadGraph(true);

function reloadGraph(set_timer)
{
    var img=new Image();
    img.src = url + "scale="+document.scale_form.scale.value+"&"+new Date().getTime();
    document.graph.src = img.src;
    if (set_timer)
	setTimer();
}    

function updateTimer()
{
    refresh-=1;
    span_obj=document.getElementById("timer");
    span_obj.childNodes[0].nodeValue=refresh;
    if(refresh==0)
        reloadGraph(true);
    else	    
        setTimeout("updateTimer()",1000);
}


function setTimer()
{
    span_obj=document.getElementById("timer");
    if(!document.graph.complete)
    {
	setTimeout("setTimer()",500);
	span_obj.childNodes[0].nodeValue="_Loading_";
	return;
    }

    refresh = Number(document.getElementById("refresh").value) + 1;
    updateTimer();
}


</script>
{/literal}

{addRelatedLink}
    <a href="/IBSng/admin/report/online_users.php" class="RightSide_links">
	Online Users
    </a>
{/addRelatedLink}

{addRelatedLink}
    <a href="/IBSng/admin/graph/realtime/realtime.php?img_url=onlines.php" class="RightSide_links">
	All RealTime Graph
    </a>
{/addRelatedLink}

{addRelatedLink}
    <a href="/IBSng/admin/graph/realtime/realtime.php?img_url=onlines.php?internet=1" class="RightSide_links">
	Internet RealTime Graph
    </a>
{/addRelatedLink}

{addRelatedLink}
    <a href="/IBSng/admin/graph/realtime/realtime.php?img_url=onlines.php?voip=1" class="RightSide_links">
	VoIP RealTime Graph
    </a>
{/addRelatedLink}

{addRelatedLink}
    <a href="/IBSng/admin/graph/realtime/realtime.php?img_url=bw.php" class="RightSide_links">
	BW RealTime Graph
    </a>
{/addRelatedLink}

{addRelatedLink}
    <a href="/IBSng/admin/graph/onlines.php" class="RightSide_links">
	Onlines Graph
    </a>
{/addRelatedLink}

{addRelatedLink}
    <a href="/IBSng/admin/graph/analysis/connection_analysis.php" class="RightSide_links">
	Connection Analysis
    </a>
{/addRelatedLink}

{setAboutPage title="Real Time Graphs"}
    
{/setAboutPage}


{include file="admin_footer.tpl"}