{attrUpdateMethod update_method="sessionTimeout"}
{userInfoTable title="Session Timeout" nofoot="TRUE"}
    {userInfoTD type="user_left"}
	Has Session Timeout
    {/userInfoTD}
    {userInfoTD type="user_right"}
	<input type=checkbox name="has_session_timeout" value="t" class=checkbox {if attrDefault($user_attrs,"session_timeout","has_session_timeout")!=""}checked{/if} onClick='session_timeout_select.toggle("session_timeout")'>
    {/userInfoTD}
    {userInfoTD type="group"}
	{ifHasAttr var_name="session_timeout" object="group" alternate="No"}
	    Yes
	{/ifHasAttr}
    {/userInfoTD}

    {userInfoTD type="user_left" comment=TRUE}
	Session Timeout
    {/userInfoTD}
    {userInfoTD type="user_right" comment=TRUE}
	<input id="session_timeout" type=text name="session_timeout" value="{attrDefault target="user" default_var="session_timeout" default_request="session_timeout"}" class=small_text> Seconds
    {/userInfoTD}
    {userInfoTD type="group" comment=TRUE}
	{ifHasAttr object="group" var_name="session_timeout"}
	    {$group_attrs.session_timeout} Seconds
	{/ifHasAttr} 
	{helpicon subject="Session Timeout" category="user"}
    {/userInfoTD}
{/userInfoTable}
<br>
<script language="javascript">
	session_timeout_select=new DomContainer();
	session_timeout_select.disable_unselected=true;
	session_timeout_select.addByID("session_timeout");
{if attrDefault($user_attrs,"session_timeout","has_session_timeout")!=""}
    session_timeout_select.select("session_timeout");
{else}
    session_timeout_select.select(null);
{/if}
</script>