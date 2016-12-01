{if amIGod() or permValueRestricted("CHANGE_USER_OWNER",getAuthUsername())}
{foreach from=$admin_names item=owner_name key=index}
    {if $index==0}
        {multiTableTR}
    {elseif $index%4==0}
        {multiTableTR begin_close_tr=TRUE}
    {/if}

    {multiTableTD type="left"}
    {counter name="owner_search_id" assign="owner_search_id"}
	<input name="owner_name_{$owner_search_id}" value="{$owner_name}" type=checkbox {ifisinrequest name="owner_name_`$owner_search_id`" value="checked"}>
    {/multiTableTD}	
    {multiTableTD type="right" width="25%"}
         {$owner_name}
    {/multiTableTD}
{/foreach}

{/if}
{multiTablePad last_index=$index go_until=3 width="25%"}
</tr><tr><td colspan=30 height=1 bgcolor="#FFFFFF"></td></tr>
