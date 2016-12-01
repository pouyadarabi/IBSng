{viewTable title="Limitations" nofoot="TRUE"}
    {addEditTD type="left"}
	{strip}
	    {if $can_change}{editCheckBox edit_tpl_name="session_timeout"}{/if}
	    Session Timeout
	{/strip}
    {/addEditTD}
    {addEditTD type="right"}
	{ifHasAttr object="group" var_name="session_timeout"}
	    {$group_attrs.session_timeout} Seconds
	{/ifHasAttr} 
	{helpicon subject="session timeout" category="user"}
    {/addEditTD}

    {addEditTD type="left"}
	{strip}
	    {if $can_change}{editCheckBox edit_tpl_name="idle_timeout"}{/if}
	    Idle Timeout
	{/strip}
    {/addEditTD}
    {addEditTD type="right"}
	{ifHasAttr object="group" var_name="idle_timeout"}
	    {$group_attrs.idle_timeout} Seconds
	{/ifHasAttr} 
	{helpicon subject="idle timeout" category="user"}
    {/addEditTD}




    {addEditTD type="left" comment=TRUE}
	{strip}
	    {if $can_change}{editCheckBox edit_tpl_name="limit_mac"}{/if}
	    Limit Mac Address
	{/strip}
    {/addEditTD}
    {addEditTD type="right" comment=TRUE}
	{ifHasAttr object="group" var_name="limit_mac"}
	    {$group_attrs.limit_mac|replace:",":"<br>"}
	{/ifHasAttr} 
	{helpicon subject="limit mac address" category="user"}
    {/addEditTD}

    {addEditTD type="left" comment=TRUE}
	{strip}
	    {if $can_change}{editCheckBox edit_tpl_name="limit_station_ip"}{/if}
	    Limit IP Address
	{/strip}
    {/addEditTD}
    {addEditTD type="right" comment=TRUE}
	{ifHasAttr object="group" var_name="limit_station_ip"}
	    {$group_attrs.limit_station_ip|replace:",":"<br>"}
	{/ifHasAttr} 
	{helpicon subject="limit station address" category="user"}
    {/addEditTD}

    {addEditTD type="left" comment=TRUE}
	{strip}
	    {if $can_change}{editCheckBox edit_tpl_name="limit_caller_id"}{/if}
	    Limit Caller ID
	{/strip}
    {/addEditTD}
    {addEditTD type="right"}
	{ifHasAttr object="group" var_name="limit_caller_id"}
	    {$group_attrs.limit_caller_id|replace:",":"<br>"}
	{/ifHasAttr} 
	{helpicon subject="limit caller id" category="user"}
    {/addEditTD}

    {addEditTD type="left"}
	{strip}
	    Allow users without caller id
	{/strip}
    {/addEditTD}
    {addEditTD type="right"}
	{ifHasAttr object="group" var_name="limit_caller_id"}
	    {if $group_attrs.limit_caller_id_allow_not_defined == FALSE }
		No
	    {else}
		Yes
	    {/if}
	{/ifHasAttr} 
	{helpicon subject="allow user without caller id" category="user"}
    {/addEditTD}



{/viewTable}
