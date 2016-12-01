{attrUpdateMethod update_method="limitCallerID"}

  {viewTable title="Limit Caller ID" nofoot="TRUE"}
    {addEditTD type="left"}
	Has Caller ID Limitation
    {/addEditTD}

    {addEditTD type="right"}
	<input type=checkbox name="has_limit_caller_id" value="t" class=checkbox {if attrDefault($group_attrs,"limit_caller_id","has_limit_caller_id")!=""}checked{/if} onClick='limit_caller_id_select.toggle("limit_caller_id")'>
    {/addEditTD}

    {addEditTD type="left" comment=TRUE}
	Limit Mac Address
    {/addEditTD}

    {addEditTD type="right" comment=TRUE}
	<textarea name=limit_caller_id id=limit_caller_id>{attrDefault target="group" default_var="limit_caller_id" default_request="limit_caller_id"}</textarea>
	{multistr form_name="group_edit" input_name="limit_caller_id"}
    {/addEditTD}

    {addEditTD type="left"}
	Allow users without caller id
    {/addEditTD}

    {addEditTD type="right"}
	<input type=checkbox name="limit_caller_id_allow_not_defined" id="limit_caller_id_allow_not_defined"
	    {if attrDefault($group_attrs,"limit_caller_id_allow_not_defined","limit_caller_id_allow_not_defined") != FALSE}checked{/if} >
    {/addEditTD}


  {/viewTable}
<script language="javascript">
	limit_caller_id_select=new DomContainer();
	limit_caller_id_select.disable_unselected=true;
	limit_caller_id_select.addByID("limit_caller_id",["limit_caller_id_allow_not_defined"]);
{if attrDefault($group_attrs,"limit_caller_id","has_limit_caller_id")!=""}
    limit_caller_id_select.select("limit_caller_id");
{else}
    limit_caller_id_select.select(null);
{/if}
</script>


