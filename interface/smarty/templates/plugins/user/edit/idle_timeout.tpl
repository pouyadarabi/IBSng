{attrUpdateMethod update_method="idleTimeout"}
{userInfoTable title="Idle Timeout" nofoot="TRUE"}
    {userInfoTD type="user_left"}
	Has Idle Timeout
    {/userInfoTD}
    {userInfoTD type="user_right"}
	<input type=checkbox name="has_idle_timeout" value="t" class=checkbox {if attrDefault($user_attrs,"idle_timeout","has_idle_timeout")!=""}checked{/if} onClick='idle_timeout_select.toggle("idle_timeout")'>
    {/userInfoTD}
    {userInfoTD type="group"}
	{ifHasAttr var_name="idle_timeout" object="group" alternate="No"}
	    Yes
	{/ifHasAttr}
    {/userInfoTD}

    {userInfoTD type="user_left" comment=TRUE}
	Idle Timeout
    {/userInfoTD}
    {userInfoTD type="user_right" comment=TRUE}
	<input id="idle_timeout" type=text name="idle_timeout" value="{attrDefault target="user" default_var="idle_timeout" default_request="idle_timeout"}" class=small_text> Seconds
    {/userInfoTD}
    {userInfoTD type="group" comment=TRUE}
	{ifHasAttr object="group" var_name="idle_timeout"}
	    {$group_attrs.idle_timeout} Seconds
	{/ifHasAttr} 
	{helpicon subject="Idle Timeout" category="user"}
    {/userInfoTD}
{/userInfoTable}
<br>
<script language="javascript">
	idle_timeout_select=new DomContainer();
	idle_timeout_select.disable_unselected=true;
	idle_timeout_select.addByID("idle_timeout");
{if attrDefault($user_attrs,"idle_timeout","has_idle_timeout")!=""}
    idle_timeout_select.select("idle_timeout");
{else}
    idle_timeout_select.select(null);
{/if}
</script>