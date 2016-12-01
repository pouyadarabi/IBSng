{attrUpdateMethod update_method="voipPreferredLanguage"}
{userInfoTable title="VoIP Preferred Language" nofoot="TRUE"}
    {userInfoTD type="user_left"}
	Has VoIP Preferred Language
    {/userInfoTD}

    {userInfoTD type="user_right"}
	<input type=checkbox name="has_voip_preferred_language" value="t" class=checkbox onClick='voip_preferred_language_select.toggle("voip_preferred_language")'>
	{helpicon subject="voip preferred language" category="user"}
    {/userInfoTD}

    {userInfoTD type="group"}
	{ifHasAttr var_name="voip_preferred_language" object="group" alternate="No"}
	    Yes
	{/ifHasAttr}
    {/userInfoTD}

    {userInfoTD type="user_left"}
	Preferred Language
    {/userInfoTD}

    {userInfoTD type="user_right"}
	<input id="voip_preferred_language" type=text name="voip_preferred_language" value="{attrDefault target="user" default_var="voip_preferred_language" default_request="voip_preferred_language"}" class=small_text>
    {/userInfoTD}

    {userInfoTD type="group"}
	{ifHasAttr object="group" var_name="voip_preferred_language"}
	    {$group_attrs.voip_preferred_language}
	{/ifHasAttr} 
    {/userInfoTD}

{/userInfoTable}
<script language="javascript">
	voip_preferred_language_select=new DomContainer();
	voip_preferred_language_select.disable_unselected=true;
	voip_preferred_language_select.addByID("voip_preferred_language");
{if attrDefault($user_attrs,"voip_preferred_language","has_voip_preferred_language")!=""}
    voip_preferred_language_select.select("voip_preferred_language");
    document.user_edit.has_voip_preferred_language.checked = true;
{else}
    voip_preferred_language_select.select(null);
{/if}
</script>