{attrUpdateMethod update_method="assignIP"}
{userInfoTable title="Assign IP Address To User" nofoot="TRUE"}
    {userInfoTD type="user_left"}
	Has Assign IP Address To User
    {/userInfoTD}
    {userInfoTD type="user_right"}
	<input type=checkbox name="has_assign_ip" value="t" class=checkbox  onClick='assign_ip_select.toggle("assign_ip")'>
    {/userInfoTD}
    {userInfoTD type="group"}
	{ifHasAttr var_name="assign_ip" object="group" alternate="No"}
	    Yes
	{/ifHasAttr}
    {/userInfoTD}

    {userInfoTD type="user_left" comment=TRUE}
	Assign IP(s) To User
    {/userInfoTD}
    {userInfoTD type="user_right" comment=TRUE}
	<textarea name=assign_ip id=assign_ip class=text>{attrDefault target="user" default_var="assign_ip" default_request="assign_ip"|replace:",":",\n"}</textarea>
	{multistr form_name="user_edit" input_name="assign_ip"}
    {/userInfoTD}
    {userInfoTD type="group" comment=TRUE}
	{ifHasAttr object="group" var_name="assign_ip"}
	    {$group_attrs.assign_ip|replace:",":"<br>"}
	{/ifHasAttr} 
	{helpicon subject="assign ip address" category="user"}
    {/userInfoTD}
{/userInfoTable}
<br>
<script language="javascript">
	assign_ip_select=new DomContainer();
	assign_ip_select.disable_unselected=true;
	assign_ip_select.addByID("assign_ip");
{if attrDefault($user_attrs,"assign_ip","has_assign_ip")!=""}
    assign_ip_select.select("assign_ip");
    document.user_edit.has_assign_ip.checked=true;
{else}
    assign_ip_select.select(null);
{/if}
</script>