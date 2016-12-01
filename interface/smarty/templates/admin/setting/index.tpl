{include file="admin_header.tpl" title="Setting" selected="Charge"}

<table border=0 width="100%" height="100%" cellspacing=0 cellpadding=0>
    <tr>
	<td colspan=2 height=30>
	</td>
    </tr>	
    <tr>
	<td valign="top" align="center"> 
		{viewTable title="Charge" table_width="200" nofoot="TRUE" color="red" arrow_color="white"}
		    {menuTR}
			<a href="/IBSng/admin/charge/charge_list.php" class="page_menu">Charge List</a>
		    {/menuTR}
		    {menuTR}
			<a href="/IBSng/admin/charge/add_new_charge.php" class="page_menu">Add New Charge</a>
		    {/menuTR}
		{/viewTable}
	</td>
	<td valign="top" align="center">
		{viewTable title="RAS" table_width="200" nofoot="TRUE" color="green" arrow_color="white"}
		    {menuTR}
			<a href="/IBSng/admin/ras/ras_list.php" class="page_menu">RAS List</a>
		    {/menuTR}
		    {menuTR}
			<a href="/IBSng/admin/ras/add_new_ras.php" class="page_menu">Add New RAS</a>
		    {/menuTR}
		{/viewTable}
	</td>
    </tr>
    <tr>
	<td valign="top" align="center">
		{viewTable title="IPpool" table_width="200" nofoot="TRUE" color="blue" arrow_color="white"}
		    {menuTR}
			<a href="/IBSng/admin/ippool/ippool_list.php" class="page_menu">IPpool List</a>
		    {/menuTR}
		    {menuTR}
			<a href="/IBSng/admin/ippool/add_new_ippool.php" class="page_menu">Add New IPpool</a>
		    {/menuTR}
		{/viewTable}
	</td>
	<td valign="top" align="center">
		{viewTable title="Misc" table_width="200" nofoot="TRUE" color="brown" arrow_color="white"}
		    {menuTR}
			<a href="/IBSng/admin/bw/interface_list.php" class="page_menu">Bandwidth Managment</a>
		    {/menuTR}
		    {menuTR}
			<a href="/IBSng/admin/charge/voip_tariff/tariff_list.php" class="page_menu">VoIP Tariff</a>
		    {/menuTR}
		    {menuTR}
			<a href="/IBSng/admin/report/clean_reports.php" class="page_menu">Clean Reports</a>
		    {/menuTR}
		    {menuTR}
			<a href="/IBSng/admin/misc/core_statistics.php" class="page_menu">Core Statistics</a>
		    {/menuTR}
		    {menuTR}
			<a href="/IBSng/admin/misc/show_ibs_defs.php" class="page_menu">Advanced Configuration</a>
		    {/menuTR}
		{/viewTable}
	</td>
    </tr>
</table>


{addRelatedLink}
    <a href="/IBSng/admin/charge/add_new_charge.php" class="RightSide_links">
	Add New Charge
    </a>
{/addRelatedLink}

{addRelatedLink}
    <a href="/IBSng/admin/ras/add_new_ras.php" class="RightSide_links">
	Add New RAS
    </a>
{/addRelatedLink}

{addRelatedLink}
    <a href="/IBSng/admin/ippool/add_new_ippool.php" class="RightSide_links">
	Add New IPpool
    </a>
{/addRelatedLink}

{addRelatedLink}
    <a href="/IBSng/admin/bw/interface_list.php" class="RightSide_links">
	Bandwidth Managment
    </a>
{/addRelatedLink}
{addRelatedLink}
    <a href="/IBSng/admin/misc/show_ibs_defs.php" class="RightSide_links">
	Advanced Configuration	
    </a>
{/addRelatedLink}


{setAboutPage title="setting"}

{/setAboutPage}
{include file="admin_footer.tpl"}

