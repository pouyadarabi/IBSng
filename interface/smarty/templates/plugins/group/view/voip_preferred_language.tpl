{viewTable title="VoIP Preferred Language" nofoot="TRUE"}
    {addEditTD type="left"}
	{strip}
	    {if $can_change} {editCheckBox edit_tpl_name="voip_preferred_language"} {/if}
	    Preferred Language
	{/strip}
    {/addEditTD}
    {addEditTD type="right"}
	{ifHasAttr object="group" var_name="voip_preferred_language"}
	    {$group_attrs.voip_preferred_language}
	{/ifHasAttr} 
	{helpicon subject="voip preferred language" category="user"}
    {/addEditTD}
{/viewTable}

