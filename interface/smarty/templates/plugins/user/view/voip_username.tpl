{userInfoTable title="VoIP Status" nofoot="TRUE"}
    {userInfoTD type="user_left"}
	{if $can_change_voip}
	    {editCheckBox edit_tpl_name="voip_username"}
	{/if}
	VoIP Username
    {/userInfoTD}

    {userInfoTD type="user_right"}
	{ifHasAttr var_name="voip_username" object="user"}
	    {$user_attrs.voip_username}
	{/ifHasAttr}
	{helpicon subject="voip username" category="user"}
    {/userInfoTD}

    {userInfoTD type="group"}
	N/A
    {/userInfoTD}



    {userInfoTD type="user_left"}
	    {if $can_change_voip}
		{editCheckBox edit_tpl_name="voip_charge"}
	    {/if}
	    VoIP Charge
    {/userInfoTD}
    {userInfoTD type="user_right"}
		{ifHasAttr object="user" var_name="voip_charge"}
		    <a class="link_in_body_black" href="/IBSng/admin/charge/charge_info.php?charge_name={$user_attrs.voip_charge|escape:"url"}">
	    	        {$user_attrs.voip_charge}  
		    </a>
		{/ifHasAttr} 
    {/userInfoTD}
    {userInfoTD type="group"}
		{ifHasAttr object="group" var_name="voip_charge"}
		    <a class="link_in_body_black" href="/IBSng/admin/charge/charge_info.php?charge_name={$group_attrs.voip_charge|escape:"url"}">
			{$group_attrs.voip_charge}  
		    </a>
		{/ifHasAttr} 
		{helpicon subject="voip charge" category="user"}
    {/userInfoTD}

{/userInfoTable}
