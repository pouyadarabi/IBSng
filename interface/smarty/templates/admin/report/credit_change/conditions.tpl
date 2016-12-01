{addEditTD type="left1" double=TRUE}
	User IDs
{/addEditTD}

{addEditTD type="right1" double=TRUE}
	<input type=text class=text name=user_ids value="{ifisinrequest name="user_ids"}"> {multistr input_name="user_ids" form_name="credit_change"}
{/addEditTD}

{addEditTD type="left2" double=TRUE}
	Issuer Admin
{/addEditTD}

{addEditTD type="right2" double=TRUE}
	{admin_names_select name="admin" default="All" default_request="admin" add_all=TRUE}
{/addEditTD}

{addEditTD type="left1" double=TRUE}
	Change Time From
{/addEditTD}

{addEditTD type="right1" double=TRUE}
	{absDateSelect name="change_time_from" default_request="change_time_from"}
{/addEditTD}

{addEditTD type="left2" double=TRUE}
	Change Time To
{/addEditTD}

{addEditTD type="right2" double=TRUE}
	{absDateSelect name="change_time_to" default_request="change_time_to"}
{/addEditTD}

{addEditTD type="left1" double=TRUE}
	Per User Credit Change
{/addEditTD}

{addEditTD type="right1" double=TRUE}
	{op class="ltgteq" name="per_user_credit_op" selected="per_user_credit_op"}
	<input type=text class=text name=per_user_credit credit value="{ifisinrequest name="per_user_credit"}"> {$MONEY_UNIT}
{/addEditTD}

{addEditTD type="left2" double=TRUE}
	Admin Credit Consumed
{/addEditTD}

{addEditTD type="right2" double=TRUE}
	{op class="ltgteq" name="admin_credit_op" selected="admin_credit_op"}
	<input type=text class=text name=admin_credit credit value="{ifisinrequest name="admin_credit"}"> {$MONEY_UNIT}
{/addEditTD}

{addEditTD type="left1" double=TRUE}
	Actions
{/addEditTD}

{addEditTD type="right1" double=TRUE}
	{html_options name="action" options=$actions selected=$actions_default}
{/addEditTD}

{addEditTD type="left2" double=TRUE}
	IP Address Of Admin
{/addEditTD}

{addEditTD type="right2" double=TRUE}
	<input type=text class=text name=remote_addr value="{ifisinrequest name="remote_addr"}"> {multistr input_name="remote_addr" form_name="credit_change"}
{/addEditTD}

{addEditTD type="left1" double=TRUE}
	Show Total Per User Credit
{/addEditTD}

{addEditTD type="right1" double=TRUE}
	<input type=checkbox class=checktext name=show_total_per_user_credit {checkBoxValue name="show_total_per_user_credit"}>
{/addEditTD}

{addEditTD type="left2" double=TRUE}
	Show Total Admin Consumed Credit
{/addEditTD}

{addEditTD type="right2" double=TRUE}
	<input type=checkbox class=checktext name=show_total_admin_credit {checkBoxValue name="show_total_admin_credit"}>
{/addEditTD}

{addEditTD type="left1" double=TRUE}
	Sort By
{/addEditTD}

{addEditTD type="right1" double=TRUE}
	{html_options name="order_by" options=$order_bys selected=$order_by_default} 
	Desc <input name=desc type=checkbox {checkBoxValue name="desc" default_checked=TRUE always_in_form="show"}>
{/addEditTD}

{addEditTD type="left2" double=TRUE}
	Results Per Page
{/addEditTD}

{addEditTD type="right2" double=TRUE}
	{reportRPP}
	View : {html_options name="view_options" options=$view_options selected=$view_by_default}
{/addEditTD}
