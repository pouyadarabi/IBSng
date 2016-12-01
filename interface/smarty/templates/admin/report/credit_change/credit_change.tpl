{include file="admin_header.tpl" title="Credit Change Report" selected="Credit Change"} 
{include file="err_head.tpl"} 
{include file="util/calendar.tpl"}

<form method=POST action="credit_changes.php#show_results" name="credit_change">
<input type=hidden name=show_reports value=1>
<input type=hidden name=credit_change value=1>
<input type=hidden name=page value=1>

{tabTable tabs="Conditions,Attributes" content_height=50 table_width=675 action_icon="ok" form_name="credit_change"}
	{tabContent add_table_tag=TRUE tab_name="Conditions"}
		{include file="admin/report/credit_change/conditions.tpl"}
	{/tabContent}

	{tabContent add_table_tag=TRUE tab_name="Attributes"}
		{addAttributeSkel form_name="credit_change" title="Select Attributes"}
			{include file="admin/report/credit_change/credit_change_attributes.tpl"}
    	{/addAttributeSkel}
	{/tabContent}
{/tabTable}

</form>

{if isInRequest("show_reports")}

<a name="show_results"></a>
{math equation = "x + 1" x = $number_of_selections assign = "generated_table_size"}

{listTable title="Credit Changes" cols_num=$generated_table_size}
    {listTableHeaderIcon action="details" close_tr=TRUE}
    {listTR type="header"}
		{eval var=$generated_tpl_header}
    {/listTR}

  {assign var="page_total_per_user_credit" value=0}
  {assign var="page_total_admin_credit" value=0}

  {foreach from=$reports item=row}
    {listTR type="body"}
    		{eval var=$generated_tpl_body}
			{listTD icon=TRUE }
	    	    <a onClick="showReportLayer('{$row.other.credit_change_id}',this); return false;" href="#">
					{listTableBodyIcon cycle_color=TRUE action="details"}
			    </a>
				{reportDetailLayer name=`$row.other.credit_change_id` title="Report Details"}
				    {layerTable}
			    		{layerTR cycle_color=TRUE}
							{listTD}
							    <font color="#990000">Comment:</font>{$row.other.comment}
							{/listTD}
						{/layerTR}

						{layerTR cycle_color=TRUE}
							{listTD}
							    <font color="#990000">Admin IP Address:</font> {$row.other.remote_addr}
							{/listTD}
						{/layerTR}

						{layerTR cycle_color=TRUE}
							{listTD}
								<font color="#990000">User IDs:</font>{arrayJoin array=`$row.other.user_ids` glue=", "}
							{/listTD}
						{/layerTR}
				    {/layerTable}
				{/reportDetailLayer}
			{/listTD}
    {/listTR}
  {/foreach}
    
{/listTable}    

{listTable title=Totals cols_num=2}
	{listTR type="body" cycle_color=TRUE}
	    {listTD}
		<b>Page</b> Total Per User Credit:
    	    {/listTD}
	    {listTD}
	        {$page_total_per_user_credit|price} {$MONEY_UNIT}
	    {/listTD}

	{/listTR}

	{listTR type="body" cycle_color=TRUE}
	    {listTD}
		<b>Page</b> Total Admin Consumed Credit:
    	    {/listTD}
	    {listTD}
	        {$page_total_admin_credit|price} {$MONEY_UNIT}
	    {/listTD}

	{/listTR}


    {if isInRequest("show_total_per_user_credit")}
	{listTR type="body" cycle_color=TRUE}
	    {listTD}
		<b>Report</b> Total Per User Credit:
    	    {/listTD}
	    {listTD}
	        {$total_per_user_credit|price} {$MONEY_UNIT}
	    {/listTD}

	{/listTR}
    {/if}

    {if isInRequest("show_total_admin_credit")}
	{listTR type="body" cycle_color=TRUE}
	    {listTD}
    		<b>Report</b> Total Admin Credit: 
	    {/listTD}
	    {listTD}
	        {$total_admin_credit|price } {$MONEY_UNIT}
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
    <a href="/IBSng/admin/report/user_audit_logs.php" class="RightSide_links">
	User Audit Logs
    </a>
{/addRelatedLink}

{addRelatedLink}
    <a href="/IBSng/admin/report/admin_deposit_change_logs/admin_deposit_change_logs.php" class="RightSide_links">
	Deposit Changes
    </a>
{/addRelatedLink}


{setAboutPage title="Credit Change"}
        
{/setAboutPage}


{include file="admin_footer.tpl"}
