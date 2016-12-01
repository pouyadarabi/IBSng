{include file="admin_header.tpl" title="Top Visited URLs" selected="Top Visited URLs"}
{include file="err_head.tpl"}
{include file="util/calendar.tpl"}

<form method=POST action="top_visited.php#show_results" name="top_visited">
<input type=hidden name=show value=1>
<input type=hidden name=page value=1>

{addEditTable double=TRUE title="Top Visited Conditions"}
    {addEditTD type="left1" double=TRUE}
	Date From
    {/addEditTD}
    {addEditTD type="right1" double=TRUE}
	{absDateSelect name="date_from" default_request="date_from" default="7"}
    {/addEditTD}

    {addEditTD type="left2" double=TRUE}
	Date To
    {/addEditTD}
    {addEditTD type="right2" double=TRUE}
	{absDateSelect name="date_to" default_request="date_to"}
    {/addEditTD}

    {addEditTD type="left1" double=TRUE}
	User IDs
    {/addEditTD}

    {addEditTD type="right1" double=TRUE}
	<input type=text class=text name=user_ids value="{ifisinrequest name="user_ids"}"> {multistr input_name="user_ids" form_name="web_analyzer_log"}
    {/addEditTD}

    {addEditTD type="left2" double=TRUE}
	Result Per Page
    {/addEditTD}
    {addEditTD type="right2" double=TRUE}
	{reportRPP}
    {/addEditTD}

{/addEditTable}
</form>

{if isInRequest("show")}

<a name="show_results"></a>
{listTable title="Top Visited URLs" cols_num=3}

    {listTR type="header"}
	{listTD}
	    Row
	{/listTD}

	{listTD}
	    URL
	{/listTD}

	{listTD}
	    Count
	{/listTD}
    {/listTR}

  {foreach from=$report item=row}
    {listTR type="body"}
	{listTD}
	    {counter}
	{/listTD}

	{listTD extra="style='text-align:left'"}
	    <a href="{$row.url}" style="color:blue" target="_blank">{$row.url|wordwrap:60:"<br />":true}</a>
	{/listTD}

	{listTD}
	    {$row.count|price}
	{/listTD}
    {/listTR}
  {/foreach}

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
    <a href="/IBSng/admin/report/web_analyzer_logs.php" class="RightSide_links">
	Web Analyzer Logs
    </a>
{/addRelatedLink}


{addRelatedLink}
    <a href="/IBSng/admin/report/realtime_web_analyzer" class="RightSide_links">
	RealTime Web Analyzer
    </a>
{/addRelatedLink}


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

{setAboutPage title="Top Visited URLs"}
    View top visited Urls over selected period
{/setAboutPage}

{include file="admin_footer.tpl"}