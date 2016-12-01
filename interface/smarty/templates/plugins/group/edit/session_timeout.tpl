{attrUpdateMethod update_method="sessionTimeout"}

  {viewTable title="Session Timeout" nofoot="TRUE"}
    {addEditTD type="left"}
	Has Session Timeout
    {/addEditTD}

    {addEditTD type="right"}
	<input type=checkbox name="has_session_timeout" value="t" class=checkbox {if attrDefault($group_attrs,"session_timeout","has_session_timeout")!=""}checked{/if} onClick='session_timeout_select.toggle("session_timeout")'>
    {/addEditTD}

    {addEditTD type="left"}
	Session Timeout
    {/addEditTD}

    {addEditTD type="right"}
	<input id="session_timeout" type=text name="session_timeout" value="{attrDefault target="group" default_var="session_timeout" default_request="session_timeout"}" class=small_text> Seconds
    {/addEditTD}

  {/viewTable}
<script language="javascript">
	session_timeout_select=new DomContainer();
	session_timeout_select.disable_unselected=true;
	session_timeout_select.addByID("session_timeout");
{if attrDefault($group_attrs,"session_timeout","has_session_timeout")!=""}
    session_timeout_select.select("session_timeout");
{else}
    session_timeout_select.select(null);
{/if}
</script>


