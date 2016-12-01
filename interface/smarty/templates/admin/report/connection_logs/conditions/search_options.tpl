{addEditTD type="left1" double=TRUE}
	User IDs
{/addEditTD}

{addEditTD type="right1" double=TRUE}
	<input type=text class=text name=user_ids value="{ifisinrequest name="user_ids"}"> {multistr input_name="user_ids" form_name="connections"}
{/addEditTD}

{addEditTD type="left2" double=TRUE}
	Owner
{/addEditTD}

{addEditTD type="right2" double=TRUE}
	{admin_names_select name="owner" default="All" default_request="owner" add_all=TRUE}
{/addEditTD}

{addEditTD type="left1" double=TRUE}
	Login Time From
{/addEditTD}

{addEditTD type="right1" double=TRUE}
	{absDateSelect name="login_time_from" default_request="login_time_from"}
{/addEditTD}

{addEditTD type="left2" double=TRUE}
	Login Time To
{/addEditTD}

{addEditTD type="right2" double=TRUE}
	{absDateSelect name="login_time_to" default_request="login_time_to"}
{/addEditTD}

{addEditTD type="left1" double=TRUE}
	Internet Username
{/addEditTD}

{addEditTD type="right1" double=TRUE}
	<input type=text class=text name=username value="{ifisinrequest name="username"}"> 
{/addEditTD}

{addEditTD type="left2" double=TRUE}
	VoIP Username
{/addEditTD}

{addEditTD type="right2" double=TRUE}
	<input type=text class=text name=voip_username value="{ifisinrequest name="voip_username"}">
{/addEditTD}

{addEditTD type="left1" double=TRUE}
	Mac Address
{/addEditTD}

{addEditTD type="right1" double=TRUE}
	<input type=text class=text name=mac value="{ifisinrequest name="mac"}">
{/addEditTD}

{addEditTD type="left2" double=TRUE}
	Caller ID
{/addEditTD}

{addEditTD type="right2" double=TRUE}
	<input type=text class=text name=caller_id value="{ifisinrequest name="caller_id"}">
{/addEditTD}

{addEditTD type="left1" double=TRUE}
	Remote IP
{/addEditTD}

{addEditTD type="right1" double=TRUE}
	<input type=text class=text name=remote_ip value="{ifisinrequest name="remote_ip"}">
{/addEditTD}

{addEditTD type="left2" double=TRUE}
	Station IP
{/addEditTD}

{addEditTD type="right2" double=TRUE}
	<input type=text class=text name=station_ip value="{ifisinrequest name="station_ip"}">
{/addEditTD}

{addEditTD type="left1" double=TRUE}
	Credit Used
{/addEditTD}

{addEditTD type="right1" double=TRUE}
	{op class="ltgteq" name="credit_used_op" selected="credit_used_op"}
	<input type=text class=small_text name=credit_used value="{ifisinrequest name="credit_used"}"> {$MONEY_UNIT}
{/addEditTD}

{addEditTD type="left2" double=TRUE}
	Show Totals of
{/addEditTD}

{addEditTD type="right2" double=TRUE}
	Credit <input type=checkbox class=checktext name=show_total_credit_used {checkBoxValue name="show_total_credit_used"}>
	Duration 	<input type=checkbox class=checktext name=show_total_duration {checkBoxValue name="show_total_duration"}>
	In/Out Bytes<input type=checkbox class=checktext name=show_total_inouts {checkBoxValue name="show_total_inouts"}>
{/addEditTD}

{addEditTD type="left1" double=TRUE}
	Successful Logins
{/addEditTD}

{addEditTD type="right1" double=TRUE}
	Yes <input type=checkbox class=checktext name="successful_yes" {checkBoxValue name="successful_yes" always_in_form="admin_connection_logs" default_checked="TRUE"}>
	No <input type=checkbox class=checktext name="successful_no" {checkBoxValue name="successful_no" always_in_form="admin_connection_logs" default_checked="TRUE"}>
{/addEditTD}

{addEditTD type="left2" double=TRUE}
	Service
{/addEditTD}

{addEditTD type="right2" double=TRUE}
	Internet <input type=checkbox class=checktext name="service_internet" {checkBoxValue name="service_internet" always_in_form="admin_connection_logs" default_checked="TRUE"}>
	VoIP <input type=checkbox class=checktext name="service_voip" {checkBoxValue name="service_voip" always_in_form="admin_connection_logs" default_checked="TRUE"}>
{/addEditTD}


{addEditTD type="left1" double=TRUE}
	Sort By
{/addEditTD}

{addEditTD type="right1" double=TRUE}
	{html_options name="order_by" options=$order_bys selected=$order_by_default} 
	Desc <input name=desc type=checkbox {checkBoxValue name="desc" default_checked=TRUE always_in_form="admin_connection_logs"}>
{/addEditTD}

{addEditTD type="left2" double=TRUE}
		Results Per Page
{/addEditTD}

{addEditTD type="right2" double=TRUE}
	{reportRPP}
	View : {html_options name="view_options" options=$view_options selected=$view_by_default}
{/addEditTD}
