{viewTable title="Fast Dial" nofoot="TRUE" table_width="100%"}
    {addEditTD type="left" comment=TRUE}
	{strip}
	    {if $can_change} {editCheckBox edit_tpl_name="fast_dial"} {/if}
	    Fast Dial
	{/strip}
    {/addEditTD}
    {addEditTD type="right" comment=TRUE}
		{ifHasAttr object="user" var_name="fast_dial"}
		    {foreach from=$user_attrs.fast_dial item=fast_dial key=index}
			{$index} -> {$user_attrs.fast_dial[$index]} <br />
		    {/foreach}
		{/ifHasAttr} 
		{helpicon subject="fast dial" category="user"}
    {/addEditTD}
{/viewTable}

