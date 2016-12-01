<form method=POST action="admin_perms_list.php">
    {addEditTable title="Save Permission Template" table_width="400" action_icon="save"} 
        {addEditTD type="left"}
	    Save This Admin Permissions into template:
        {/addEditTD}
	{addEditTD type="right"}
	    <input class="text" type=text name=template_name>
	    <input type=hidden name=action value=save>
	    <input type=hidden name=admin_username value={$admin_username}>
	{/addEditTD}
    {/addEditTable} 
</form>
<form method=POST action="admin_perms_list.php" name="load_template">
    {addEditTable title="Load Permission Template Into $admin_username" table_width="400" action_icon="load"}
        {addEditTD type="left"}
	    Load Permission Template into admin:
        {/addEditTD}
	{addEditTD type="right"}
	    {literal}
	    <script language="javascript">
		function showTemplatePerms(){
		    selected=getSelectedOption("load_template","template_name");
		    open("show_permtemplate_perms.php?template_name="+selected,"template_perms","width=500,height=400,scrollbars=yes");
		}
	    </script>
	    {/literal}
	    <select name=template_name>
		{html_options values=$templates_list output=$templates_list}
	    </select> <a class="link_in_body" href="javascript:showTemplatePerms();">Show Permissions</a>
	    <input type=hidden name=action value=load>
	    <input type=hidden name=admin_username value={$admin_username}>

	{/addEditTD}
    {/addEditTable} 
</form>
<form method=POST action="admin_perms_list.php" name="del_template">
    {addEditTable title="Delete Permission Template" table_width="400" action_icon="delete"}
        {addEditTD type="left"}
	    Delete Permission Template
        {/addEditTD}
	{addEditTD type="right"}
	    <select name=template_name>
		{html_options values=$templates_list output=$templates_list}
	    </select>
	    <input type=hidden name=action value=delete>
	    <input type=hidden name=admin_username value={$admin_username}>
	{/addEditTD}
    {/addEditTable} 
</form>

	    