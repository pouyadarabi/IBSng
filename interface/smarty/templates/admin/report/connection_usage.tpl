{include file="admin_header.tpl" title="Connection Usages" selected="Connection Usages"} 
{include file="err_head.tpl"} 
{include file="util/calendar.tpl"}

<form method=POST action="connection_usages.php#show_results" name="connection_usage">
<input type=hidden name=show value=1>
<input type=hidden name=show_reports value=1>
<input type=hidden name=page value=1>

<!-- show in all of generated table -->
<input type=hidden name=User_ID value="show__all_user_id|linkUserIDToUserInfo">
<input type=hidden name=Username value="show__all_user_name|formatUserRepr">

<!-- variables for showning in Credit Usages -->
<input type=hidden name=Credit_Usage&#40;UNITS&#41; value="show__credit_usages_credit_usage|price">

<!-- variables for showning in Time Usages -->
<input type=hidden name=Time_Usage value="show__time_usages_time_usage|duration">

<!-- variables for showing in In Out Usages -->
<input type=hidden name=IN_Bytes value="show__inout_usages_in_bytes|byte">
<input type=hidden name=OUT_Bytes value="show__inout_usages_out_bytes|byte">


{addEditTable double=TRUE title="Connection Usages"}

    {addEditTD type="left1" double=TRUE}
		Report Type
    {/addEditTD}

    {addEditTD type="right1" double=TRUE}
		{html_options name="report_type" options=$report_types selected=$report_type_default}
    {/addEditTD}

    {addEditTD type="left2" double=TRUE}
		Results Per Page
    {/addEditTD}

    {addEditTD type="right2" double=TRUE}
		{reportRPP}
    	View : {html_options name="view_options" options=$view_options selected=$view_by_default}
    {/addEditTD}

    {addEditTD type="left1" double=TRUE}
		User IDs
    {/addEditTD}

    {addEditTD type="right1" double=TRUE}
		<input type=text class=text name=user_ids value="{ifisinrequest name="user_ids"}"> {multistr input_name="user_ids" form_name="connections"}
    {/addEditTD}

    {addEditTD type="left2" double=TRUE}
		Owner
    {/addEditTD}

    {addEditTD type="right2" double=TRUE}
		{admin_names_select name="owner" default="All" default_request="owner" add_all=TRUE}
    {/addEditTD}

    {addEditTD type="left1" double=TRUE}
		Login Time From
    {/addEditTD}

    {addEditTD type="right1" double=TRUE}
		{absDateSelect name="login_time_from" default_request="login_time_from" default="1"}
    {/addEditTD}

    {addEditTD type="left2" double=TRUE}
		Login Time To
    {/addEditTD}

    {addEditTD type="right2" double=TRUE}
		{absDateSelect name="login_time_to" default_request="login_time_to"}
    {/addEditTD}

{/addEditTable}
</form>

{if isInRequest("show")}
	<a name="show_results"></a>

	{if $smarty.request.report_type == "inout_usages"}
		{assign var = 'title' value = 'In Out Usages'}
	{elseif $smarty.request.report_type == "credit_usages"}
		{assign var = 'title' value = 'Credit Usages'}
	{elseif $smarty.request.report_type == "time_usages"}
		{assign var = 'title' value = 'Time Usages'}
	{/if}

	{listTable title=$title cols_num=10}
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
    <a href="/IBSng/admin/report/connections.php" class="RightSide_links">
	Connection Logs
    </a>
{/addRelatedLink}

{addRelatedLink}
    <a href="/IBSng/admin/report/connection_analysis.php" class="RightSide_links">
	Connection Analysis
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

{setAboutPage title="Connection Usage"}
    
{/setAboutPage}


{include file="admin_footer.tpl"}