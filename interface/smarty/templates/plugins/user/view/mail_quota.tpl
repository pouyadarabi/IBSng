{userInfoTable title="Mail Quota" nofoot="TRUE"}
    {userInfoTD type="user_left"}
        {if $can_change}{editCheckBox edit_tpl_name="mail_quota"}{/if}
        Has Mail Quota
    {/userInfoTD}
    {userInfoTD type="user_right"}
	{ifHasAttr object="user" var_name="mail_quota" alternate="No"}
	    Yes
	{/ifHasAttr} 
    {/userInfoTD}
    {userInfoTD type="group"}
	{ifHasAttr object="group" var_name="mail_quota" alternate="No"}
	    Yes
	{/ifHasAttr} 
    {/userInfoTD}

    {userInfoTD type="user_left"}
        Mailbox Quota
    {/userInfoTD}
    {userInfoTD type="user_right"}
	{ifHasAttr object="user" var_name="mail_quota"}
	    {$user_attrs.mail_quota|byte}  
	{/ifHasAttr} 
    {/userInfoTD}
    {userInfoTD type="group"}
	{ifHasAttr object="group" var_name="mail_quota"}
	    {$group_attrs.mail_quota|byte}
	{/ifHasAttr} 
	{helpicon subject="mail quota" category="user"}
    {/userInfoTD}

    {userInfoTD type="user_left"}
        Mailbox Usage
    {/userInfoTD}
    {userInfoTD type="user_right"}
	{ifHasAttr object="user" var_name="mail_usage"}
	    {$user_attrs.mail_usage|byte}  
	{/ifHasAttr} 
    {/userInfoTD}
    {userInfoTD type="group"}
	    N/A
	{helpicon subject="mail usage" category="user"}
    {/userInfoTD}

{/userInfoTable}
