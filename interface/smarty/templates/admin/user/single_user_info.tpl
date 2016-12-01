{* User Info
    User Properties:
	$user_info: dic of user infos containing basic_info and attrs
	$user_attrs: parsed attributes of user
	$group_attrs: parsed attributes of group

*}

{include file="admin_header.tpl" title="User Information" selected="User Information" page_valign=top} 
{include file="err_head.tpl"} 
<form method=POST action="/IBSng/admin/plugins/edit.php" name="user_info">
    <input type=hidden name="user_id" value="{$user_id}">
    <input type=hidden name="edit_user" value="1">

    {tabTable tabs="Main,Exp Dates,Comment,Persistent Lan,VoIP,IPPool,Periodic Accounting,Limitations,Multi Login,Mailbox,Approx Duration,Misc" content_height=150 action_icon="edit" bgcolor=white tab_each_row=4 form_name="user_info" table_width="380"}

    {tabContent tab_name="Main"}
	{include file="plugins/user/view/single_user_info.tpl"}
        <br />
	{include file="plugins/user/view/normal_username.tpl"}
	<br />
	{include file="plugins/user/view/voip_username.tpl"}
	<br />
        {include file="plugins/user/view/lock.tpl"}

    {/tabContent}


    {tabContent tab_name="Exp Dates"}
	{include file="plugins/user/view/exp_date.tpl"}
    {/tabContent}

    {tabContent tab_name="Comment"}
        {include file="plugins/user/view/comment.tpl"}
    {/tabContent}

    {tabContent tab_name="Multi Login"}
        {include file="plugins/user/view/multi_login.tpl"}
    {/tabContent}

    {tabContent tab_name="VoIP"}
        {include file="plugins/user/view/caller_id.tpl"}
	<br />
        {include file="plugins/user/view/fast_dial.tpl"}
	<br />
        {include file="plugins/user/view/voip_preferred_language.tpl"}
    {/tabContent}

    {tabContent tab_name="Persistent Lan"}
        {include file="plugins/user/view/persistent_lan.tpl"}
    {/tabContent}

    {tabContent tab_name="Limitations"}
	{include file="plugins/user/view/limitations.tpl"}
    {/tabContent}

    {tabContent tab_name="IPPool"}
	{include file="plugins/user/view/ippool.tpl"}
    {/tabContent}

    {tabContent tab_name="Periodic Accounting"}
	{include file="plugins/user/view/monthly_time_paccounting.tpl"}
	<br>
	{include file="plugins/user/view/monthly_traffic_paccounting.tpl"}
        <br>
        {include file="plugins/user/view/daily_time_paccounting.tpl"}
	<br>
        {include file="plugins/user/view/daily_traffic_paccounting.tpl"}
    {/tabContent}

    {tabContent tab_name="Mailbox"}
        {include file="plugins/user/view/email_address.tpl"}
        {include file="plugins/user/view/mail_quota.tpl"}
    {/tabContent}

    {tabContent tab_name="Approx Duration"}
        {include file="plugins/user/view/approx_duration.tpl"}
    {/tabContent}

    {tabContent tab_name="Misc"}
        {include file="plugins/user/view/save_bw_usage.tpl"}
	<br>
        {include file="plugins/user/view/radius_attrs.tpl"}
    {/tabContent}

    {/tabTable}

</form> 


{addRelatedLink}
    <a href="/IBSng/admin/report/connections.php?user_ids={$user_id}" class="RightSide_links">
	Connection Logs of <b>User</b>
    </a>
{/addRelatedLink}

{addRelatedLink}
    <a href="/IBSng/admin/report/credit_changes.php?user_ids={$user_id}" class="RightSide_links">
	Credit Changes of <b>User</b>
    </a>
{/addRelatedLink}

{addRelatedLink}
    <a href="/IBSng/admin/report/user_audit_logs.php?user_ids={$user_id}" class="RightSide_links">
	User Audit Logs of <b>User</b>
    </a>
{/addRelatedLink}


{if $can_delete}
    {addRelatedLink}
	<a href="/IBSng/admin/user/del_user.php?user_id={$user_id}" class="RightSide_links">
	    Delete <b>User</b>
	</a>
    {/addRelatedLink}
{/if}

{addRelatedLink}
    <a href="/IBSng/admin/message/post_message_to_user.php?user_id={$user_id}" class="RightSide_links">
	Post Message To <b>User<b>
    </a>
{/addRelatedLink}

{addRelatedLink}
    <a href="/IBSng/admin/user/search_add_user_saves.php?user_id={$user_id}&order_by=add_date&desc=1&show=1" class="RightSide_links">
	Add User Saves Of <b>User</b>
    </a>
{/addRelatedLink}

{addRelatedLink}
    <a href="/IBSng/admin/graph/analysis/connection_analysis.php?user_ids={$user_id}&analysis_type=durations&show=1" class="RightSide_links">
	Connection Analysis Of <b>User</b>
    </a>
{/addRelatedLink}

{addRelatedLink}
    <a href="/IBSng/admin/report/web_analyzer_logs.php?user_ids={$user_id}" class="RightSide_links">
	Web Analysis Of <b>User</b>
    </a>
{/addRelatedLink}

{if isset($user_attrs.save_bw_usage) || isset($group_attrs.save_bw_usage)}
    {if isset( $user_attrs.normal_username ) }
	{assign var="username" value=`$user_attrs.normal_username`}
    {else}
	{assign var="username" value=`$user_id`}
    {/if}

    {addRelatedLink}
	<a href="/IBSng/admin/graph/bw_graph.php?user_id={$user_id}&username={$username}" class="RightSide_links">
	    BW Usage Graph <b>User</b>
	</a>
    {/addRelatedLink}
{/if} 


{setAboutPage title="User Info"}
User Informations and Attributes are shown here. If user doesn't have any attribute, it's value is empty.
{/setAboutPage}


{include file="admin_footer.tpl"}
