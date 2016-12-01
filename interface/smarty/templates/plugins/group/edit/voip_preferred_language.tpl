{attrUpdateMethod update_method="voipPreferredLanguage"}
  {viewTable title="Preferred Language" nofoot="TRUE"}
    {addEditTD type="left"}
	Has Preferred Language
    {/addEditTD}

    {addEditTD type="right"}
	<input type=checkbox name="has_voip_preferred_language" value="t" class=checkbox onClick='voip_preferred_language_select.toggle("voip_preferred_language")'>
    {/addEditTD}

    {addEditTD type="left"}
	Preferred Language
    {/addEditTD}

    {addEditTD type="right"}
	<input id="voip_preferred_language" type=text name="voip_preferred_language" value="{attrDefault target="group" default_var="voip_preferred_language" default_request="voip_preferred_language"}" class=small_text> 
    {/addEditTD}

  {/viewTable}
  <BR>
<script language="javascript">
	voip_preferred_language_select=new DomContainer();
	voip_preferred_language_select.disable_unselected=true;
	voip_preferred_language_select.addByID("voip_preferred_language");
{if attrDefault($group_attrs,"voip_preferred_language","has_voip_preferred_language")!=""}
    voip_preferred_language_select.select("voip_preferred_language");
    document.group_edit.has_voip_preferred_language.checked = true;
{else}
    voip_preferred_language_select.select(null);
{/if}
</script>

