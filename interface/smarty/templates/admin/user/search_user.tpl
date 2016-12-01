{* Search User

*}
{include file="admin_header.tpl" title="User Search" selected="User Information" page_valign=top} 
{include file="err_head.tpl"} 


<script language="javascript" src="/IBSng/js/check_box_container.js"></script>
<form method=POST action="/IBSng/admin/user/search_user.php#show_results" name="search_user">
    {tabTable tabs="Main,Group,Charge,Owner,ExpDates,Lock,Lan,Comment,Misc" content_height=100 action_icon="search" form_name="search_user"}

    {tabContent add_table_tag=TRUE tab_name="Main"}
		{include file="plugins/search/user_id.tpl"} 
		{include file="plugins/search/normal_user.tpl"}
		{include file="plugins/search/voip_user.tpl"}
		{include file="plugins/search/no_username.tpl"}
		{include file="plugins/search/caller_id.tpl"}
		{include file="plugins/search/credit.tpl"}
    {/tabContent}

    {tabContent add_table_tag=TRUE tab_name="Group"}
        {include file="plugins/search/group.tpl"} 
    {/tabContent}

    {tabContent add_table_tag=TRUE tab_name="Charge"}
		{include file="plugins/search/charge.tpl"}
    {/tabContent}

    {tabContent add_table_tag=TRUE tab_name="Owner"}
		{include file="plugins/search/owner.tpl"}
    {/tabContent}

    {tabContent add_table_tag=TRUE tab_name="ExpDates"}
        {include file="plugins/search/abs_exp_date.tpl"}
        {include file="plugins/search/rel_exp_date.tpl"}
        {include file="plugins/search/first_login.tpl"}
    {/tabContent}

    {tabContent add_table_tag=TRUE tab_name="Lock"}
        {include file="plugins/search/lock.tpl"}
    {/tabContent}

    {tabContent add_table_tag=TRUE tab_name="Lan"}
        {include file="plugins/search/persistent_lan.tpl"}
        {include file="plugins/search/limit_mac.tpl"}
        {include file="plugins/search/limit_station_ip.tpl"}
    {/tabContent}

    {tabContent add_table_tag=TRUE tab_name="Comment"}
		{include file="plugins/search/comment.tpl"}
    {/tabContent}

    {tabContent add_table_tag=TRUE tab_name="Misc"}
		{include file="plugins/search/email_address.tpl"}
		{include file="plugins/search/multi_login.tpl"}
		{include file="plugins/search/ippool.tpl"}
		{include file="plugins/search/assign_ip.tpl"}
		{include file="plugins/search/save_bw_usage.tpl"}
		{include file="plugins/search/fast_mode.tpl"}
    {/tabContent}

    <tr><td colspan=20>	
        {include file="report_foot.tpl"}
    </td></tr>

    <tr><td colspan=20>
    	{addAttributeSkel form_name="search_user" title="Attributes to Edit"}
			{include file="admin/user/search_user/search_user_attributs.tpl"}
    	{/addAttributeSkel}
    </td></tr>

    {/tabTable}
    <input type=hidden name=search value=1>
    <input type=hidden name=show_reports value=1>
    <input type=hidden name=page value=1>
</form>
<form method=POST action="" name="edit_user">
<input type=hidden name=submit_form value=1>
{if $show_results}
	<p>
	<a name="show_results"></a>

	{if $fast_mode}
            {include file="admin/user/search_user/user_list_fast.tpl"}
	{else}
		{include file="admin/user/search_user/user_list.tpl"}
	{/if}

	{if $can_change}
	    {literal}
	    <script>
		function submitEdit(var_name)
		{
		    document.edit_user.action="/IBSng/admin/user/search_user_edit.php?"+var_name+"=1";
		    document.edit_user.submit();
		}
		
		function checkAnyUserChecked()
		{
		    if( user_ids.allUnChecked() ) 
		    {
			alert('No user(s) selected');
			return false;
		    }
		    return true;
		}
	    </script>
	    {/literal}

		{listTable no_header=TRUE no_foot=TRUE table_width=50%}
    		{include file = "admin/report/skel_conditions.tpl"
					 name = "edit_attrs"
		 			 form_name = "edit_user"
					 title = "Attributes to Edit"
					 normal_username_checked="FALSE"
					 voip_username_checked="FALSE"
					 inc  = "admin/user/edit_select_attrs.tpl"}
	    {/listTable}

	    <input type=image src="/IBSng/images/icon/edit.gif" name=edit value=edit onClick="javascript:  if(checkAnyUserChecked()) submitEdit('edit'); return false;">
	    <input type=image src="/IBSng/images/icon/change_credit.gif" name=changecredit value="Change Credit" onClick="javascript: if(checkAnyUserChecked()) submitEdit('change_credit'); return false;">
	    <input type=image src="/IBSng/images/icon/view_connection_logs.gif" name=connection_log value="View Connection Logs" onClick="javascript: if(checkAnyUserChecked()) submitEdit('connection_log'); return false;">
	    <input type=image src="/IBSng/images/icon/view_credit_changes.gif" name=credit_log value="View Credit Changes" onClick="javascript: if(checkAnyUserChecked()) submitEdit('credit_change'); return false;">
	    <input type=image src="/IBSng/images/icon/view_audit_logs.gif" name=audit_log value="View Audit Logs" onClick="javascript: if(checkAnyUserChecked()) submitEdit('audit_log'); return false;">
	    <input type=image src="/IBSng/images/icon/delete.gif" name=delete value="Delete" onClick="javascript: if(checkAnyUserChecked()) submitEdit('delete_users'); return false;">

	{/if}
    
</form> 
{reportPages total_results=$result_count do_post=TRUE}

{/if}


{addRelatedLink}
    <a href="/IBSng/admin/user/search_user.php" class="RightSide_links">
	Search User
    </a>
{/addRelatedLink}

{addRelatedLink}
    <a href="/IBSng/admin/user/user_info.php" class="RightSide_links">
	User Information
    </a>
{/addRelatedLink}

{setAboutPage title="Search User"}
You can search through user attributes
{/setAboutPage}

{include file="admin_footer.tpl"}
