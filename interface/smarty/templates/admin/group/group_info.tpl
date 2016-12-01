{* Group Info


    Group Properties:
	$group_name
	$group_id
	$comment
	$owner_id
	$owner_name
	$attrs





*}
{include file="admin_header.tpl" title="Group Information" selected="Group List" page_valign=top} 
{include file="err_head.tpl"}
<form method=POST action="/IBSng/admin/plugins/edit.php" name="group_info">
    <input type=hidden name="group_name" value="{$group_name}">
    <input type=hidden name="edit_group" value="1">


{tabTable tabs="Main,Exp Dates,Mailbox,IPPool,Periodic Accounting,Limitations,Multi Login,Misc" content_height=160 action_icon="edit" bgcolor=white tab_each_row=4 form_name="group_info" table_width=350}

    {tabContent tab_name="Main"}
	{include file="plugins/group/view/group_info.tpl"}
	<br>
	{include file="plugins/group/view/normal_charge.tpl"}
	<br>
	{include file="plugins/group/view/voip_charge.tpl"}

    {/tabContent}

    {tabContent tab_name="Exp Dates"}
	{include file="plugins/group/view/exp_date.tpl"}
    {/tabContent}

    {tabContent tab_name="Mailbox"}
	{include file="plugins/group/view/mail_quota.tpl"}
    {/tabContent}

    {tabContent tab_name="Multi Login"}
	{include file="plugins/group/view/multi_login.tpl"}
    {/tabContent}

    {tabContent tab_name="Limitations"}
	{include file="plugins/group/view/limitations.tpl"}
    {/tabContent}

    {tabContent tab_name="IPPool"}
	{include file="plugins/group/view/ippool.tpl"}
    {/tabContent}

    {tabContent tab_name="Periodic Accounting"}
	{include file="plugins/group/view/monthly_time_paccounting.tpl"}
	<br>
	{include file="plugins/group/view/monthly_traffic_paccounting.tpl"}
	<br>
	{include file="plugins/group/view/daily_time_paccounting.tpl"}
	<br>
	{include file="plugins/group/view/daily_traffic_paccounting.tpl"}
    {/tabContent}

    {tabContent tab_name="Misc"}
	{include file="plugins/group/view/save_bw_usage.tpl"}
	<br>
	{include file="plugins/group/view/radius_attrs.tpl"}
	<br>
	{include file="plugins/group/view/voip_preferred_language.tpl"}
    {/tabContent}

    {/tabTable}


</form>

{addRelatedLink}
    <a href="/IBSng/admin/group/group_list.php" class="RightSide_links">
	Group List
    </a>
{/addRelatedLink}

{if $can_del}
    {addRelatedLink}
        <a href="/IBSng/admin/group/group_info.php?delete_group=1&group_name={$group_name|escape:"url"}" 
		{jsconfirm msg="Are you sure you want to delete Group?\\n Warning: Group should not be used in any user."}
		 class="RightSide_links">
	    Delete Group <b>{$group_name}</b>
	</a>
    {/addRelatedLink}
{/if}

{addRelatedLink}
    <a href="/IBSng/admin/user/search_user.php?search=1&show_defaults=1&group_name_{$group_name}={$group_name}&tab1_selected=Group" class="RightSide_links">
	Users With Group <b>{$group_name}</b>
    </a>
{/addRelatedLink}


{setAboutPage title="Group Info"}
You can see which attributes this group have. You can edit attribute values if you have relevant permission
{/setAboutPage}


{include file="admin_footer.tpl"}
