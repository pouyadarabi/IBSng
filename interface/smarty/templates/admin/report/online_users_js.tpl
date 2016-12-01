{* Online Users By Type : Show a list of online users, seperated by their type(eg. Internet or VoIP)
*}

{include file="admin_header.tpl" title="Online Users" selected="Online Users" page_valign=top} 

<script language="javascript" src="/IBSng/js/check_box_container.js"></script>
<script type="text/javascript" src="/IBSng/js/onlines.js"></script>
<script type="text/javascript" src="/IBSng/js/libface.js"></script>

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

<div align=center><a href="online_users.php" class="page_menu" style="font-weight: bold; font-size: 11; font-family: tahoma;">Switch to Normal Mode</a></div>
<br>

<!-- kill user frame -->
<iframe name=msg id=msg border=0 FRAMEBORDER=0 SCROLLING=NO height=50 valign=top src="/IBSng/util/empty.php"></iframe>

{tabTable tabs="Ras Filter,Internet,VoIP,Username Filter" content_height=50 action_icon="" form_name=""}
    {tabContent tab_name="Ras Filter" add_table_tag=TRUE add_table_id="ras_filter_select"}
	{include file="admin/report/online_users/ras_filter.tpl"} 
    {/tabContent}

    {tabContent tab_name="Username Filter" add_table_tag=TRUE add_table_id="username_filter_select"}
	{include file="admin/report/online_users/username_filter.tpl"} 
    {/tabContent}

    {tabContent tab_name="Internet" add_table_tag=TRUE add_table_id="internet_select"}
	{include file="admin/report/online_users/internet_attrs.tpl"} 
    {/tabContent}

    {tabContent tab_name="VoIP" add_table_tag=TRUE add_table_id="voip_select"}
	{include file="admin/report/online_users/voip_attrs.tpl"} 
    {/tabContent}

    <tr><td colspan=20 align=center>	

    <table width=100% border="0" cellspacing="0" bordercolor="#000000" cellpadding="0">    

	<tr class="List_Foot_Line_red">
		<td colspan=30></td>
	</tr>

	{include file="admin/report/online_users/tab_foot.tpl"} 

    </table>

    </td></tr>


{/tabTable}

<span id="all_internet">

<form id="internet_onlines" name="internet_onlines"></form>

</span>

<br />

<span id="all_voip">

<form id="voip_onlines" name="voip_onlines"></form>

</span>

<br />

<input align=center type=image src="/IBSng/images/icon/kick.gif" name=kick value="kick" onClick="actionIconClicked('kick')">
<input align=center type=image src="/IBSng/images/icon/clear.gif" name=clear value="clear" onClick="actionIconClicked('clear')">
<input align=center type=image src="/IBSng/images/icon/message.gif" name=clear value="message" onClick="actionIconClicked('message')">

{literal}
<script>
setCheckBoxesOnclick("internet_select",displayOnlines);
setCheckBoxesOnclick("voip_select",displayOnlines);

window.internet_onlines=[];
window.voip_onlines=[];

window.refresh_timer_status="play";
requestOnlines();


function doRequest()
{
    requestOnlines();
}

function getOnlinesHandler(http_request)
{
    if (http_request.readyState == 4) 
    {    
	if (http_request.status == 200) 
	{
	    document.getElementById("request_time").innerHTML=(new Date().getTime() - window.request_send)/1000
	    
    	    clearError();

	    if(http_request.responseXML.getElementsByTagName("result")[0].childNodes[0].nodeValue!="SUCCESS")
		showError(http_request.responseXML.getElementsByTagName("reason")[0].childNodes[0].nodeValue);
	    else
	    {
		var parser_start=new Date().getTime();

	        var xml_internet_onlines=http_request.responseXML.getElementsByTagName("internet_onlines");
		var xml_voip_onlines=http_request.responseXML.getElementsByTagName("voip_onlines");
	        window.internet_onlines=convertOnlinesToArray(xml_internet_onlines[0].childNodes);
		window.voip_onlines=convertOnlinesToArray(xml_voip_onlines[0].childNodes);

		document.getElementById("parser_time").innerHTML=(new Date().getTime() - parser_start)/1000
		
		var render_start=new Date().getTime();
		
		displayOnlines();
		
		document.getElementById("render_time").innerHTML=(new Date().getTime() - render_start)/1000
	    }
	    
	}
	else
	    showError("Internal Error");
	
	updateTimer();

    }

}


function requestOnlines()
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
	http_request.onreadystatechange = function() { getOnlinesHandler(http_request) };
	var url='/IBSng/admin/report/online_users_js.php?internet_order_by='+getCurSort("internet")+
							'&internet_desc='+getCurDesc("internet")+
							'&voip_order_by='+getCurSort("voip")+
							"&voip_desc="+getCurDesc("voip")+
							"&"+getFiltersURL();
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

{include file="admin/report/online_users_footer.tpl"}
