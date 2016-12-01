{userInfoTable title="Save BW Usage" nofoot="TRUE"}
    {userInfoTD type="user_left"}
        {if $can_change}{editCheckBox edit_tpl_name="save_bw_usage"}{/if}
        Save Bandwidth Usage
    {/userInfoTD}
    {userInfoTD type="user_right"}
	{ifHasAttr object="user" var_name="save_bw_usage" alternate="&nbsp;&nbsp;No"}
	    Yes
	{/ifHasAttr}
    {/userInfoTD}
    {userInfoTD type="group"}
	{ifHasAttr object="group" var_name="save_bw_usage" alternate="No"}
	    Yes
	{/ifHasAttr} 
	{helpicon subject="Save BW Usage" category="user"}
    {/userInfoTD}

{/userInfoTable}
