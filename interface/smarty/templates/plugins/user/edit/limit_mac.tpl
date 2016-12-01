{attrUpdateMethod update_method="limitMac"}
{userInfoTable title="Limit Mac Address" nofoot="TRUE"}
    {userInfoTD type="user_left"}
	Has Mac Address Limitation
    {/userInfoTD}
    {userInfoTD type="user_right"}
	<input type=checkbox name="has_limit_mac" value="t" class=checkbox {if attrDefault($user_attrs,"limit_mac","has_limit_mac")!=""}checked{/if} onClick='limit_mac_select.toggle("limit_mac")'>
    {/userInfoTD}
    {userInfoTD type="group"}
	{ifHasAttr var_name="limit_mac" object="group" alternate="No"}
	    Yes
	{/ifHasAttr}
    {/userInfoTD}

    {userInfoTD type="user_left" comment=TRUE}
	Limit Mac Address
    {/userInfoTD}
    {userInfoTD type="user_right" comment=TRUE}
	<textarea name=limit_mac id=limit_mac class=text>{attrDefault target="user" default_var="limit_mac" default_request="limit_mac"|replace:",":",\n"}</textarea>
	{multistr form_name="user_edit" input_name="limit_mac"}
    {/userInfoTD}
    {userInfoTD type="group" comment=TRUE}
	{ifHasAttr object="group" var_name="limit_mac"}
	    {$group_attrs.limit_mac|replace:",":"<br>"}
	{/ifHasAttr} 
	{helpicon subject="limit mac address" category="user"}
    {/userInfoTD}
{/userInfoTable}
<br>
<script language="javascript">
	limit_mac_select=new DomContainer();
	limit_mac_select.disable_unselected=true;
	limit_mac_select.addByID("limit_mac");
{if attrDefault($user_attrs,"limit_mac","has_limit_mac")!=""}
    limit_mac_select.select("limit_mac");
{else}
    limit_mac_select.select(null);
{/if}
</script>