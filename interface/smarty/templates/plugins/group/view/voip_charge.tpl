{viewTable title="VoIP Charge" nofoot="TRUE"}
    {addEditTD type="left"}
	{strip}
	    {if $can_change}{editCheckBox edit_tpl_name="voip_charge"}{/if}
	    VoIP Charge
	{/strip}
    {/addEditTD}
    {addEditTD type="right"}
		{ifHasAttr object="group" var_name="voip_charge"}
		    <a class="link_in_body_black" href="/IBSng/admin/charge/charge_info.php?charge_name={$group_attrs.voip_charge|escape:"url"}">
			{$group_attrs.voip_charge}
		    </a>
		{/ifHasAttr} 
		{helpicon subject="voip charge" category="user"}
    {/addEditTD}

{/viewTable}
