{userInfoTable title="Preferred Language" nofoot="TRUE"}
    {userInfoTD type="user_left"}
	{strip}
	    {if $can_change} {editCheckBox edit_tpl_name="voip_preferred_language"} {/if}
	    Preferred Language
	{/strip}
    {/userInfoTD}
    {userInfoTD type="user_right"}
	{ifHasAttr object="user" var_name="voip_preferred_language"}
	    {$user_attrs.voip_preferred_language}
	{/ifHasAttr} 
    {/userInfoTD}
    {userInfoTD type="group"}
	{ifHasAttr object="group" var_name="voip_preferred_language"}
	    {$group_attrs.voip_preferred_language}
	{/ifHasAttr} 
	{helpicon subject="voip preferred language" category="user"}
    {/userInfoTD}
{/userInfoTable}

