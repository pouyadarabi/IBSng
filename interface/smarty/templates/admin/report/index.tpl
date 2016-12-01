{include file="admin_header.tpl" title="Reports" selected="Online Users""}

<table border=0 width="100%" height="100%" cellspacing=0 cellpadding=0>
    <tr>
	<td colspan=2 height=30>
	</td>
    </tr>	
    <tr>
	<td valign="center" align="center"> 
		{viewTable title="Reports" table_width="200" nofoot="TRUE" color="red" arrow_color="white"}
		    {menuTR}
			<a href="/IBSng/admin/report/online_users.php" class="page_menu">Online Users</a>
		    {/menuTR}

		    {menuTR}
			<a href="/IBSng/admin/report/connections.php" class="page_menu">Connection Logs</a>
		    {/menuTR}

		    {menuTR}
			<a href="/IBSng/admin/report/connection_usages.php" class="page_menu">Connection Usages</a>
		    {/menuTR}

		    {menuTR}
			<a href="/IBSng/admin/report/credit_changes.php" class="page_menu">Credit Changes</a>
		    {/menuTR}

		    {menuTR}
			<a href="/IBSng/admin/report/admin_deposit_change_logs/admin_deposit_change_logs.php" class="page_menu">Deposit Changes</a>
		    {/menuTR}

		    {menuTR}
			<a href="/IBSng/admin/report/user_audit_logs.php" class="page_menu">User Audit Logs</a>
		    {/menuTR}

		    {menuTR}
			<a href="/IBSng/admin/report/realtime_log_console.php" class="page_menu">RealTime Log Console</a>
		    {/menuTR}
		    
		{/viewTable}
	</td>
	<td valign="center" align="center"> 
		{viewTable title="Web Analyzer" table_width="200" nofoot="TRUE" color="red" arrow_color="white"}
		    {menuTR}
			<a href="/IBSng/admin/report/web_analyzer_logs.php" class="page_menu">Web Analyzer Logs</a>
		    {/menuTR}

		    {menuTR}
			<a href="/IBSng/admin/report/realtime_web_analyzer.php" class="page_menu">RealTime Web Analyzer</a>
		    {/menuTR}

		    {menuTR}
			<a href="/IBSng/admin/report/top_visited.php" class="page_menu">Top Visited</a>
		    {/menuTR}

		{/viewTable}

	</td>
    </tr>
</table>

{addRelatedLink}
    <a href="/IBSng/admin/report/online_users.php" class="RightSide_links">
	Online Users
    </a>
{/addRelatedLink}

{addRelatedLink}
    <a href="/IBSng/admin/report/connections.php" class="RightSide_links">
	Connetion Logs
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

{setAboutPage title="Report"}

{/setAboutPage}

{include file="admin_footer.tpl"}

