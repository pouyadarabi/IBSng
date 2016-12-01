{include file="admin_header.tpl" title="Clean Reports" selected="Clean Reports"} 
{include file="err_head.tpl"} 

{headerMsg var_name="auto_clean_commit_success"}Auto Clean Reports Updated Successfully{/headerMsg}

{headerMsg var_name="manual_delete_success"}Table Manually Cleaned Successfully{/headerMsg}


<form method=POST>
<input type=hidden name="auto_clean_submit" value=1>
{addEditTable double=TRUE title="Auto Clean Reports" action_onclick="confirm(\"Are you sure?\");"}
    {addEditTD type="left1" double=TRUE}
	Auto Clean Connection Log
    {/addEditTD}

    {addEditTD type="right1" double=TRUE}
	<input type=checkbox name="auto_clean_connection_log" {if $connection_log[0] > 0} checked {/if} onClick='connection_log.toggle("connection_log_date")'>
    {/addEditTD}

    {addEditTD type="left2" double=TRUE}
	Auto Clean Connection Logs Before
    {/addEditTD}

    {addEditTD type="right2" double=TRUE}
	<input id="connection_log_date" type=text class=small_text name="connection_log_date" value="{$connection_log[0]}">
	{relative_units id="connection_log_unit" name="connection_log_unit" default="`$connection_log[1]`"}
    {/addEditTD}

    {addEditTD type="left1" double=TRUE}
	Auto Clean Credit Changes
    {/addEditTD}

    {addEditTD type="right1" double=TRUE}
	<input type=checkbox name="auto_clean_credit_change" {if $credit_change[0] > 0} checked {/if} onClick='credit_change.toggle("credit_change_date")'>
    {/addEditTD}

    {addEditTD type="left2" double=TRUE}
	Auto Clean Credit Changes Before
    {/addEditTD}

    {addEditTD type="right2" double=TRUE}
	<input id="credit_change_date" type=text class=small_text name="credit_change_date" value="{$credit_change[0]}">
	{relative_units id="credit_change_unit" name="credit_change_unit" default="`$credit_change[1]`"}
    {/addEditTD}


    {addEditTD type="left1" double=TRUE}
	Auto Clean User Audit Log
    {/addEditTD}

    {addEditTD type="right1" double=TRUE}
	<input type=checkbox name="auto_clean_user_audit_log" {if $user_audit_log[0] > 0} checked {/if} onClick='user_audit_log.toggle("user_audit_log_date")'>
    {/addEditTD}

    {addEditTD type="left2" double=TRUE}
	Auto Clean User Audit Logs Before
    {/addEditTD}

    {addEditTD type="right2" double=TRUE}
	<input id="user_audit_log_date" type=text class=small_text name="user_audit_log_date" value="{$user_audit_log[0]}">
	{relative_units id="user_audit_log_unit" name="user_audit_log_unit" default="`$user_audit_log[1]`"}
    {/addEditTD}

    {addEditTD type="left1" double=TRUE}
	Auto Clean Snap Shots
    {/addEditTD}

    {addEditTD type="right1" double=TRUE}
	<input type=checkbox name="auto_clean_snapshots" {if $snapshots[0] > 0} checked {/if} onClick='snapshots.toggle("snapshots_date")'>
    {/addEditTD}

    {addEditTD type="left2" double=TRUE}
	Auto Clean SnapShots Before
    {/addEditTD}

    {addEditTD type="right2" double=TRUE}
	<input id="snapshots_date" type=text class=small_text name="snapshots_date" value="{$snapshots[0]}">
	{relative_units id="snaphots_unit" name="snapshots_unit" default="`$snapshots[1]`"}
    {/addEditTD}

    {addEditTD type="left1" double=TRUE}
	Auto Clean WebAnalyzer Logs
    {/addEditTD}

    {addEditTD type="right1" double=TRUE}
	<input type=checkbox name="auto_clean_web_analyzer" {if $web_analyzer_log[0] > 0} checked {/if} onClick='web_analyzer.toggle("web_analyzer_date")'>
    {/addEditTD}

    {addEditTD type="left2" double=TRUE}
	Auto Clean Web Analyzer Logs
    {/addEditTD}

    {addEditTD type="right2" double=TRUE}
	<input id="web_analyzer_date" type=text class=small_text name="web_analyzer_date" value="{$web_analyzer_log[0]}">
	{relative_units id="web_analyzer_unit" name="web_analyzer_unit" default="`$web_analyzer_log[1]`"}
    {/addEditTD}


{/addEditTable}

