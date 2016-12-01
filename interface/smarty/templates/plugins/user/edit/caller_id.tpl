{attrUpdateMethod update_method="callerID"}
{viewTable title="Caller ID" table_width="380" nofoot="TRUE"} 
    {addEditTD type="left"}
	Has Caller ID
    {/addEditTD}

    {addEditTD type="right"}
	<input type=checkbox name="has_caller_id" value="t" class=checkbox {if attrDefault($user_attrs,"caller_id","has_caller_id")!=""}checked{/if} onClick='caller_id_select.toggle("caller_id")'>
    {/addEditTD}

    {addEditTD type="left"}
	VoIP Caller ID
    {/addEditTD}

    {addEditTD type="right"}
	<input id="caller_id" type=text  class=text name="caller_id" 
	    value="{attrDefault target="user" default_var="caller_id" default_request="caller_id"}" > 
	{multistr form_name="user_edit" input_name="caller_id"}
	{helpicon subject="caller id" category="user"}
    {/addEditTD}

{/viewTable}
<br>
<script language="javascript">
	caller_id_select=new DomContainer();
	caller_id_select.disable_unselected=true;
	caller_id_select.addByID("caller_id",[]);
{if attrDefault($user_attrs,"caller_id","has_caller_id")!=""}
    caller_id_select.select("caller_id");
{else}
    caller_id_select.select(null);
{/if}
</script>