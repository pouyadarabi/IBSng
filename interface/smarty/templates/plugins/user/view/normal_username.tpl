{userInfoTable title="Internet Status" nofoot="TRUE"}
    {userInfoTD type="user_left"}
	{if $can_change_normal}
	    {editCheckBox edit_tpl_name="normal_username"}
	{/if}
	Internet Username
    {/userInfoTD}

    {userInfoTD type="user_right"}
	{ifHasAttr var_name="normal_username" object="user"}
	    {$user_attrs.normal_username}
	{/ifHasAttr}
	{helpicon subject="normal username" category="user"}
    {/userInfoTD}

    {userInfoTD type="group"}
	N/A
    {/userInfoTD}

    {userInfoTD type="user_left"}
	{if $can_change_normal}
	    {editCheckBox edit_tpl_name="normal_charge"}
	{/if}
	Internet Charge
    {/userInfoTD}
    {userInfoTD type="user_right"}
		{ifHasAttr object="user" var_name="normal_charge"}
		    <a class="link_in_body_black" href="/IBSng/admin/charge/charge_info.php?charge_name={$user_attrs.normal_charge|escape:"url"}">
			{$user_attrs.normal_charge}
		    </a>
		{/ifHasAttr} 
    {/userInfoTD}
    {userInfoTD type="group"}
		{ifHasAttr object="group" var_name="normal_charge"}
		    <a class="link_in_body_black" href="/IBSng/admin/charge/charge_info.php?charge_name={$group_attrs.normal_charge|escape:"url"}">
			{$group_attrs.normal_charge}  
		    </a>
		{/ifHasAttr} 
		{helpicon subject="normal charge" category="user"}
    {/userInfoTD}

{/userInfoTable}
