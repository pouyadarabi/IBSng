{viewTable title="Radius Attrs" nofoot="TRUE"}
    {addEditTD type="left" comment=TRUE}
	{strip}
	    {if $can_change}{editCheckBox edit_tpl_name="radius_attrs"}{/if}
	    Radius Attrs
	{/strip}
    {/addEditTD}
    {addEditTD type="right" comment=TRUE}
	{ifHasAttr object="group" var_name="radius_attrs"}
	    {$group_attrs.radius_attrs|nl2br}  
	{/ifHasAttr} 
	{helpicon subject="radius attrs" category="user"}
    {/addEditTD}

{/viewTable}
