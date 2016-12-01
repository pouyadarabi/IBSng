{attrUpdateMethod update_method="multiLogin"}
  {viewTable title="Multi Login" nofoot="TRUE"}
    {addEditTD type="left"}
	Has Multi Login
    {/addEditTD}

    {addEditTD type="right"}
	<input type=checkbox name="has_multi_login" value="t" class=checkbox {if attrDefault($group_attrs,"multi_login","has_multi_login")!=""}checked{/if} onClick='multi_login_select.toggle("multi_login")'>
    {/addEditTD}

    {addEditTD type="left"}
	Multi Login
    {/addEditTD}

    {addEditTD type="right"}
	<input id="multi_login" type=text name="multi_login" value="{attrDefault target="group" default_var="multi_login" default_request="multi_login"}" class=small_text> 
    {/addEditTD}

  {/viewTable}
  <BR>
<script language="javascript">
	multi_login_select=new DomContainer();
	multi_login_select.disable_unselected=true;
	multi_login_select.addByID("multi_login");
{if attrDefault($group_attrs,"multi_login","has_multi_login")!=""}
    multi_login_select.select("multi_login");
{else}
    multi_login_select.select(null);
{/if}
</script>

