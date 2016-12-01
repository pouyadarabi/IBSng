{attrUpdateMethod update_method="idleTimeout"}

  {viewTable title="Idle Timeout" nofoot="TRUE"}
    {addEditTD type="left"}
	Has Idle Timeout
    {/addEditTD}

    {addEditTD type="right"}
	<input type=checkbox name="has_idle_timeout" value="t" class=checkbox {if attrDefault($group_attrs,"idle_timeout","has_idle_timeout")!=""}checked{/if} onClick='idle_timeout_select.toggle("idle_timeout")'>
    {/addEditTD}

    {addEditTD type="left"}
	Idle Timeout
    {/addEditTD}

    {addEditTD type="right"}
	<input id="idle_timeout" type=text name="idle_timeout" value="{attrDefault target="group" default_var="idle_timeout" default_request="idle_timeout"}" class=small_text> Seconds
    {/addEditTD}

  {/viewTable}
<script language="javascript">
	idle_timeout_select=new DomContainer();
	idle_timeout_select.disable_unselected=true;
	idle_timeout_select.addByID("idle_timeout");
{if attrDefault($group_attrs,"idle_timeout","has_idle_timeout")!=""}
    idle_timeout_select.select("idle_timeout");
{else}
    idle_timeout_select.select(null);
{/if}
</script>


