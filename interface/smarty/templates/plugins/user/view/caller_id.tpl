{viewTable title="Caller ID" table_width="100%" nofoot="TRUE"} 
    {addEditTD type="left"}
	{if $can_change_voip}
	    {editCheckBox edit_tpl_name="caller_id"}
	{/if}
	VoIP Caller ID
    {/addEditTD}

    {addEditTD type="right"}
	{ifHasAttr var_name="caller_id" object="user"}
	    {$user_attrs.caller_id}
	    <input type=hidden name=hidden_caller_id value="{$user_attrs.caller_id}">
	    {multistr form_name="user_info" input_name="hidden_caller_id"}
	{/ifHasAttr}
	{helpicon subject="caller id" category="user"}
    {/addEditTD}
{/viewTable}
