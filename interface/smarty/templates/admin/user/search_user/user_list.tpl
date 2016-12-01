<script language="javascript">
    var user_ids=new CheckBoxContainer();
</script>

{listTable no_header=TRUE} 
    {listTableHeader cols_num=30 type="left"}
	List of Users
    {/listTableHeader}
    {listTableHeader type="right"}
	Total Results:  <font color="#9a1111">{$result_count}</font> 
    {/listTableHeader}
    {listTR type="header" }
    	{if $can_change}
			{listTD}
		    	<input type=checkbox name="check_all_users"> 
		    	<script language="javascript">
					user_ids.setCheckAll("edit_user","check_all_users");
		    	</script>
			{/listTD}
    	{/if}
    	
	{eval var=$generated_tpl_header}

    {/listTR}

{foreach from=$reports item=row}

	{assign var="user_id" value=`$row.report_root.user_id`}
	{listTR type="body" cycle_color=TRUE hover_location="/IBSng/admin/user/user_info.php?user_id=`$user_id`"}
	    {if $can_change}
			{listTD extra="onClick='event.cancelBubble=true;'"}
	    		<input type=checkbox name="edit_user_id_{$user_id}" value="{$user_id}"> 
		    	<script language="javascript">
					user_ids.addByName("edit_user","edit_user_id_{$user_id}");
		    	</script>
        	{/listTD}	
	    {/if}
	    {eval var=$generated_tpl_body}
	{/listTR}
{/foreach}

{/listTable}
