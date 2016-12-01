{attrUpdateMethod update_method="absExpDate"}
{include file="util/calendar.tpl"}
{userInfoTable title="User Expiration Date" nofoot="TRUE"} 
    {userInfoTD type="user_left"}
	Has Absolute Expiration Date
    {/userInfoTD}
    {userInfoTD type="user_right"}
	<input type=checkbox name="has_abs_exp" value="t" class=checkbox {if attrDefault($user_attrs,"abs_exp_date","has_abs_exp")!=""}checked{/if} onClick='abs_exp_select.toggle("abs_exp_date_input")'>
    {/userInfoTD}
    {userInfoTD type="group"}
	{ifHasAttr var_name="abs_exp_date" object="group" alternate="No"}
	    Yes
	{/ifHasAttr}
    {/userInfoTD}

    {userInfoTD type="user_left"}
	Absolute Expiration Date:
    {/userInfoTD}

    {userInfoTD type="user_right"}
	{absDateSelect name="abs_exp_date" default_request="abs_exp_date" default_var="abs_exp_date" target="user"}
    {/userInfoTD}

    {userInfoTD type="group"}
	{ifHasAttr var_name="abs_exp_date" object="group"}
	    {$group_attrs.abs_exp_date}
	{/ifHasAttr}
    {/userInfoTD}
{/userInfoTable}
<br>
<script language="javascript">
	abs_exp_select=new DomContainer();
	abs_exp_select.disable_unselected=true;
	abs_exp_select.addByID("abs_exp_date_input",Array("abs_exp_date_select"));
{if attrDefault($user_attrs,"abs_exp_date","has_abs_exp")!=""}
    abs_exp_select.select("abs_exp_date_input");
{else}
    abs_exp_select.select(null);
{/if}
</script>
