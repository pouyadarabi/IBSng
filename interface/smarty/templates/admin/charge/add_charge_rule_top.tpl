    	    {addEditTD type="left1" double="TRUE"}
		Charge Name
	    {/addEditTD}
	    {addEditTD type="right1" double="TRUE"}
		{$charge_name}<input type=hidden name=charge_name value="{$charge_name}">
	    <input type=hidden name=charge_name value="{$charge_name}">
	    {/addEditTD}
	    {addEditTD type="left2" double="TRUE"}
	    	Charge Rule ID
	    {/addEditTD}
	    {addEditTD type="right2" double="TRUE"}
		{$rule_id}<input type=hidden name=charge_rule_id value="{$rule_id}">
	    {/addEditTD}

    	    {addEditTD type="left1" double="TRUE" err="rule_start_err"}
		Rule Start Time
	    {/addEditTD}
	    {addEditTD type="right1" double="TRUE"}
		<input class="medium_text" type=text name=rule_start value="{ifisinrequest name="rule_start" default_var="start_time"}" >
	    <input type=hidden name=charge_name value="{$charge_name}">
	    {/addEditTD}
	    {addEditTD type="left2" double="TRUE" err="rule_end_err"}
	    	Rule End Time
	    {/addEditTD}
	    {addEditTD type="right2" double="TRUE"}
		<input class="medium_text" type=text name=rule_end value="{ifisinrequest name="rule_end" default_var="end_time"}">
	    {/addEditTD}