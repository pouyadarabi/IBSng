{attrUpdateMethod update_method="relExpDate"}

  {viewTable title="Expiration Dates" nofoot="TRUE"}
    {addEditTD type="left"}
	Has Relative Expiration Date
    {/addEditTD}

    {addEditTD type="right"}
	<input type=checkbox name="has_rel_exp" value="t" class=checkbox {if attrDefault($group_attrs,"rel_exp_date","has_rel_exp")!=""}checked{/if} onClick='rel_exp_select.toggle("rel_exp_date")'>
    {/addEditTD}

    {addEditTD type="left"}
	Relative Expiration Date
    {/addEditTD}

    {addEditTD type="right"}
	<input id="rel_exp_date" type=text name="rel_exp_date" value="{attrDefault target="group" default_var="rel_exp_date" default_request="rel_exp_date"}" class=small_text > 
	{relative_units name="rel_exp_date_unit" id="rel_exp_date_unit" default_var="rel_exp_date_unit" default_request="rel_exp_date_unit" target="group"}
    {/addEditTD}

  {/viewTable}
<BR>
<script language="javascript">
	rel_exp_select=new DomContainer();
	rel_exp_select.disable_unselected=true;
	rel_exp_select.addByID("rel_exp_date",Array("rel_exp_date_unit"));
{if attrDefault($group_attrs,"rel_exp_date","has_rel_exp")!=""}
    rel_exp_select.select("rel_exp_date");
{else}
    rel_exp_select.select(null);
{/if}
</script>


