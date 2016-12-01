{* Show Permissions of one category
    
*}
{config_load file=perm_category_names.conf}
{include file="admin_header.tpl" title="Add Permission to admin [$admin_username]" selected="Admin List"}
{include file="err_head.tpl"}

<table border="0"  class="List_Main" cellspacing="1" bordercolor="#FFFFFF" cellpadding="0" width="400">
	<tr>
		<td class="Menu_Content_Row_white" align="center" colspan=4>
		<font size=2 color="#800000">Please Select Permission category:</font></td>
	<tr>	
	    <td>
		<img border=0 src="/IBSng/images/permission/admin_permission.gif">
	    <td class="Menu_Content_Row_white">
	    <a class="page_menu" href="/IBSng/admin/admins/show_perms.php?category=ADMIN&admin_username={$admin_username}">{#ADMIN#}</a>
		
	    <td>
		<img border=0 src="/IBSng/images/permission/user_permission.gif">
	    <td class="Menu_Content_Row_white">	
		<a class="page_menu" href="/IBSng/admin/admins/show_perms.php?category=USER&admin_username={$admin_username}">{#USER#}</a>

	<tr>	
	    <td>
		<img border=0 src="/IBSng/images/permission/charge_permission.gif">
	    <td class="Menu_Content_Row_white">
		<a class="page_menu" href="/IBSng/admin/admins/show_perms.php?category=CHARGE&admin_username={$admin_username}">{#CHARGE#}</a>
		
	    <td>
		<img border=0 src="/IBSng/images/permission/group_permission.gif">
	    <td class="Menu_Content_Row_white">
		<a class="page_menu" href="/IBSng/admin/admins/show_perms.php?category=GROUP&admin_username={$admin_username}">{#GROUP#}</a>

	<tr>	
	    <td>
		<img border=0 src="/IBSng/images/permission/ras_permission.gif">
	    <td class="Menu_Content_Row_white">
		<a class="page_menu" href="/IBSng/admin/admins/show_perms.php?category=RAS&admin_username={$admin_username}">{#RAS#}</a>
		
	    <td>
		<img border=0 src="/IBSng/images/permission/misc_permission.gif">
	    <td class="Menu_Content_Row_white">
		<a class="page_menu" href="/IBSng/admin/admins/show_perms.php?category=MISC&admin_username={$admin_username}">{#MISC#}</a>

    </table>

</form>
{addRelatedLink}
    <a href="/IBSng/admin/admins/show_perm_categories.php?admin_username={$admin_username}" class="RightSide_links">
	Add New Permission to <b>{$admin_username|capitalize}</b>
    </a>
{/addRelatedLink}

{addRelatedLink}
    <a href="/IBSng/admin/admins/admin_perms_list.php?admin_username={$admin_username}" class="RightSide_links">
	<b>{$admin_username|capitalize}</b> Permissions
    </a>
{/addRelatedLink}

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

{setAboutPage title="Add New Permission"}

{/setAboutPage}

{include file="admin_footer.tpl"}