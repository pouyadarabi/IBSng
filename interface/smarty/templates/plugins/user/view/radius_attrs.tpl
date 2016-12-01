{userInfoTable title="Radius Attributes" nofoot="TRUE"}
    {userInfoTD type="user_left" comment=TRUE}
        {if $can_change}{editCheckBox edit_tpl_name="radius_attrs"}{/if}
        Radius Attributes
    {/userInfoTD}
    {userInfoTD type="user_right" comment=TRUE}
	{ifHasAttr object="user" var_name="radius_attrs"}
	    {$user_attrs.radius_attrs|nl2br}  
	{/ifHasAttr} 
    {/userInfoTD}
    {userInfoTD type="group" comment=TRUE}
	{ifHasAttr object="group" var_name="radius_attrs"}
	    {$group_attrs.radius_attrs|nl2br}  
	{/ifHasAttr} 
	{helpicon subject="radius attrs" category="user"}
    {/userInfoTD}

{/userInfoTable}
