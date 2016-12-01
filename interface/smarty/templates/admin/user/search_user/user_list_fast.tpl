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
	    Select All:
	    <input type=checkbox name="check_all_users"> 
	    <script language="javascript">
		user_ids.setCheckAll("edit_user","check_all_users");
	    </script>
	{/listTD}
    {/if}	


    {/listTR}

    <tr><td colspan=30>
    {multiTable}

    {assign var="index" value=0}
    {foreach from=$user_ids item=user_id}
        {if $index%4==0}
	    {multiTableTR}
	{/if}


	{multiTableTD type="left"}
	    {math equation="index+1" index=$index}.
	    <input type=checkbox name="edit_user_id_{$user_id}" value="{$user_id}"> 
	{/multiTableTD}
	{multiTableTD type="right" width="25%"}
	    {$user_id}
	{/multiTableTD}

	{math equation="index+1" index=$index assign="index"}
    {/foreach}
    {multiTablePad last_index=$index go_until=4}

    <script language="javascript">
    {foreach from=$user_ids item=user_id}
	user_ids.addByName("edit_user","edit_user_id_{$user_id}");
    {/foreach}
    </script>
    
    {/multiTable}
    
    </td></tr>

{/listTable}
