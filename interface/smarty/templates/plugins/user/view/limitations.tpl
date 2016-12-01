{userInfoTable title="Limitations" nofoot="TRUE"}
    {userInfoTD type="user_left"}
        {if $can_change}{editCheckBox edit_tpl_name="session_timeout"}{/if}
        Session Timeout
    {/userInfoTD}
    {userInfoTD type="user_right"}
	{ifHasAttr object="user" var_name="session_timeout"}
	    {$user_attrs.session_timeout} Seconds
	{/ifHasAttr} 
    {/userInfoTD}
    {userInfoTD type="group"}
	{ifHasAttr object="group" var_name="session_timeout"}
	    {$group_attrs.session_timeout} Seconds
	{/ifHasAttr} 
	{helpicon subject="session timeout" category="user"}
    {/userInfoTD}

    {userInfoTD type="user_left"}
        {if $can_change}{editCheckBox edit_tpl_name="idle_timeout"}{/if}
        Idle Timeout
    {/userInfoTD}
    {userInfoTD type="user_right"}
	{ifHasAttr object="user" var_name="idle_timeout"}
	    {$user_attrs.idle_timeout} Seconds
	{/ifHasAttr} 
    {/userInfoTD}
    {userInfoTD type="group"}
	{ifHasAttr object="group" var_name="idle_timeout"}
	    {$group_attrs.idle_timeout} Seconds
	{/ifHasAttr} 
	{helpicon subject="idle timeout" category="user"}
    {/userInfoTD}
 
    {userInfoTD type="user_left" comment=TRUE}
        {if $can_change}{editCheckBox edit_tpl_name="limit_mac"}{/if}
        Limit Mac Address
    {/userInfoTD}
    {userInfoTD type="user_right" comment=TRUE}
	{ifHasAttr object="user" var_name="limit_mac"}
	    {$user_attrs.limit_mac|replace:",":"<br>"}
	{/ifHasAttr} 
    {/userInfoTD}
    {userInfoTD type="group" comment=TRUE}
	{ifHasAttr object="group" var_name="limit_mac"}
	    {$group_attrs.limit_mac|replace:",":"<br>"}
	{/ifHasAttr} 
	{helpicon subject="Limit Mac Address" category="user"}
    {/userInfoTD}


    {userInfoTD type="user_left" comment=TRUE}
        {if $can_change}{editCheckBox edit_tpl_name="limit_station_ip"}{/if}
        Limit Station IP
    {/userInfoTD}
    {userInfoTD type="user_right" comment=TRUE}
	{ifHasAttr object="user" var_name="limit_station_ip"}
	    {$user_attrs.limit_station_ip|replace:",":"<br>"}
	{/ifHasAttr} 
    {/userInfoTD}
    {userInfoTD type="group" comment=TRUE}
	{ifHasAttr object="group" var_name="limit_station_ip"}
	    {$group_attrs.limit_station_ip|replace:",":"<br>"}
	{/ifHasAttr} 
	{helpicon subject="Limit Station IP Address" category="user"}
    {/userInfoTD}



    {userInfoTD type="user_left" comment=TRUE}
        {if $can_change}{editCheckBox edit_tpl_name="limit_caller_id"}{/if}
        Limit Caller ID
    {/userInfoTD}
    {userInfoTD type="user_right" comment=TRUE}
	{ifHasAttr object="user" var_name="limit_caller_id"}
	    {$user_attrs.limit_caller_id|replace:",":"<br>"}
	{/ifHasAttr} 
    {/userInfoTD}
    {userInfoTD type="group" comment=TRUE}
	{ifHasAttr object="group" var_name="limit_caller_id"}
	    {$group_attrs.limit_caller_id|replace:",":"<br>"}
	{/ifHasAttr} 
	{helpicon subject="Limit Caller ID" category="user"}
    {/userInfoTD}

    {userInfoTD type="user_left"}
        Allow user without Caller ID
    {/userInfoTD}
    {userInfoTD type="user_right"}
	{ifHasAttr object="user" var_name="limit_caller_id_allow_not_defined"}
	    {if $user_attrs.limit_caller_id_allow_not_defined == FALSE }
		No
	    {else}
		Yes
	    {/if}
	{/ifHasAttr} 
    {/userInfoTD}
    {userInfoTD type="group"}
	{ifHasAttr object="group" var_name="limit_caller_id_allow_not_defined"}
	    {if $group_attrs.limit_caller_id_allow_not_defined == FALSE }
		No
	    {else}
		Yes
	    {/if}
	{/ifHasAttr} 
	{helpicon subject="Allow users without caller id" category="user"}
    {/userInfoTD}

{/userInfoTable}
