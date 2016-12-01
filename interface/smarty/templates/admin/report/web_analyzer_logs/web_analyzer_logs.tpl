{include file="err_head.tpl"} 
{include file="util/calendar.tpl"}

{include file="admin_header.tpl" title="Web Analyzer Logs" selected="Web Analyzer Logs"} 

<form method=POST action="web_analyzer_logs.php#show_results" name="web_analyzer_logs">

<input type=hidden name=show_reports value=1>
<input type=hidden name=page value=1>
<input type=hidden name=web_analyzer_logs>

{tabTable tabs="Conditions,Attributes" content_height=50 table_width=675 action_icon="search" form_name="web_analyzer_logs"}

    {tabContent add_table_tag=TRUE tab_name="Conditions"}
		{include file = "admin/report/web_analyzer_logs/conditions.tpl"}
    {/tabContent}

    {tabContent add_table_tag=TRUE tab_name="Attributes"}
		{include file	= "admin/report/skel_conditions.tpl"
			 name		= "web_analyzer_logs"
			 title		= "Select Attributes"
			 form_name	= "web_analyzer_logs"
			 inc 		= "admin/report/web_analyzer_logs/skel_condition.tpl"}
    {/tabContent}

{/tabTable}

</form>

{if isInRequest("show_reports")}
	<a name="show_results"></a>

{math assign="number_of_cols" equation="x + 1" x=$number_of_selections}

{listTable title="Web Analyzer Logs" cols_num=$number_of_cols}
    {listTableHeaderIcon action="details" close_tr=TRUE }

	{listTR type="header"}
		{eval var=$generated_tpl_header}
	{/listTR}

	{foreach from=$reports item=row}
		{listTR type="body" cycle_color=TRUE}

			{eval var=$generated_tpl_body}

			{listTD icon=TRUE}

   		    <a onClick="showReportLayer('{$row.other.log_id}',this); return false;" href="#">
				{listTableBodyIcon action="details"}
		    </a>
			{reportDetailLayer name=`$row.other.log_id` title="Report Details"}
			    {layerTable}
	    			{layerTR cycle_color=TRUE}
					    {listTD}
				    	    Source IP:
					    {/listTD}

					    {listTD}
				    	    {$row.other.ip_addr}
					    {/listTD}
					{/layerTR}

			    	{layerTR cycle_color=TRUE}
						    {listTD}
				    		    Elapsed Time:
						    {/listTD}
		
						    {listTD}
								{$row.other.elapsed|duration}
						    {/listTD}
					{/layerTR}

		    		{layerTR cycle_color=TRUE}
					    {listTD}
				    	    Fetch Files Count:
					    {/listTD}

				    {listTD}
						{$row.other._count}
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
		Total Number Of Results:
    	    {/listTD}
	    {listTD}
	        {$total_rows}
	    {/listTD}
	{/listTR}

	{listTR type="body" cycle_color=TRUE}
	    {listTD}
		Total Objects Fetched:
    	    {/listTD}
	    {listTD}
	        {$total_count}
	    {/listTD}
	{/listTR}

	{listTR type="body" cycle_color=TRUE}
	    {listTD}
		Total Elapsed Time:
    	    {/listTD}
	    {listTD}
	        {$total_elapsed|duration}
	    {/listTD}
	{/listTR}

	{listTR type="body" cycle_color=TRUE}
	    {listTD}
		Total Bytes Transferred:
    	    {/listTD}
	    {listTD}
	        {$total_bytes|byte}
	    {/listTD}

	{/listTR}

	{listTR type="body" cycle_color=TRUE}
	    {listTD}
		Total Cache Misses:
    	    {/listTD}
	    {listTD}
	        {$total_miss|price}
	    {/listTD}

	{/listTR}

	{listTR type="body" cycle_color=TRUE}
	    {listTD}
		Total Cache Hits:
    	    {/listTD}
	    {listTD}
	        {$total_hit|price}
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

    {addRelatedLink}
	<a href="/IBSng/admin/report/top_visited.php?user_ids={$smarty.request.user_ids}" class="RightSide_links">
	    User <b>{$smarty.request.user_ids|truncate:15}</b> Top Visited Urls
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

{setAboutPage title=" Web Analyzer Logs"}
    
{/setAboutPage}

{include file="admin_footer.tpl"}