<script language="javascript">
    connection_log=new DomContainer();
    connection_log.disable_unselected=true;
    connection_log.addByID("connection_log_date",["connection_log_unit"]);
{if $connection_log[0] > 0 }
    connection_log.select("connection_log_date");
{else}
    connection_log.select(null);
{/if}

    credit_change=new DomContainer();
    credit_change.disable_unselected=true;
    credit_change.addByID("credit_change_date",["credit_change_unit"]);
{if $credit_change[0] > 0 }
    credit_change.select("credit_change_date");
{else}
    credit_change.select(null);
{/if}

    user_audit_log=new DomContainer();
    user_audit_log.disable_unselected=true;
    user_audit_log.addByID("user_audit_log_date",["user_audit_log_unit"]);
{if $user_audit_log[0] > 0 }
    user_audit_log.select("user_audit_log_date");
{else}
    user_audit_log.select(null);
{/if}

    snapshots=new DomContainer();
    snapshots.disable_unselected=true;
    snapshots.addByID("snapshots_date",["snapshots_unit"]);
{if $snapshots[0] > 0 }
    snapshots.select("snapshots_date");
{else}
    snapshots.select(null);
{/if}

    web_analyzer=new DomContainer();
    web_analyzer.disable_unselected=true;
    web_analyzer.addByID("web_analyzer_date",["web_analyzer_unit"]);
{if $web_analyzer_log[0] > 0 }
    web_analyzer.select("web_analyzer_date");
{else}
    web_analyzer.select(null);
{/if}

</script>

</form>


<form method=POST>
<input type=hidden name="delete_connection_logs" value=1>
{addEditTable double=TRUE title="Manually Clean Connection Logs" action_onclick="confirm(\"Are you sure?\");"}

    {addEditTD type="left"}
	Delete Connection Logs Before
    {/addEditTD}

    {addEditTD type="right" }
	<input type=text class=small_text name="connection_log_date" value="{ifisinrequest name="connection_log_date"}">
	{relative_units name="connection_log_unit" default="Months" default_request="connection_log_unit"}
    {/addEditTD}
{/addEditTable}
</form>

<form method=POST>
<input type=hidden name="delete_credit_changes" value=1>
{addEditTable double=TRUE title="Manually Clean Credit Changes" action_onclick="confirm(\"Are you sure?\");"}

    {addEditTD type="left"}
	Delete Credit Changes Before
    {/addEditTD}

    {addEditTD type="right" }
	<input type=text class=small_text name="credit_change_date" value="{ifisinrequest name="credit_change_date"}">
	{relative_units name="credit_change_unit" default="Months" default_request="credit_change_unit"}
    {/addEditTD}
{/addEditTable}
</form>

<form method=POST>
<input type=hidden name="delete_user_audit_logs" value=1>
{addEditTable double=TRUE title="Manually Clean User Audit Logs" action_onclick="confirm(\"Are you sure?\");"}

    {addEditTD type="left"}
	Delete User Audit Logs Before
    {/addEditTD}

    {addEditTD type="right" }
	<input type=text class=small_text name="user_audit_log_date" value="{ifisinrequest name="user_audit_log_date"}">
	{relative_units name="user_audit_log_unit" default="Months" default_request="user_audit_log_unit"}
    {/addEditTD}
{/addEditTable}
</form>

<form method=POST>
<input type=hidden name="delete_snapshots" value=1>
{addEditTable double=TRUE title="Manually Clean SnapShots" action_onclick="confirm(\"Are you sure?\");"}

    {addEditTD type="left"}
	Delete SnapShots Before
    {/addEditTD}

    {addEditTD type="right" }
	<input type=text class=small_text name="snapshots_date" value="{ifisinrequest name="snapshots_date"}">
	{relative_units name="snapshots_unit" default="Months" default_request="snapshots_unit"}
    {/addEditTD}
{/addEditTable}
</form>

<form method=POST>
<input type=hidden name="delete_web_analyzer" value=1>
{addEditTable double=TRUE title="Manually Web Analyzer Logs" action_onclick="confirm(\"Are you sure?\");"}

    {addEditTD type="left"}
	Delete WebAnalyzer Logs Before
    {/addEditTD}

    {addEditTD type="right" }
	<input type=text class=small_text name="web_analyzer_date" value="{ifisinrequest name="web_analyzer_date"}">
	{relative_units name="web_analyzer_unit" default="Months" default_request="web_analyzer_unit"}
    {/addEditTD}
{/addEditTable}
</form>



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

{addRelatedLink}
    <a href="/IBSng/admin/report/user_audit_logs.php" class="RightSide_links">
	User Audit Logs
    </a>
{/addRelatedLink}


{setAboutPage title="Auto Clean Reports"}
    
{/setAboutPage}


{include file="admin_footer.tpl"}