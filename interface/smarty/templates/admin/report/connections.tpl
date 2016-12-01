{* 
*}

{include file="admin_header.tpl" title="Connection Logs" selected="Connection Logs" page_valign="top"} 
{include file="err_head.tpl"} 
{include file="util/calendar.tpl"}

<form method=POST action="connections.php#show_results" name="connections">
<input type=hidden name=show_reports value=1>
<input type=hidden name=page value=1>
<input type=hidden name=admin_connection_logs value=1>


{* select attribute for showing logs *}

{include file="admin/report/connection_logs/conditions/conditions.tpl" title="Attributes To Show"}

</form>
{if isInRequest("show_reports") }

<a name="show_results"></a>

{math equation="x + y" assign ="size" x = $size y = 1}

{listTable title="Connection Logs" cols_num=$size}
    {listTableHeaderIcon action="details" close_tr=TRUE}
    {listTR type="header"}
	{eval var=$generated_tpl_header}
    {/listTR}

  {assign var="page_total_credit" value=0}
  {assign var="page_total_duration" value=0}

    {foreach from=$reports item=row}
		{capture name="layer"}
			{layerTable}
			    {foreach from=`$row.other.details` item=tuple}
	    	        {layerTR cycle_color=TRUE}
					    {listTD}
					        {$tuple[0]}:
					    {/listTD}
					    {listTD}
						{if $tuple[0] == "bytes_in" or $tuple[0] == "bytes_out"}
						    {$tuple[1]|byte}
						{else}
						    {$tuple[1]} 
						{/if}
						
					    {/listTD}
		
					    {if $tuple[0] == "username"}
					        {assign var="username" value=`$tuple[1]`}
					    {elseif $tuple[0] == "voip_username"}
					        {assign var="username" value=`$tuple[1]`}
					    {elseif $tuple[0] == "persistent_lan"}
					        {assign var="username" value="_PLAN_"}
					    {/if}
					
					{/layerTR}
			    {/foreach}
			{/layerTable}
		{/capture}
	
		{listTR type="body"}
		    {eval var=$generated_tpl_body}
		    {listTD icon=TRUE}
	    		<a onClick="showReportLayer('{$row.other.connection_log_id}',this); return false;" href="#">
			    	{listTableBodyIcon cycle_color=TRUE action="details"}
				</a>
			    {reportDetailLayer name=`$row.other.connection_log_id` title="Report Details"}
					{$smarty.capture.layer}
			    {/reportDetailLayer}
		    {/listTD}
		
		{/listTR}
    {/foreach}

{/listTable}

{listTable title=Totals cols_num=2}
	{listTR type="body" cycle_color=TRUE}
	    {listTD}
			<b>Page</b> Total Credit Used:
    	{/listTD}
	    {listTD}
	        {$page_total_credit|price} {$MONEY_UNIT}
	    {/listTD}

	{/listTR}

	{listTR type="body" cycle_color=TRUE}
	    {listTD}
		<b>Page</b> Total Duration:
    	    {/listTD}
	    {listTD}
	        {$page_total_duration|duration}
	    {/listTD}

	{/listTR}

    {if isInRequest("show_total_credit_used")}
	{listTR type="body" cycle_color=TRUE}
	    {listTD}
		<b>Report</b> Total Credit Used:
    	    {/listTD}
	    {listTD}
	        {$total_credit|price} {$MONEY_UNIT}
	    {/listTD}

	{/listTR}
    {/if}

    {if isInRequest("show_total_duration")}
	{listTR type="body" cycle_color=TRUE}
	    {listTD}
    		<b>Report</b> Total Duration: 
	    {/listTD}
	    {listTD}
	        {$total_duration|duration}
	    {/listTD}
	{/listTR}
    {/if}

    {if isInRequest("show_total_inouts")}
	{listTR type="body" cycle_color=TRUE}
	    {listTD}
    		<b>Report</b> Total In Bytes: 
	    {/listTD}
	    {listTD}
	        {$total_in_bytes|byte}
	    {/listTD}
	{/listTR}

	{listTR type="body" cycle_color=TRUE}
	    {listTD}
    		<b>Report</b> Total Out Bytes: 
	    {/listTD}
	    {listTD}
	        {$total_out_bytes|byte}
	    {/listTD}
	{/listTR}
    {/if}

    {listTR type="body" cycle_color=TRUE}
        {listTD}
		Total Number Of Results:
    	{/listTD}
	{listTD}
	    {$total_rows} 
	{/listTD}

    {/listTR}

{/listTable}

{reportPages total_results=$total_rows}


{/if}


{if requestVal("user_ids") ne ""}
    {addRelatedLink}
	<a href="/IBSng/admin/user/user_info.php?user_id_multi={$smarty.request.user_ids}" class="RightSide_links">
	    User <b>{$smarty.request.user_ids|truncate:15}</b> Info
        </a>
    {/addRelatedLink}

{/if}


{addRelatedLink}
    <a href="{requestToUrl}&Internet_Username=show__details_username&Bytes_IN=show__details_bytes_in|byte&Bytes_OUT=show__details_bytes_out|byte&search=1&Login_Time=show__login_time_formatted&Logout_Time=show__logout_time_formatted&Duration=show__duration_seconds|duration&Successful=show__successful|formatBoolean&Service=show__service_type|formatServiceType&Credit=show__credit_used|price" class="RightSide_links">
	Internet Connections
    </a>
{/addRelatedLink}

{addRelatedLink}
    <a href="{requestToUrl}&VoIP_Username=show__details_voip_username&Called_Number=show__details_called_number&Prefix_Name=show__details_prefix_name&search=1&Login_Time=show__login_time_formatted&Logout_Time=show__logout_time_formatted&Duration=show__duration_seconds|duration&Successful=show__successful|formatBoolean&Service=show__service_type|formatServiceType&Credit=show__credit_used|price" class="RightSide_links">
	VoIP Connections
    </a>
{/addRelatedLink}

{addRelatedLink}
    <a href="/IBSng/admin/report/connection_usages.php" class="RightSide_links">
	Connection Usages
    </a>
{/addRelatedLink}

{addRelatedLink}
    <a href="/IBSng/admin/graph/analysis/connection_analysis.php" class="RightSide_links">
	Connections Analysis
    </a>
{/addRelatedLink}

{addRelatedLink}
    <a href="/IBSng/admin/report/online_users.php" class="RightSide_links">
	Online Users
    </a>
{/addRelatedLink}

{addRelatedLink}
    <a href="/IBSng/admin/report/credit_changes.php" class="RightSide_links">
	Credit Changes
    </a>
{/addRelatedLink}

{addRelatedLink}
    <a href="/IBSng/admin/report/admin_deposit_change_logs/admin_deposit_change_logs.php" class="RightSide_links">
	Deposit Changes
    </a>
{/addRelatedLink}

{addRelatedLink}
    <a href="/IBSng/admin/report/user_audit_logs.php" class="RightSide_links">
	User Audit Logs
    </a>
{/addRelatedLink}

{setAboutPage title="Connection Log"}
{/setAboutPage}


{include file="admin_footer.tpl"}
