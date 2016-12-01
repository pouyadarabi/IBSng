{include file="admin_header.tpl" title="Home" selected=""}

<table border=0 width="100%" height="100%" cellspacing=0 cellpadding=0>
    <tr>
	<td colspan=2 height=30>
	</td>
    </tr>	
    <tr>
	<td valign="top" align="center"> 
		{viewTable title="User" table_width="200" nofoot="TRUE" color="red" arrow_color="white"}
		    {menuTR}
			<a href="/IBSng/admin/user/user_info.php" class="page_menu">User Informaion</a>
		    {/menuTR}
		    {menuTR}
			<a href="/IBSng/admin/user/search_user.php" class="page_menu">Search User</a>
		    {/menuTR}
		    {menuTR}
			<a href="/IBSng/admin/user/add_new_users.php" class="page_menu">Add New User</a>
		    {/menuTR}

		    {menuTR}
			<a href="/IBSng/admin/user/search_add_user_saves.php" class="page_menu">Add User Saves</a>
		    {/menuTR}
		{/viewTable}
	</td>
	<td valign="top" align="center">
		{viewTable title="Setting" table_width="200" nofoot="TRUE" color="red" arrow_color="white"}
		    {menuTR}
			<a href="/IBSng/admin/charge/charge_list.php" class="page_menu">Charge</a>
		    {/menuTR}
		    {menuTR}
			<a href="/IBSng/admin/ras/ras_list.php" class="page_menu">RAS</a>
		    {/menuTR}
		    {menuTR}
			<a href="/IBSng/admin/ippool/ippool_list.php" class="page_menu">IPpool</a>
		    {/menuTR}
		    {menuTR}
			<a href="/IBSng/admin/bw/interface_list.php" class="page_menu">Bandwidth Managment</a>
		    {/menuTR}
		    {menuTR}
			<a href="/IBSng/admin/charge/voip_tariff/tariff_list.php" class="page_menu">VoIP Tariff</a>
		    {/menuTR}

		    {menuTR}
			<a href="/IBSng/admin/report/clean_reports.php" class="page_menu">Clean Reports</a>
		    {/menuTR}

		{/viewTable}

	</td>
    </tr>
    <tr>
	<td valign="top" align="center">
		{viewTable title="Group" table_width="200" nofoot="TRUE" color="red" arrow_color="white"}
		    {menuTR}
			<a href="/IBSng/admin/group/group_list.php" class="page_menu">Group List</a>
		    {/menuTR}
		    {menuTR}
			<a href="/IBSng/admin/group/add_new_group.php" class="page_menu">Add New Group</a>
		    {/menuTR}
		{/viewTable}

	</td>
	<td valign="top" align="center">
		{viewTable title="Admin" table_width="200" nofoot="TRUE" color="red" arrow_color="white"}
		    {menuTR}
			<a href="/IBSng/admin/admins/admin_list.php" class="page_menu">Admin List</a>
		    {/menuTR}
		    {menuTR}
			<a href="/IBSng/admin/admins/add_new_admin.php" class="page_menu">Add New Admin</a>
		    {/menuTR}

		    {menuTR}
			<a href="/IBSng/admin/message/view_messages.php" class="page_menu">Messages</a>
		    {/menuTR}
		{/viewTable}

	</td>
    </tr>
    <tr>
	<td valign="top" align="center">
		{viewTable title="Report" table_width="200" nofoot="TRUE" color="red" arrow_color="white"}
		
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
			<a href="/IBSng/admin/report/realtime_log_console.php" class="page_menu">Log Console</a>
		    {/menuTR}

		    {menuTR}
			<a href="/IBSng/admin/report/web_analyzer_logs.php" class="page_menu">Web Analyzer Logs</a>
		    {/menuTR}

		    {menuTR}
			<a href="/IBSng/admin/report/realtime_web_analyzer.php" class="page_menu">RealTime Web Analyzer</a>
		    {/menuTR}


		{/viewTable}
	</td>
	<td valign="top" align="center">
		{viewTable title="Graph" table_width="200" nofoot="TRUE" color="red" arrow_color="white"}
		    {menuTR}
			<a href="/IBSng/admin/graph/realtime/realtime.php?img_url=onlines.php" class="page_menu">All Onlines RealTime Graph</a>
		    {/menuTR}
		    {menuTR}
			<a href="/IBSng/admin/graph/realtime/realtime.php?img_url=onlines.php?internet=1" class="page_menu">Internet Onlines RealTime Graph</a>
		    {/menuTR}
		    {menuTR}
			<a href="/IBSng/admin/graph/realtime/realtime.php?img_url=onlines.php?voip=1" class="page_menu">VoIP Onlines RealTime Graph</a>
		    {/menuTR}
		    {menuTR}
			<a href="/IBSng/admin/graph/realtime/realtime.php?img_url=bw.php" class="page_menu">Internet BW RealTime Graph</a>
		    {/menuTR}

		    {menuTR}
			<a href="/IBSng/admin/graph/onlines.php" class="page_menu">Onlines Graph</a>
		    {/menuTR}

		    {menuTR}
			<a href="/IBSng/admin/graph/analysis/connection_analysis.php" class="page_menu">Connections Analysis</a>
		    {/menuTR}
		    
		{/viewTable}

	</td>
    </tr>
</table>


{addRelatedLink}
    <a href="/IBSng/admin/user/user_info.php" class="RightSide_links">
	User
    </a>
{/addRelatedLink}

{addRelatedLink}
    <a href="/IBSng/admin/group/group_list.php" class="RightSide_links">
	Group
    </a>
{/addRelatedLink}

{addRelatedLink}
    <a href="/IBSng/admin/report/" class="RightSide_links">
	Report
    </a>
{/addRelatedLink}

{addRelatedLink}
    <a href="/IBSng/admin/admins/admin_list.php" class="RightSide_links">
	Admin
    </a>
{/addRelatedLink}

{addRelatedLink}
    <a href="/IBSng/admin/setting/" class="RightSide_links">
	Setting
    </a>
{/addRelatedLink}


{setAboutPage title="Home"}

{/setAboutPage}

{include file="admin_footer.tpl"}

