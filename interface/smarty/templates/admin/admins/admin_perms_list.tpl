{* List permissions of an admin
    
*}
{config_load file=admin_perms_list.conf}
{config_load file=perm_category_names.conf}
{include file="admin_header.tpl" title="Admin [$admin_username] Permission List" selected="Admin List"}
{include file="err_head.tpl"}

    

<center>

{headerMsg var_name="del_perm_success"}
    Permission deleted from admin successfully
{/headerMsg}

{headerMsg var_name="del_perm_val_success"}
    Permission Value updated successfully
{/headerMsg}

{headerMsg var_name="save_template_success"}
    Permissions Saved to template successfully
{/headerMsg}

{headerMsg var_name="load_template_success"}
    Permission Template Loaded into admin successfully
{/headerMsg}

{headerMsg var_name="del_template_succes"}
    Permission Template Deleted successfully
{/headerMsg}


<table boreder=1>
<tr><td>

    {foreach from=$perms key=category item=cat_perms}
	{listTable title="`$category_names.$category`" cols_num=3 table_width="100%"}
	    {listTableHeaderIcon action="view"}
	{if $can_change eq TRUE}
	    {listTableHeaderIcon action="delete" close_tr=TRUE}
	{/if}
	    {listTR type="header"}
		{listTD}
		    Name
		{/listTD}
		{listTD}
		    Value
		{/listTD}
		{listTD}
			Description
		{/listTD}
	    {/listTR}	
        {foreach from=$cat_perms item=perm}
	    {listTR type="body"}
		{listTD}
		    <nobr><b><font size=2>{$perm.name}</font></b>
		{/listTD}
		{listTD}
		    {if $perm.value_type eq "NOVALUE"}
			No Value
		    {elseif $perm.value_type eq "SINGLEVALUE"}
			{$perm.value} 
			{if $can_change eq TRUE}
			    <a class="link_in_body" href="{eval var=#show_perms_link#}">
				Change
			    </a>
			{/if}
		{elseif $perm.value_type eq "MULTIVALUE"}
			<table border=1 style="border-collapse:collapse" bordercolor="#c0c0c0">
			{foreach from=$perm.value item=val}
			    <tr class="{cycle values="list_Row_LightColor,list_Row_DarkColor"}">
				<td>
				    {$val} 
				<td>
				    {if $can_change eq TRUE}
					<a class="link_in_body" href="/IBSng/admin/admins/admin_perms_list.php?admin_username={$admin_username}&delete_perm={$perm.name|escape:"url"}&delete_perm_val={$val|escape:"url"}" 
					 {jsconfirm msg="Are you sure you want to delete value $val from `$perm.name`"}>
					    <font size=1><b>Delete</b></font>
					</a>
				    {/if}
			{/foreach}
			{if $can_change eq TRUE}
			    <tr class="{cycle values="list_Row_LightColor,list_Row_DarkColor"}">
				<td colspan=2>
				    <a class="link_in_body" href="{eval var=#show_perms_link#}">
					    <b><nobr>Add Another Value</b>
				    </a>
			{/if}
			</table>
			    			
		    {/if}
		{/listTD}
		{listTD}
		    {$perm.description|truncate:100}
		{/listTD}
				
		{listTD icon="TRUE"}
		    <a href="{eval var=#show_perms_link#}">
			    {listTableBodyIcon action="view" cycle_color="TRUE"}
		    </a>
		{/listTD}

		{listTD icon="TRUE"}
		{if $can_change eq TRUE}
		    <a href="/IBSng/admin/admins/admin_perms_list.php?admin_username={$admin_username}&delete_perm={$perm.name|escape:"url"}"
		    {jsconfirm msg="Are you sure you want to delete Permission `$perm.name`"}>
		    {listTableBodyIcon action="delete"}
		    </a>
		{/if}
		{/listTD}

	        {/listTR}
	    {/foreach}
		{/listTable}
	    {/foreach}
	    </td></tr></table>


{if $can_change eq TRUE}
    {include file="admin/admins/admin_perms_list_templates.tpl"}
{addRelatedLink}
    <a href="/IBSng/admin/admins/show_perm_categories.php?admin_username={$admin_username}" class="RightSide_links">
	Add New Permission to <b>{$admin_username|capitalize}</b>
    </a>
{/addRelatedLink}
{/if}

{addRelatedLink}
    <a href="/IBSng/admin/admins/admin_info.php?admin_username={$admin_username}" class="RightSide_links">
	Admin <b>{$admin_username|capitalize}</b> info
    </a>
{/addRelatedLink}
{addRelatedLink}
    <a href="/IBSng/admin/admins/admin_list.php" class="RightSide_links">
	Admin List
    </a>
{/addRelatedLink}
{addRelatedLink}
    <a href="/IBSng/admin/admins/add_new_admin.php" class="RightSide_links">
	Add New Admin
    </a>
{/addRelatedLink}
{setAboutPage title="Admin Change Password"}

{/setAboutPage}


{include file="admin_footer.tpl"}