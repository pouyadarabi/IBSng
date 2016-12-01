{* User Home

*}

{include file="user_header.tpl" title="Users Home" selected="home"}
{include file="err_head.tpl"}

{viewTable title="User Information" double="TRUE" table_width="580"}
    {addEditTD type="left1" double="TRUE"}
	Internet Username
    {/addEditTD}
    {addEditTD type="right1" double="TRUE"}
	{ifHasAttr var_name="normal_username" object="user"}
	    {$user_attrs.normal_username} 
	{/ifHasAttr}
    {/addEditTD}
    {addEditTD type="left2" double="TRUE"}
    	VoIP Username
    {/addEditTD}
    {addEditTD type="right2" double="TRUE"}
	{ifHasAttr var_name="voip_username" object="user"}
	    {$user_attrs.voip_username} 
	{/ifHasAttr}
    {/addEditTD}

    {addEditTD type="left1" double="TRUE"}
	Current Credit
    {/addEditTD}
    {addEditTD type="right1" double="TRUE"}
	{$user_info.basic_info.credit|price} {$MONEY_UNIT}
    {/addEditTD}
    {addEditTD type="left2" double="TRUE"}
    	Expiration Date
    {/addEditTD}
    {addEditTD type="right2" double="TRUE"}
	{ifHasAttr var_name="nearest_exp_date" object="user"}
	    {$user_attrs.nearest_exp_date} 
	{/ifHasAttr}
    {/addEditTD}

    {addEditTD type="left1" double="TRUE"}
	Locked
    {/addEditTD}
    {addEditTD type="right1" double="TRUE"}
	{ifHasAttr object="user" var_name="lock" alternate="No"}
	    Yes
	{/ifHasAttr}
    {/addEditTD}
    {addEditTD type="left2" double="TRUE"}
    	Creation Date
    {/addEditTD}
    {addEditTD type="right2" double="TRUE"}
	{$user_info.basic_info.creation_date} 
    {/addEditTD}


{/viewTable}

{include file="user/en/approx_duration.tpl"}
<br />
{include file="user/en/paccounting.tpl"}

{include file="user_footer.tpl"}