{attrUpdateMethod update_method="multiLogin"}
{userInfoTable title="Multi Login" nofoot="TRUE"}
    {userInfoTD type="user_left"}
	Has Multi Login
    {/userInfoTD}
    {userInfoTD type="user_right"}
	<input type=checkbox name="has_multi_login" value="t" class=checkbox {if attrDefault($user_attrs,"multi_login","has_multi_login")!=""}checked{/if} onClick='multi_login_select.toggle("multi_login")'>
    {/userInfoTD}
    {userInfoTD type="group"}
	{ifHasAttr var_name="multi_login" object="group" alternate="No"}
	    Yes
	{/ifHasAttr}
    {/userInfoTD}

    {userInfoTD type="user_left"}
	    Multi Login
    {/userInfoTD}
    {userInfoTD type="user_right"}
	<input id="multi_login" type=text name="multi_login" value="{attrDefault target="user" default_var="multi_login" default_request="multi_login"}" class=small_text> 
    {/userInfoTD}
    {userInfoTD type="group"}
	{ifHasAttr object="group" var_name="multi_login"}
	    {$group_attrs.multi_login} instances 
	{/ifHasAttr} 
	{helpicon subject="multi login" category="user"}
    {/userInfoTD}
{/userInfoTable}
<br>
<script language="javascript">
	multi_login_select=new DomContainer();
	multi_login_select.disable_unselected=true;
	multi_login_select.addByID("multi_login");
{if attrDefault($user_attrs,"multi_login","has_multi_login")!=""}
    multi_login_select.select("multi_login");
{else}
    multi_login_select.select(null);
{/if}
</script>