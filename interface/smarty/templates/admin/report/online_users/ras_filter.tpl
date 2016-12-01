{foreach from=$ras_descs item=ras_tuple key=index}
	{if $index%4 == 0}
	    {multiTableTR}
	{/if}

	{reportToShowCheckBox name="ras_`$ras_tuple[1]`" value=$ras_tuple[1] output="$ras_tuple[0]" default_checked="FALSE" always_in_form=""}
{/foreach}
{multiTablePad last_index=$index go_until=3 width="25%"}
