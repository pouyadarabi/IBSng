{* 
*}

{include file="admin_header.tpl" title="RealTime WebAnalyzer Log" selected="RealTime Web Analyzer"} 

<script type="text/javascript" src="/IBSng/js/libface.js"></script>
<script type="text/javascript" src="/IBSng/js/web_analyzer.js"></script>

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


{viewTable title="RealTime Web Analyzer Logs For `$username`"}
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

	Seconds <font size=1>(<a href="#" onClick="window.do_refresh=true" id="timer" class=link_in_body>_Loading_</a></span> 

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

{multiTable style="width:200"}
    {multiTableTR}
    		{multiTableTD type="left"}
		    Total Files Fetched:
		{/multiTableTD}
		{multiTableTD type="right"}
		    <span id="total_count">0</span>
		{/multiTableTD}

    		{multiTableTD type="left"}
		    Total Elapsed Time:
		{/multiTableTD}
		{multiTableTD type="right"}
		    <span id="total_elapsed">00:00:00</span>
		{/multiTableTD}
    {multiTableTR}


    		{multiTableTD type="left"}
		    Total Cache Misses:
		{/multiTableTD}
		{multiTableTD type="right"}
		    <span id="total_miss">0</span>
		{/multiTableTD}

    		{multiTableTD type="left"}
		    Total Cache Hits:
		{/multiTableTD}
		{multiTableTD type="right"}
		    <span id="total_hit">0</span>
		{/multiTableTD}

    {multiTableTR}

    		{multiTableTD type="left"}
		    Total Successful Requests:
		{/multiTableTD}
		{multiTableTD type="right"}
		    <span id="total_success">0</span>
		{/multiTableTD}
		
    		{multiTableTD type="left"}
		    Total Failed Requests:
		{/multiTableTD}
		{multiTableTD type="right"}
		    <span id="total_failure">0</span>
		{/multiTableTD}

    {multiTableTR}

    		{multiTableTD type="left"}
		    Total Bytes Transferred:
		{/multiTableTD}
		{multiTableTD type="right"}
		    <span id="total_bytes">0b</span>
		{/multiTableTD}
{/multiTable}

<br />

<span id="logs" name="logs"></span>
<script>

window.default_query='{$default_query}';
window.start_date='{$start_date}';

{if isset($user_id)}
    window.user_id='{$user_id}';
{/if}

{literal}

window.logs=[];
window.last_log_id=-1;
window.totals={"total_count":0,
	       "total_elapsed":0,
	       "total_miss":0,
	       "total_hit":0,
	       "total_success":0,
	       "total_failure":0,
	       "total_bytes":0};

window.logs_table=new LogsTable();
window.new_rows_count=0;

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

		    var totals=http_request.responseXML.getElementsByTagName("TOTALS");
		    var new_rows=http_request.responseXML.getElementsByTagName("REPORT");

		
	            totals=convertElementsToDic(totals[0]);
	    	    appendToLogs(convertXMLToArrayOfDics(new_rows[0].childNodes));
		
		    document.getElementById("parser_time").innerHTML=(new Date().getTime() - parser_start)/1000
		
	    	    var render_start=new Date().getTime();
		
		    displayLogs(totals);
		
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
	var url='/IBSng/admin/report/web_analyzer_logs.php?'+generateURLQuery();
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

{if requestVal("user_id") ne ""}
    {addRelatedLink}
	<a href="/IBSng/admin/user/user_info.php?user_id_multi={$smarty.request.user_id}" class="RightSide_links">
	    User <b>{$smarty.request.user_id|truncate:15}</b> Info
        </a>
    {/addRelatedLink}

{/if}

{addRelatedLink}
    <a href="/IBSng/admin/report/web_analyzer_logs.php" class="RightSide_links">
	Web Analyzer Logs
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
