{viewTable title="Internet Charge" nofoot="TRUE"}
    {addEditTD type="left"}
	{strip}
	    {if $can_change}{editCheckBox edit_tpl_name="normal_charge"}{/if}
		Internet Charge
	{/strip}
    {/addEditTD}
    {addEditTD type="right"}
		{ifHasAttr object="group" var_name="normal_charge"}
		    <a class="link_in_body_black" href="/IBSng/admin/charge/charge_info.php?charge_name={$group_attrs.normal_charge|escape:"url"}">
			{$group_attrs.normal_charge}  
		    </a>
		{/ifHasAttr} 
		{helpicon subject="normal charge" category="user"}
    {/addEditTD}

{/viewTable}
