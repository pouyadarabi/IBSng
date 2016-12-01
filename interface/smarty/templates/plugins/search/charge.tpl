{counter name="charge_search_id" start=0 print=false}

{if sizeof($internet_charges)}
    {foreach from=$internet_charges item=charge_name key=index}

	{if $index==0}
    	    {multiTableTR}
	{elseif $index%4==0}
    	    {multiTableTR begin_close_tr=TRUE}
	{/if}

	{multiTableTD type="left"}
    	    <input name="normal_charge_{$charge_name}" value="{$charge_name}" type=checkbox {ifisinrequest name="normal_charge_`$charge_name`" value="checked"}> 
	{/multiTableTD}
	{multiTableTD type="right" width="25%"}
	    {$charge_name}
	{/multiTableTD}
    {/foreach}
    {multiTablePad last_index=$index go_until=3 width="25%"}
{/if}
{if sizeof($voip_charges)}
    {foreach from=$voip_charges item=charge_name key=index}

	{if $index==0}
    	    {multiTableTR}
	{elseif $index%4==0}
    	    {multiTableTR begin_close_tr=TRUE}
	{/if}

	{multiTableTD type="left"}
    	    <input name="voip_charge_{$charge_name}" value="{$charge_name}" type=checkbox {ifisinrequest name="voip_charge_`$charge_name`" value="checked"}> 
	{/multiTableTD}
	{multiTableTD type="right" width="25%"}
	    {$charge_name}
	{/multiTableTD}
    {/foreach}
    {multiTablePad last_index=$index go_until=3 width="25%"}
{/if}

</tr><tr><td colspan=30 height=1 bgcolor="#FFFFFF"></td></tr>
