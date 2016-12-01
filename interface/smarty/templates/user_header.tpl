{include file="header.tpl"}
<body topmargin="0" leftmargin="0" rightmargin="0" bottommargin="0" marginwidth="0" marginheight="0">

<!-- Header -->
<table border="0" width="100%" cellspacing="0" cellpadding="0">
	<tr>
		<td rowspan="3" width="107"><img border="0" src="/IBSng/images/logo/logoibsng.gif"></td>

		<td rowspan="3" width="112" valign="top" class="Header_Color"><img border="0" src="/IBSng/images/logo/edition.gif">
		<br />&nbsp;Version {$IBSNG_VERSION}
		</td>
		
		<td rowspan="3" width="100%" class="Header_Color"></td>
		<!-- Top right Link -->
		<td class="Header_Color" width="204"></td>
		<td width="180" height="19">
		<table height="19" border="0" width="100%" cellspacing="0" cellpadding="0">
			<tr class="Header_Top_link">
				<td width="7"><img border="0" src="/IBSng/images/header/top_right_links_begin.gif"></td>
				<td class="Page_Top_Link">User</td>
				<td class="Page_Top_Link">&nbsp;</td>
				<td class="Page_Top_Link">Username:<font color="#FF9C00">{$auth_name|capitalize}</font></td>
				<td class="Page_Top_Link"><img border="0" src="/IBSng/images/menu/line_between_topmenu.gif"></td>
				<td class="Page_Top_Link"><a class="Header_Top_links" href="/IBSng/user/?logout=1">Logout</a></td>
			</tr>
		</table>
		</td>
		<!-- End Top right Link-->
	</tr>
	<tr>
		<td colspan="3" width="384" height="18" class="Header_Color"></td>
	</tr>
	<tr>
		<td colspan="3" width="384" height="24">
		<!-- Links Button -->
		<table border="0" width="384" cellspacing="0" height="24" cellpadding="0">
			<tr>
			    <td>{userMenuIcon name="home"}</td>
			    <td>{userMenuIcon name="change_pass"}</td>

			    <td>
			{if $auth_type == "NORMAL_USER" }			    
			    {userMenuIcon name="connection_log" url_params="show_reports=1&rpp=20&page=1&order_by=login_time&desc=1&show_total_credit_used=1&show_total_duration=1&set_defaults=1&Username=show__details_username&Login_Time=show__login_time_formatted&Logout_Time=show__logout_time_formatted&Duration=show__duration_seconds|duration&Successful=show__successful|formatBoolean&Credit_Used=show__credit_used|price&Successful=show__successful|formatBoolean&Service=show__service_type|formatServiceType&Caller_ID=show__details_caller_id&Bytes_OUT=show__details_bytes_out|byte&Bytes_IN=show__details_bytes_out|byte#show_results"}
			{else}
				{userMenuIcon name="connection_log" url_params="show_reports=1&rpp=20&page=1&order_by=login_time&desc=1&show_total_credit_used=1&show_total_duration=1&set_defaults=1&Username=show__details_username&Login_Time=show__login_time_formatted&Logout_Time=show__logout_time_formatted&Duration=show__duration_seconds|duration&Successful=show__successful|formatBoolean&Credit_Used=show__credit_used|price&Successful=show__successful|formatBoolean&Service=show__service_type|formatServiceType&Caller_ID=show__details_caller_id&Called_Number=show__details_called_number&Prefix_Name=show__details_prefix_name#show_results"}
			{/if}
			    </td>
    	    		    <td>{userMenuIcon name="credit_log" url_params="show=1&rpp=20&page=1&show_total_per_user_credit=1#show_results"}</td>
    	    		    <td>{userMenuIcon name="view_messages" url_params="show=1&rpp=20&page=1&order_by=message_id&desc=1#show_results"}</td>
			    {ifUserHasAttr user_id=-1 attr_name="save_bw_usage"}
				<td>{userMenuIcon name="bw_graph"}</td>
			    {/ifUserHasAttr}

			</tr>
		</table>
		<!-- End Links Button -->
		</td>
	</tr>
	<tr>
		<td align="right" colspan="5" class="Header_Submenu">
			<table align="right" border="0" cellspacing="0" cellpadding="0" class="Header_Submenu">
				<tr>
				<td width=10></td>
				</tr>
			</table>
		</td>
	</tr>
<tr><td colspan=5 valign=top height=25>
<!-- End Header -->
<!-- Page title & Info -->
<table border="0" width="100%" cellspacing="0" cellpadding="0">
	<tr>
		<td width="200" rowspan="2">
		<table border="0" width="100%" cellspacing="0" cellpadding="0">
			<tr>
				<td width="22"><img border="0" src="/IBSng/images/arrow/arrow_before_page_title.gif"></td>
				<td class="Page_Title">{$title}</td>
				<td width="27" ><img border="0" src="/IBSng/images/arrow/arrow_after_page_title.gif"></td>
			</tr>
		</table>
		</td>
		<td class="Page_Header_Line"></td>
	</tr>
	<tr>
		<td class="Page_Header_Info">{"now"|date_format:"%A, %B %e, %Y"}&nbsp;&nbsp;</td>
	</tr>
	<tr>
		<td colspan="2" class="Page_Top_Space"></td>
	</tr>
</table>
<!-- End Page title & Info -->
</td></tr>
</table>
<!-- Main Table -->
<table border="0" cellspacing="0" cellpadding="0" class="Main_Page">
	<tr>
		<td align="center">		

