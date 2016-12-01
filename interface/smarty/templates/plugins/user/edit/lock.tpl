{attrUpdateMethod update_method="lock"}
{viewTable title="User Lock" table_width="380" nofoot="TRUE"} 
    {addEditTD type="left"}
	User is Locked
    {/addEditTD}

    {addEditTD type="right"}
	<input type=checkbox name="has_lock" value="t" class=checkbox {if attrDefault($user_attrs,"lock","has_lock","_empty_")!="_empty_"}checked{/if} onClick='lock_select.toggle("lock")'>
	{helpicon subject="lock" category="user"}
    {/addEditTD}

    {addEditTD type="left" comment=TRUE}
	Lock Reason
    {/addEditTD}

    {addEditTD type="right" comment=TRUE}
	<textarea name="lock" id="lock" class=text>{attrDefault target="user" default_var="lock" default_request="lock"}</textarea>
    {/addEditTD}
{/viewTable}
<script language="javascript">
	lock_select=new DomContainer();
	lock_select.disable_unselected=true;
	lock_select.addByID("lock");
{if attrDefault($user_attrs,"lock","has_lock","_empty_")!="_empty_"}
    lock_select.select("lock");
{else}
    lock_select.select(null);
{/if}
</script>