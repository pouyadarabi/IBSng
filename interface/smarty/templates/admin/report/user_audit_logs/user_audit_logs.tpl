{include file="admin_header.tpl" title="User Audit Logs" selected="User Audit Logs"} 
{include file="err_head.tpl"} 
{include file="util/calendar.tpl"}

<form method=POST action="user_audit_logs.php#show_results" name="user_audit_log">
<input type=hidden name=show_reports value=1>
<input type=hidden name=page value=1>
<input type=hidden name=user_audit_log_in_form value=1>

{tabTable tabs="Conditions,Attributes" content_height=50 table_width=675 action_icon="ok" form_name="user_audit_log"}
	{tabContent add_table_tag=TRUE tab_name="Conditions"}
		{include file="admin/report/user_audit_logs/conditions.tpl"}
	{/tabContent}

	{tabContent add_table_tag=TRUE tab_name="Attributes"}
		{addAttributeSkel form_name="user_audit_log" title="Select Attributes"}
			{include file="admin/report/user_audit_logs/user_audit_logs_attributes.tpl"}
    	{/addAttributeSkel}
	{/tabContent}
{/tabTable}
</form>

{if isInRequest("show_reports")}

<a name="show_results"></a>

{math equation = "x + 1" x = $number_of_selections assign = "generated_table_size"}

{listTable title="User Audit Logs" cols_num=$generated_table_size}
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
    <a href="/IBSng/admin/report/online_users.php" class="RightSide_links">
	Online Users
    </a>
{/addRelatedLink}

{addRelatedLink}
    <a href="/IBSng/admin/report/connections.php" class="RightSide_links">
	Connection Logs
    </a>
{/addRelatedLink}

{addRelatedLink}
    <a href="/IBSng/admin/report/credit_changes.php" class="RightSide_links">
	Credit Changes
    </a>
{/addRelatedLink}

{setAboutPage title="User Audit Logs"}
    
{/setAboutPage}


{include file="admin_footer.tpl"}