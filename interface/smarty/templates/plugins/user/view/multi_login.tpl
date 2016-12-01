{userInfoTable title="Multi Login" nofoot="TRUE"}
    {userInfoTD type="user_left"}
	{strip}
	    {if $can_change} {editCheckBox edit_tpl_name="multi_login"} {/if}
	    Multi Login
	{/strip}
    {/userInfoTD}
    {userInfoTD type="user_right"}
		{ifHasAttr object="user" var_name="multi_login"}
		    {$user_attrs.multi_login} instances 
		{/ifHasAttr} 
    {/userInfoTD}
    {userInfoTD type="group"}
		{ifHasAttr object="group" var_name="multi_login"}
		    {$group_attrs.multi_login} instances 
		{/ifHasAttr} 
		{helpicon subject="multi login" category="user"}
    {/userInfoTD}
{/userInfoTable}

