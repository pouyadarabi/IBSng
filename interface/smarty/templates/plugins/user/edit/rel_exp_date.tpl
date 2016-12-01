{attrUpdateMethod update_method="relExpDate"}
{userInfoTable title="User Expiration Date" nofoot="TRUE"} 
    {userInfoTD type="user_left"}
	Has Reletaive Expiration Date
    {/userInfoTD}
    {userInfoTD type="user_right"}
	<input type=checkbox name="has_rel_exp" value="t" class=checkbox {if attrDefault($user_attrs,"rel_exp_date","has_rel_exp")!=""}checked{/if} onClick='rel_exp_select.toggle("rel_exp_date")'>
    {/userInfoTD}
    {userInfoTD type="group"}
	{ifHasAttr var_name="rel_exp_date" object="group" alternate="No"}
	    Yes
	{/ifHasAttr}
    {/userInfoTD}


    {userInfoTD type="user_left"}
	Relative Expiration Date:
    {/userInfoTD}

    {userInfoTD type="user_right"}
	<input id="rel_exp_date" type=text class=small_text name="rel_exp_date" value="{attrDefault default_request="rel_exp_date" default_var="rel_exp_date" target="user"}">
	{relative_units id="rel_exp_date_unit" name="rel_exp_date_unit" default_var="rel_exp_date_unit" default_request="rel_exp_date_unit" target="user"}
    {/userInfoTD}

    {userInfoTD type="group"}
	{ifHasAttr var_name="rel_exp_date" object="group"}
	    {$group_attrs.rel_exp_date} {$group_attrs.rel_exp_date_unit}
	{/ifHasAttr}
    {/userInfoTD}
{/userInfoTable}
<br>
<script language="javascript">
	rel_exp_select=new DomContainer();
	rel_exp_select.disable_unselected=true;
	rel_exp_select.addByID("rel_exp_date",Array("rel_exp_date_unit"));
{if attrDefault($user_attrs,"rel_exp_date","has_rel_exp")!=""}
    rel_exp_select.select("rel_exp_date");
{else}
    rel_exp_select.select(null);
{/if}
</script>
