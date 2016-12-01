{include file="admin_header.tpl" title="Deposit Change Logs" selected="User Audit Logs"} 
{include file="err_head.tpl"} 
{include file="util/calendar.tpl"}

<form method=POST action="admin_deposit_change_logs.php#show_results" name="admin_deposit_change_logs">
<input type=hidden name=show_reports value=1>
<input type=hidden name=page value=1>
<input type=hidden name=deposit_change_logs>

{tabTable tabs="Conditions,Attributes" content_height=50 table_width=675 action_icon="search" form_name="admin_deposit_change_logs"}

    {tabContent add_table_tag=TRUE tab_name="Conditions"}
		{include file = "admin/report/admin_deposit_change_logs/conditions.tpl"}
    {/tabContent}

    {tabContent add_table_tag=TRUE tab_name="Attributes"}
		{include file	= "admin/report/skel_conditions.tpl"
			 name		= "change_deposit_logs"
			 title		= "Select Attributes"
			 form_name	= "admin_deposit_change_logs"
			 inc 		= "admin/report/admin_deposit_change_logs/selected_attributes.tpl"}
    {/tabContent}


{/tabTable}

</form>

{if isInRequest("show_reports")}
	<a name="show_results"></a>

{listTable title="Connection Logs" cols_num=10}
	{assign var="page_total_deposit_change" value=0}
	{listTR type="header"}
		{eval var=$generated_tpl_header}
	{/listTR}

	{foreach from=$reports item=row}
		{listTR type="body" cycle_color=TRUE}
			{eval var=$generated_tpl_body}
		{/listTR}
	{/foreach} 

{/listTable}


{listTable title=Totals cols_num=2}

	{listTR type="body" cycle_color=TRUE}
	    {listTD}
   			<b>Page</b> Total Change: 
	    {/listTD}
	    {listTD}
    	    {$page_total_deposit_change|price} {$MONEY_UNIT}
	    {/listTD}
	{/listTR}

    {if isInRequest("show_total_deposit_change")}
		{listTR type="body" cycle_color=TRUE}
		    {listTD}
    			<b>Report</b> Total Change: 
		    {/listTD}
		    {listTD}
	    	    {$total_deposit_change|price} {$MONEY_UNIT}
		    {/listTD}
		{/listTR}
    {/if}

	{listTR type="body" cycle_color=TRUE}
	    {listTD}
		Total Number Of Results:
    	    {/listTD}
	    {listTD}
			{$total_of_rows}
	    {/listTD}
	{/listTR}

{/listTable}

{reportPages total_results=$total_of_rows}

{/if}
{addRelatedLink}
    <a href="/IBSng/admin/report/credit_changes.php" class="RightSide_links">
	Credit Changes
    </a>
{/addRelatedLink}

{addRelatedLink}
    <a href="/IBSng/admin/report/connections.php" class="RightSide_links">
	Connection Logs
    </a>
{/addRelatedLink}


{setAboutPage title="Admin Deposit Change Logs"}
    
{/setAboutPage}


{include file="admin_footer.tpl"}
