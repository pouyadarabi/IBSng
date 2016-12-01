<form method=get action="{requestToUrl ignore="refresh"}" name="refresh_form">
{addEditTable title=$title action_icon="ok" action_onclick="updateRefresh()"}
    {addEditTD type="left"}
	Refresh Every 
    {/addEditTD}
    {addEditTD type="right"}
	{html_options name="refresh" values=$refresh_times output=$refresh_times selected=$refresh_default}
	Seconds <font size=1>
	(<span id="timer">_Loading_</span>
	    <a href="#" onClick="playPauseOnClick(); return false;" style="text-decoration:none">
		<img src="/IBSng/images/icon/pause.gif" border=0 id="refresh_play_pause" style="position: relative; top: 3">
	    </a>
	 seconds remaining)</font>
    {/addEditTD}
{/addEditTable}
</form>

<script language=javascript>
{if isInRequest("refresh")}
    window.refresh={$smarty.request.refresh};
{else}
    window.refresh=20;
{/if}
    window.url_without_refresh='{requestToUrl ignore="refresh"}';
{literal}
	    
    addToWindowOnloads( setupRefreshCounter );

    function setupRefreshCounter()
    {
	window.refresh_timer_status="play";
	updateTimer();
    }
    
    function updateTimer()
    {
	if (window.refresh_timer_status == "play")
	{
	    window.refresh-=1;
	    span_obj=document.getElementById("timer");
    	    span_obj.childNodes[0].nodeValue=refresh;
	    if(window.refresh==0)
		window.location = window.location;
	    else	    
		setTimeout("updateTimer()",1000);
	}
	else
	    setTimeout("updateTimer()",1000);
    }

    function updateRefresh()
    {
	window.location=url_without_refresh+"&refresh="+document.refresh_form.refresh.value;
	return false;
    }

{/literal}

</script>