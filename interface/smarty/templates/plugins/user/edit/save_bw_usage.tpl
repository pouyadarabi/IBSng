{attrUpdateMethod update_method="saveBWUsage"}
{userInfoTable title="Save BW Usage" nofoot="TRUE"}
    {userInfoTD type="user_left"}
	Save Bandwidth Usage
    {/userInfoTD}
    {userInfoTD type="user_right"}
	<input type=checkbox name="save_bw_usage" value="t" class=checkbox {if attrDefault($user_attrs,"save_bw_usage","save_bw_usage","something")!="something"}checked{/if}>
    {/userInfoTD}
    {userInfoTD type="group"}
	{ifHasAttr var_name="save_bw_usage" object="group" alternate="No"}
	    Yes
	{/ifHasAttr}
    {/userInfoTD}
{/userInfoTable}

