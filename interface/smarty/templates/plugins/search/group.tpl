
{counter name="group_search_id" start=0 print=false}

{foreach from=$group_names item=group_name key=index}
    {if $index%4==0}
        {multiTableTR}
    {/if}

    {multiTableTD type="left"}
	<input name="group_name_{$group_name}" value="{$group_name}" type=checkbox {ifisinrequest name="group_name_`$group_name`" value="checked"}> 
    {/multiTableTD}	
    {multiTableTD type="right" width="25%"}
        {$group_name}
    {/multiTableTD}
{/foreach}
{multiTablePad last_index=$index go_until=4 width="25%"}
</tr><tr><td colspan=30 height=1 bgcolor="#FFFFFF"></td></tr>
