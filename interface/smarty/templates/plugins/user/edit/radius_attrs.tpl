{attrUpdateMethod update_method="radiusAttrs"}
{userInfoTable title="Radius Attributes" nofoot="TRUE"}
    {userInfoTD type="user_left"}
	Has Radius Attributes
    {/userInfoTD}
    {userInfoTD type="user_right"}
	<input type=checkbox name="has_radius_attrs" value="t" class=checkbox {if attrDefault($user_attrs,"radius_attrs","has_radius_attrs")!=""}checked{/if} onClick='radius_attrs_select.toggle("radius_attrs")'>
    {/userInfoTD}
    {userInfoTD type="group"}
	{ifHasAttr var_name="radius_attrs" object="group" alternate="No"}
	    Yes
	{/ifHasAttr}
    {/userInfoTD}

    {userInfoTD type="user_left" comment=TRUE}
	Radius Attrs(x="y")
    {/userInfoTD}
    {userInfoTD type="user_right" comment=TRUE}
	<textarea name=radius_attrs id=radius_attrs>{attrDefault target="user" default_var="radius_attrs" default_request="radius_attrs"}</textarea>
    {/userInfoTD}
    {userInfoTD type="group" comment=TRUE}
	{ifHasAttr object="group" var_name="radius_attrs"}
	    {$group_attrs.radius_attrs|nl2br}
	{/ifHasAttr} 
	{helpicon subject="radius attrs" category="user"}
    {/userInfoTD}
{/userInfoTable}
<br>
<script language="javascript">
	radius_attrs_select=new DomContainer();
	radius_attrs_select.disable_unselected=true;
	radius_attrs_select.addByID("radius_attrs");
{if attrDefault($user_attrs,"radius_attrs","has_radius_attrs")!=""}
    radius_attrs_select.select("radius_attrs");
{else}
    radius_attrs_select.select(null);
{/if}
</script>