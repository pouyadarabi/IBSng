{attrUpdateMethod update_method="limitCallerID"}
{userInfoTable title="Limit Caller ID" nofoot="TRUE"}
    {userInfoTD type="user_left"}
	Has Caller ID Limitation
    {/userInfoTD}
    {userInfoTD type="user_right"}
	<input type=checkbox name="has_limit_caller_id" value="t" class=checkbox {if attrDefault($user_attrs,"limit_caller_id","has_limit_caller_id")!=""}checked{/if} onClick='limit_caller_id_select.toggle("limit_caller_id")'>
    {/userInfoTD}
    {userInfoTD type="group"}
	{ifHasAttr var_name="limit_caller_id" object="group" alternate="No"}
	    Yes
	{/ifHasAttr}
    {/userInfoTD}

    {userInfoTD type="user_left" comment=TRUE}
	Limit Caller ID
    {/userInfoTD}
    {userInfoTD type="user_right" comment=TRUE}
	<textarea name=limit_caller_id id=limit_caller_id class=text>{attrDefault target="user" default_var="limit_caller_id" default_request="limit_caller_id"|replace:",":",\n"}</textarea>
	{multistr form_name="user_edit" input_name="limit_caller_id"}
    {/userInfoTD}
    {userInfoTD type="group" comment=TRUE}
	{ifHasAttr object="group" var_name="limit_caller_id"}
	    {$group_attrs.limit_caller_id|replace:",":"<br>"}
	{/ifHasAttr} 
	{helpicon subject="limit caller id" category="user"}
    {/userInfoTD}


    {userInfoTD type="user_left"}
	Allow users with no caller id
    {/userInfoTD}
    {userInfoTD type="user_right"}
	<input type=checkbox name="limit_caller_id_allow_not_defined" id="limit_caller_id_allow_not_defined"
	    {if attrDefault($user_attrs,"limit_caller_id_allow_not_defined","limit_caller_id_allow_not_defined") != FALSE}checked{/if} >
    {/userInfoTD}
    {userInfoTD type="group"}
	{ifHasAttr object="group" var_name="limit_caller_id"}
	    {if $group_attrs.limit_caller_id_allow_not_defined == FALSE }
		No
	    {else}
		Yes
	    {/if}
	{/ifHasAttr} 
	{helpicon subject="Allow users with no caller id" category="user"}
    {/userInfoTD}

{/userInfoTable}
<br>
<script language="javascript">
	limit_caller_id_select=new DomContainer();
	limit_caller_id_select.disable_unselected=true;
	limit_caller_id_select.addByID("limit_caller_id",["limit_caller_id_allow_not_defined"]);
	
{if attrDefault($user_attrs,"limit_caller_id","has_limit_caller_id")!=""}
    limit_caller_id_select.select("limit_caller_id");
{else}
    limit_caller_id_select.select(null);
{/if}
</script>