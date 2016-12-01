{attrUpdateMethod update_method="saveBWUsage"}

  {viewTable title="Radius Attributes" nofoot="TRUE"}
    {addEditTD type="left"}
	Save BW Usage
    {/addEditTD}

    {addEditTD type="right"}
	<input type=checkbox name="save_bw_usage" value="t" class=checkbox {if attrDefault($group_attrs,"save_bw_usage","save_bw_usage","something")!="something"}checked{/if}>
    {/addEditTD}

  {/viewTable}
