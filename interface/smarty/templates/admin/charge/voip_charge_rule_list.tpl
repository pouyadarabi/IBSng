{listTable title="VoIP Charge Rule List" cols_num=7}
	{if $can_change and !$is_editing}
	    {listTableHeaderIcon action="edit"}
	    {listTableHeaderIcon action="delete" close_tr=TRUE}
	{/if}
	{listTR type="header"}
	    {listTD}
		ID
	    {/listTD}
	    {listTD}
		Start
	    {/listTD}
	    {listTD}
		End
	    {/listTD}
	    {listTD}
		Tariff Name
	    {/listTD}
	    {listTD}
		RAS
	    {/listTD}
	    {listTD}
		Ports
	    {/listTD}
	    {listTD}
		Days Of Week
	    {/listTD}

	{/listTR}

	{foreach from=$rules item=rule}
	    {listTR type="body"}
		{listTD}
		    {$rule.rule_id}
		{/listTD}
    		{listTD}
		    {$rule.start_time}
		{/listTD}
		{listTD}
		    {$rule.end_time}
    		{/listTD}
		{listTD}
		    <a class="link_in_body" href="/IBSng/admin/charge/voip_tariff/tariff_info.php?tariff_name={$rule.tariff_name|escape:"url"}">
			{$rule.tariff_name}
		    </a>
		{/listTD}
		{listTD}
		    {$rule.ras_description}
		{/listTD}
		{listTD}
		    {arrayJoin array=`$rule.ports` glue=", " truncate=30} 
    		{/listTD}
		{listTD}
		    {arrayJoin array=`$rule.day_of_weeks` glue=", " truncate_each=3} 
    		{/listTD}
		{if $can_change and !$is_editing}
		    {listTD icon=TRUE}
			<a href="/IBSng/admin/charge/edit_voip_charge_rule.php?charge_rule_id={$rule.rule_id}&charge_name={$charge_name|escape:"url"}">{listTableBodyIcon action="edit" cycle_color="TRUE"}</a>
    		    {/listTD}
		    {listTD icon=TRUE}
		        <a {jsconfirm msg="Are you sure you want to delete charge rule with id `$rule.rule_id`"} href="/IBSng/admin/charge/charge_info.php?charge_rule_id={$rule.rule_id}&charge_name={$charge_name|escape:"url"}&delete_charge_rule=1">{listTableBodyIcon action="delete"}</a>
    		    {/listTD}
		{/if}
		{/listTR}
	{/foreach}
{/listTable}
