{* 
*}

{include file="admin_header.tpl" title="Log Console" selected="Log Console"} 

<script type="text/javascript" src="/IBSng/js/libface.js"></script>
<script type="text/javascript" src="/IBSng/js/log_console.js"></script>

<table align=center border=0 style="display: none" id="error_table"> 
<tr> 
<td align=left>
    <img border="0" src="/IBSng/images/msg/before_error_message.gif">
</td>
    <td align=left class="error_messages">
	<span id="error_message">&nbsp;</span>
    </td>
</tr>
</table>


{viewTable title="Log Console"}
    {addEditTD type="left"}
	Refresh Every 
    {/addEditTD}
    {addEditTD type="right"}
	<select name=refresh_interval id=refresh_interval onChange="window.reset_timer=true;">
	    <option>5</option>
	    <option selected>10</option>
	    <option>20</option>
	    <option>30</option>
	</select>

	Seconds <font size=1>
	(<a href="#" onClick="window.do_refresh=true" id="timer" class=link_in_body>_Loading_</a></span> 

	<a href="#" onClick="playPauseOnClick(this); return false;" style="text-decoration:none">
	    <img src="/IBSng/images/icon/pause.gif" border=0 id="refresh_play_pause" style="position: relative; top: 3">
	</a>

	seconds remaining)</font>
    {/addEditTD}

    {addEditTD type="left"}
	Rows Per Page
    {/addEditTD}
    {addEditTD type="right"}
	<select name=row_per_page id=row_per_page>
	    <option>50</option>
	    <option selected>100</option>
	    <option>200</option>
	</select>

    {/addEditTD}

{/viewTable}


<br />

<span id="logs" name="logs"></span>
<script>

{literal}

window.logs=[];
window.last_log_time=0;
window.new_rows_count=0;
window.logs_table=new LogsTable();

requestLogs();

function doRequest()
{
    requestLogs();
}

function getLogsHandler(http_request)
{
    if (http_request.readyState == 4) 
    {    
	if (http_request.status == 200) 
	{
	    document.getElementById("request_time").innerHTML=(new Date().getTime() - window.request_send)/1000
	    
    	    clearError();
	    try
	    {
	        if(!http_request.responseXML.getElementsByTagName("result"))
		    showError("Invalid Response");		
	        else if(http_request.responseXML.getElementsByTagName("result")[0].childNodes[0].nodeValue!="SUCCESS")
		    showError(http_request.responseXML.getElementsByTagName("reason")[0].childNodes[0].nodeValue);
    	        else
		{
		    var parser_start=new Date().getTime();

		    var new_rows=http_request.responseXML.getElementsByTagName("REPORT");
		
	    	    appendToLogs(convertXMLToArrayOfDics(new_rows[0].childNodes));
		
		    document.getElementById("parser_time").innerHTML=(new Date().getTime() - parser_start)/1000
		
	    	    var render_start=new Date().getTime();
		
		    displayLogs();
		
	    	    document.getElementById("render_time").innerHTML=(new Date().getTime() - render_start)/1000
		}
	    }
	    catch(e)
	    {
		showError("Internal Error<br /> " + e.fileName + ":" + e.lineNumber +" Name: "+e.name + " Message:" + e.message);
	    }
	}
	else
	    showError("Internal Error");
	
	updateTimer();

    }

}


function requestLogs()
{
    var http_request;
    changeTimerState("_Loading_");
    
    if (window.XMLHttpRequest)
	http_request = new XMLHttpRequest();
    else if (window.ActiveXObject) 
	http_request = new ActiveXObject("Microsoft.XMLHTTP");

    if(http_request)
    {
	window.request_send=new Date().getTime();
	http_request.onreadystatechange = function() { getLogsHandler(http_request) };
	var url='/IBSng/admin/report/realtime_log_console.php?last_log_time='+window.last_log_time;
	http_request.open('GET', url, true);
	http_request.send(null);	
    }
    else
	showError("Browser doesn't support xmlhttp");
}


</script>

{/literal}

<br />
<p align=right style="font-family: tahoma; font-size:6pt"> Request: <span id=request_time></span> Parser: <span id=parser_time></span> Render: <span id=render_time></span> Seconds</font>

{addRelatedLink}
    <a href="/IBSng/admin/report/connections.php" class="RightSide_links">
	Connection Logs
    </a>
{/addRelatedLink}

{addRelatedLink}
    <a href="/IBSng/admin/report/online_users.php" class="RightSide_links">
	Online Users
    </a>
{/addRelatedLink}

{addRelatedLink}
    <a href="/IBSng/admin/graph/onlines.php" class="RightSide_links">
	Onlines Graph
    </a>
{/addRelatedLink}


{setAboutPage title="RealTime Web Analyzer Logs"}
{/setAboutPage}

{include file="admin_footer.tpl"}
